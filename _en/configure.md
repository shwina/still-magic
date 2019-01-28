---
title: "Configuring Software"
questions:
-   "How can I make it easy for users to configure software?"
objectives:
-   "Describe the four levels of configuration typically used by robust software."
-   "Explain what an overlay configuration is."
-   "Explain why nested configuration options are usually not a good idea."
-   "Add flat overlay configuration to a small application."
keypoints:
-   "Use short command-line parameters to set commonly-changed options."
-   "Allow long command-line parameters to change all other options to facilitate scripting."
-   "Use the `getopt` library to parse command-line flags."
-   "Read a system-wide configuration file, then a user configuration file, then a job configuration file."
-   "Format configuration files using YAML."
-   "Dump all configuration values in the same format used for input on request."
-   "Include the software version number in the dumped configuration."
---

A program that does exactly the same thing every time we run it
isn't as useful as one that can work on different files
or analyze data with different thresholds.
Software of all kinds needs to be controlled;
some things change more often than others,
so we need a simple, uniform way to specify some options and leave others alone.

The modern Unix convention is to provide four levels of configuration:

1.  A system-wide configuration file for general settings.
2.  A user-specific configuration file for personal preferences.
3.  A job-specific file with settings for a specific run.
4.  Command-line options to change things that commonly change.

This is sometimes called [overlay configuration](#g:overlay-configuration)
because each level overrides the ones above it:
the user's configuration file overrides the system settings,
the job configuration overrides the user's defaults,
and the command-line options overrides that.

## How can I handle command-line flags consistently? {#s:configure-cmdline}

Modern Python programs use the `argparse` library for handling command-line arguments,
but the older and simpler `getopt` library will illustrate the core ideas,
so we will use it.

`getopt` works by matching a specification of what [flags](#g:flag) are allowed
against a list of actual command-line arguments.
In simplest form,
the spec is string listing all the single-letter flags,
with colons showing the ones that take arguments.
For example, the string `b:q` means
"the `-b` flag takes an argument and the `-q` flag doesn't".

The list of actual arguments is almost always `sys.argv[1:]`,
i.e.,
all of the command-line arguments except for the name of the program itself.
(The name `argv` stands for "argument vector",
and is a holdover from the days of C.)
Given the spec and the list of actual arguments,
`getopt` returns two lists:
the first is the (flag, argument) pairs it matched,
and the second is everything else---typically a list of files to be processed.

```python
from getopt import getopt

args = ['-q', '-b', '/tmp/log.txt', 'file1.txt', 'file2.txt']
options, extras = getopt(args, 'b:q')
print('options is', options)
print('extras is', extras)
```
{: title="configure/getopt_simple.py"}
```
options is [('-q', ''), ('-b', '/tmp/log.txt')]
extras is ['file1.txt', 'file2.txt']
```

Once we have these two lists,
we can define default values for our configuration
and then loop over the (flag, argument) pairs to override those values:

```python
# Defaults.
logfile = None
quiet = False

# Override based on command-line options.
for (opt, arg) in options:
    if opt == '-b':
        logfile = arg
    elif opt == '-q':
        quiet = True
    else:
        assert False, 'unrecognized option {}'.format(opt)
print('Log file is {} and quiet is {}'.format(logfile, quiet))
```
{: title="configure/getopt_simple.py"}
```text
Log file is /tmp/log.txt and quiet is True
```

This pattern is called [set and override](#g:set-and-override),
and makes programs easier to understand
by putting all of the default settings in one place.
Since we will often want to pass those settings into functions that do the actual work,
it's very common to put the entire configuration in a [dictionary](#g:dictionary)
so that we have a single [configuration object](#g:configuration-object) to pass around.
It's also common to check that some configuration values aren't accidentally being set twice.
After rearranging our code a little,
we get this:

```python
import sys
from getopt import getopt

# Defaults.
settings = {
    'logfile' : None,
    'quiet' : False
}

# Override based on command-line options.
options, extras = getopt(sys.argv[1:], 'b:q')
for (opt, arg) in options:
    if opt == '-b':
        assert settings['logfile'] is None, 'cannot set logfile twice'
        settings['logfile'] = arg
    elif opt == '-q':
        settings['quiet'] = True
    else:
        assert False, 'unrecognized option {}'.format(opt)

# Display.
print('Log file {}'.format(settings['logfile']))
print('Quiet {}'.format(settings['quiet']))
print('Extras {}'.format(extras))
```
{: title="configure/getopt_dict.py"}

<!-- == \noindent -->
which we can run like this:

```shell
$ python getopt_dict.py -q first.txt
```
```text
Log file None
Quiet True
Extras ['first.txt']
```

We really shouldn't use [`assert`](#g:assertion) to handle errors here;
[CHAPTER](../logging/) will explore a better approach.

## What do I do when I run out of memorable single-letter flags? {#s:configure-long}

Taschuk's Third Rule says, "Make common operations easy to control." [Tasc2017](#BIB)
so that users can control everything from a shell script without having to create temporary configuration files.
However,
there are only so many single-letter flags available,
and using `-b` to specify the name of a log file is hardly intuitive.

To allow for this,
`getopt` handles another kind of flag:
a double dash followed by a longer name like `--erase-temp-files`.
These flags can take a single argument like their single-letter siblings.
To tell `getopt` what long names it should recognize,
we give the function an extra list
and use `=` as a suffix to indicate if the option takes an argument.

```python
from getopt import getopt

args = ['-q', '--logfile', '/tmp/log.txt', '--overwrite', 'file1.txt', 'file2.txt']
options, extras = getopt(args, 'b:q', ['logfile=', 'overwrite'])
print('options is', options)
print('extras is', extras)
```
{: title="configure/getopt_long.py"}
```
options is [('-q', ''), ('--logfile', '/tmp/log.txt'), ('--overwrite', '')]
extras is ['file1.txt', 'file2.txt']
```

It's common to use single-letter flags for the most frequently changed options
and long names for things that are changed less frequently,
and to provide long-name aliases for the single-letter flags
(e.g., to have `--all-files` mean the same thing as `-a`).

## How can I manage configuration files consistently? {#s:configure-files}

Controlling programs from the command line is useful,
but complex programs can have many different configuration options,
and it's very useful to be able to save settings in a file for later reference
(and reproducibility).
Enabling a program to read its configuration from a file
also allows users to set values once and then not worry about them,
which is particularly useful when they're installing the software on their own computer
and want to put temporary files in a different location
or change the value of the alpha parameter for fitting curves.

Programmers have invented many formats for configuration files,
so please do not create your own.
One possibility is to write the configuration as a Python data structure
and then load it as if it was a library.
This is clever,
but it's hard for tools in other languages to process.
Programers are also fond of [JSON](#g:json),
which is a subset of the syntax that JavaScript uses for data structures,
but that involves a lot of curly braces.
A third option is the [Windows INI format][ini-format],
which is laid out like this:

```text
[section_1]
key_1=value_1
key_2=value_2

[section_2]
key_3=value_3
key_4=value_4
```

INI files are simple to read and write,
but the format is slowly falling out of use.
What seems to be replacing it is [YAML](#g:yaml),
which stands for "Yet Another Markup Language".
Since YAML is used in GitHub Pages ([CHAPTER](../ghp/)),
and (unlike JSON) allows comments,
we'll explore it in this section.

Here's a sample configuration file:

```text
# Example configuration file
logfile: "/tmp/log.txt"
quiet: false
overwrite: false
fonts:
- Verdana
- Serif
```
{: title="configure/config.yml"}

<!-- == \noindent -->
And here's a short Python program that reads and prints that configuration:

```python
import yaml

with open('config.yml', 'r') as reader:
    config = yaml.load(reader)
print(config)
```
{: title="configure/read_config.py"}
```text
{'logfile': '/tmp/log.txt', 'quiet': False, 'overwrite': False, 'fonts': ['Verdana', 'Serif']}
```

Simple YAML files are simple to write:

1.  Lines starting with `#` are comments.
2.  A line `key: value` defines a value for the given key.
    Values can be numbers,
    `true` or `false`,
    or quoted strings.
    (Strings don't actually have to be quoted in every case,
    but the file is a lot easier to understand if you always use quotes.)
3.  A point-form list underneath a key becomes an array of values.

When a file like this is read in Python,
the result is a dictionary.
YAML allows nested keys and lists,
but if you need them,
you're probably doing something wrong [Xu2015](#BIB):
most users never use most configuration options and find their presence confusing.

## How can I implement overlay configuration? {#s:configure-overlay}

We said at the start that programs often have
system-wide, per-user, and per-job configuration files,
with each overriding values from the one(s) before
and command-line parameters overriding the rest.
We can implement this using `dict.update`,
which updates one dictionary with values from another:

```python
def get_full_configuration(filenames, command_line={}):
    '''
    Overlay configuration files and command-line parameters,
    returning configuration object.
    '''
    result = {}
    for f in filenames:
        with open(f, 'r') as reader:
            config = yaml.load(reader)
            result.update(config)
    result.update(command_line)
    return result
```
{: title="configure/util.py"}

This function creates an empty dictionary to hold settings.
It then reads each specified configuration file in turn
and updates the result dictionary with whatever it found in that file.
If a file defines values that were previously defined in an earlier file,
the `update` method call automatically overwrites the older values.
We end by overriding what we read from the files with whatever was given on the command line;
we'll have to convert `getopt`'s output to a dictionary,
but that's straightforward---the only trick is to match
the command-line flag (like `-q`) to the configuration variable name (like `quiet`):

```python
def getopt_to_dict(pairs, names):
    '''
    Convert [(flag, value)...] pairs and {flag: config...} names
    to dictionary.
    '''
    result = {}
    for (key, value) in pairs:
        result[names[key]] = value
    return result
```
{: title="configure/util.py"}

We can test this with these three configuration files
(we have lined up corresponding values to make them easier to see):

<table>
  <tr>
    <th><code>system.yml</code></th>
    <th><code>user.yml</code></th>
    <th><code>job.yml</code></th>
  </tr>
  <tr>
    <tr><code>quiet: true</code></tr>
    <tr><code>quiet: false</code></tr>
    <tr><code></code></tr>
  </tr>
  <tr>
    <tr><code></code></tr>
    <tr><code>logfile: "/tmp/log.txt"</code></tr>
    <tr><code>logfile: "./complaints.txt"</code></tr>
  </tr>
</table>
<!-- {: title="configure/system.yml"} -->
<!-- {: title="configure/user.yml"} -->
<!-- {: title="configure/job.yml"} -->

<!-- == \noindent -->
using this test program:

```python
import sys
from getopt import getopt
from util import get_full_configuration, getopt_to_dict

config_files = ['system.yml', 'user.yml', 'job.yml']

options, extras = getopt('b:q', sys.argv[1:])
options = getopt_to_dict(options, {'-b': 'logfile', '-q': 'quiet'})
config = get_full_configuration(config_files, options)
print(config)
```
{: title="configure/test_config.py"}

<!-- == \noindent -->
and this command line:

```shell
$ python test-config.py -q
```
```text
{'quiet': False, 'logfile': './complaints.txt'}
```

## How can I find configuration files? {#s:configure-find}

Our configuration files will usually not all be in the same directory.
System-wide settings for an application called `app` are often stored in `/etc/app.yml`.
Alternatively,
some programs will set an environment variable APP to the name of the installation directory,
and then read the system configuration file from `$APP/app.yml`.
We can use `os.getenv('APP')` to get the value of the environment variable `APP`,
then append `app.yml` and load that.
(Older programs often use the name `app.rc`,
where "rc" stands for "resource control".)

Similarly,
we can get personal settings from `$HOME/.app.yml`;
the leading '.' hides the configuration file from `ls`.
Finally,
per-job settings can come from `app.yml` in the current directory,
where again "app" is replaced with the name of the program.
Here's a utility routine that constructs and checks these filenames:

```python
def find_config_files(name):
    '''
    Construct a list of configuration files for the named application.
    '''
    app_yml = name + '.yml'
    locations = [(name.upper(), app_yml),
                 ('HOME', '.' + app_yml),
                 ('PWD', app_yml)]
    result = []
    for (var, filename) in locations:
        value = os.getenv(var)
        if value:
            path = os.path.join(value, filename)
            if os.path.isfile(path):
                result.append(path)
    return result
```

Note that we use `os.path.isfile` to check that file exists before trying to read it.

## How can I keep a record of the actual configuration that produced particular results? {#s:configure-dump}

Careful record keeping is essential to reproducible science,
and if *we* are careful,
the computer can do the record keeping.
We can save the entire (merged) configuration object for a particular run of a program
using `yaml.dump`.
If we have written our configuration functions correctly,
this will let us re-create configuration on another machine
even if it has different default settings.
The test is whether our program can load a dumped configuration,
then dump it again and get the same result.

If we're going to do this,
we should always include a version number as a field in the dumped configuration;
our program should also print this out when given a `--version` flag.
We need this because how we interpret options will change over time,
and if you don't know what the version of the program was,
we'll have to guess what options mean.

## Summary {#s:workflow-summary}

-   Many tool also allow longer command-line options to control everything to support scripting
    -   Out of scope of this lesson
-   Every tool acts as if it was the only extra thing your project needed
    -   So you wind up with lots of configuration files littering your root directory
    -   Tempting to move them all to `./etc/`, but tools don't know to look there

<figure id="f:configure-concept"> <figcaption>Configuration Concept Map</figcaption> <img src="../../figures/configure_concept.svg"/> </figure>

## Exercises {#s:workflow-exercises}

-   FIXME: dump configuration and check.
    -   How to handle lack of order in keys? (answer: use deep equality)
-   FIXME: implement flag to read entire configuration from file *and nothing else*.
-   FIXME: implement `usage` function to display message and exit instead of using `assert`.
-   FIXME: how to handle reading from stdin/stdout if no files specified.

{% include links.md %}
