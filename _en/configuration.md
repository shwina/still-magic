---
permalink: "/en/configuration/"
title: "Configuration"
undone: true
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

-   Software needs to be controlled
    -   Some things change more often than others
    -   Want a simple, uniform way to specify some options and leave others alone
-   Modern Unix convention is [overlay configuration](../gloss/#g:overlay-configuration)
    -   Short command-line options to change things that commonly change
    -   Per-result configuration file to control all those same options
    -   Per-user configuration file for personal preferences
    -   Per-system configuration file for system-wide preferences
-   Usually also allow longer command-line options to control everything to support scripting
    -   Out of scope of this lesson

## How Can I Handle Command-Line Flags Consistently? {#s:configuration-cmdline}

-   Use `getopt` for simple programs and `argparse` for complex ones
    -   `getopt` example will illustrate the ideas
-   Two kinds of flags:
    -   `-a`: single dash, single letter
    -   `--long-name`: double dash, full name (conventionally hyphenated)
-   Either kind can be on its own or take a single argument
-   `getopt` matches a spec against a list of command-line arguments
    -   Typically `sys.argv[1:]` (i.e., program name removed)
-   In simplest form, spec is all the single-letter flags, with colons showing the ones that take arguments
-   Get back a list of (flag, argument) pairs and a list of everything else

```python
from getopt import getopt

args = ['-q', '-b', '/tmp/log.txt', 'file1.txt', 'file2.txt']
options, extras = getopt(args, 'b:q')
print('options is', options)
print('extras is', extras)
```
```
options is [('-q', ''), ('-b', '/tmp/log.txt')]
extras is ['file1.txt', 'file2.txt']
```

-   Typically loop over the (flag, argument) pairs to set up controls

```python
logfile = None
quiet = False
for (opt, arg) in options:
    if opt == '-b':
        logfile = arg
    elif opt == '-q':
        quiet = True
    else:
        assert False, 'unrecognized option {}'.format(opt)
```

-   Optionally provide a list of long-name options
    -   Indicate which take parameters by appending '=' to the name

```python
args = ['-q', '--logfile', '/tmp/log.txt', '--overwrite', 'file1.txt', 'file2.txt']
options, extras = getopt(args, 'b:q', ['logfile=', 'overwrite'])
print('options is', options)
print('extras is', extras)
```
```
options is [('-q', ''), ('--logfile', '/tmp/log.txt'), ('--overwrite', '')]
extras is ['file1.txt', 'file2.txt']
```

-   Taschuk's Rules: always provide a way to set all options from the command line
    -   So that users can control everything from a shell script without having to create temporary configuration files
-   Only provide short (single-letter) flags for commonly-used options
    -   Signals what you expect to change frequently and what you expect will be left alone

## How Can I Manage Configuration Files Consistently? {#s:configuration-files}

-   Enable program to read configuration from file
    -   Because in manual use, a lot of values stay the same
    -   And whoever installs the software on the cluster may want to set some defaults
-   Many formats for configuration files, so do not create your own
    -   Actual Python (but hard for tools in other languages to process)
    -   Windows INI files (falling out of fashion)
    -   JSON (but that's a lot of curly braces...)
-   YAML is becoming the most popular
    -   And is used in the headers of Markdown pages, so you might as well get used to it
    -   And allows comments

```yaml
# Example configuration file
logfile: "/tmp/log.txt"
quiet: false
overwrite: false
fonts:
- Verdana
- Serif
```
```python
import yaml

with open('config.yml', 'r') as reader:
    config = yaml.load(reader)
print(config)
```
```
{'logfile': '/tmp/log.txt', 'quiet': False, 'overwrite': False, 'fonts': ['Verdana', 'Serif']}
```

-   If your configuration file needs more depth than this, you're probably doing something wrong [Xu2015](#BIB)
    -   Most users never use most configuration options
    -   And find their presence confusing
-   Return to command-line parsing
    -   Rather than creating a bunch of free-standing variables, fill in one dictionary of options
    -   `if config['quiet']` is only a little more typing than `if quiet`, intent is clearer, and it's consistent with reaing from config files

## How Can I Implement Multi-Layer Configuration? {#s:configuration-overlay}

-   System settings, then user settings, then job settings, each overriding what came before
-   use `dict.update` to overwrite previous settings

```python
def get_full_configuration(filenames, command_line={}):
    result = {}
    for f in filenames:
        with open(f, 'r') as reader:
            config = yaml.load(reader)
            result.update(config)
    result.update(command_line)
    return result
```

-   System-wide settings:
    -   `/etc/app.yml` for system settings standard applications
        -   Use your program's name instead of `app`
    -   If you set an environment variable to the install location `$APP/config.rc`
        -   Use `os.getenv('APP')` to get the value of the environment variable
-   Personal settings:
    -   `$HOME/.app.yml` (the leading '.' hides it from `ls`)
    -   Many use `.rc` (which stands for "resource control" - an old Unix convention)
-   Per-run settings:
    -   Look in current directory for a file with a specific name
    -   But also provide a command-line way to override (like `Makefile` and `-f filename.mk`)
-   Use `os.path.isfile` to check that file exists

```python
def find_configuration_files():
    locations = [('APP', 'config.yml', ('HOME', '.app.yml', ('PWD', 'config.yml')]
    result = []
    for (var, filename) in locations:
        if os.getenv(var) is not None:
            path = os.path.join(os.getenv(var), filename)
            if os.path.isfile(path):
                result.append(path)
    return result
```

## How Can I Keep a Record of the Actual Configuration That Produced Particular Results? {#s:configuration-dump}

-   Careful record keeping is essential to reproducible science
    -   The computer can do the record keeping
-   Save entire (merged) configuration using `yaml.dump`
    -   Guaranteed to re-create configuration even on another machine with different defaults
    -   Test: program should be able to load a dumped configuration
-   Include this in the program's log as a single string
    -   Do not write one record per value, since that will mean more parsing work to reload
    -   And can easily lead to confusion about what's part of the log and what's part of the configuration
    -   And you're likely to have multiple configurations in a log if your pipeline has multiple stages
-   Always include a version number as a field in the dumped configuration
    -   The `--version` flag should produce this as well
-   Because option interpretation will change over time, and if you don't know what the version was, you'll have to guess

## Summary {#s:workflow-summary}

FIXME: create concept map for configuration

{% include links.md %}
