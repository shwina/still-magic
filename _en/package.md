---
title: "Packaging"
undone: true
questions:
-   "How can I manage the libraries my project relies on?"
-   "How can I package up my work for others to use?"
objectives:
-   "Create and use virtual environments to manage library versions without conflict."
-   "Create and test a citable, shareable Pip package."
keypoints:
-   "Use `virtualenv` to create a separate virtual environment for each project."
-   "Use `pip` to create a distributable package containing your project's software, documentation, and data."
---

> Another response of the wizards,
> when faced with a new and unique situation,
> was to look through their libraries to see if it had ever happened before.
> This was...a good survival trait.
> It meant that in times of danger you spent the day sitting very quietly in a building with very thick walls.
>
> -- Terry Pratchett

-   A programming language is a way to build and combine software libraries
-   Every widely-used language now has a shared repository for installable packages
-   This lesson shows you how to use Python's tools
-   Based in part on [Python 102][python-102] by [Ashwin Srinath][srinath-ashwin]

## How Can I Turn a Set of Python Source Files Into a Module? {#s:package-modules}

-   Any Python source file can be imported
    -   Statements are executed as the file is loaded
    -   Variables defined in the file are then available as `module.name`
    -   This is why Python files should be named using pothole\_case instead of kebab-case
-   Example: put constant and two functions used in Zipf's Law study in `zipf.py`

```python
from pytest import approx


RELATIVE_ERROR = 0.05


def make_zipf(length):
    assert length > 0, 'Zipf distribution must have at least one element'
    result = [1/(1 + i) for i in range(length)]
    return result


def is_zipf(hist, rel=RELATIVE_ERROR):
    assert len(hist) > 0, 'Cannot test Zipfiness without data'
    scaled = [h/hist[0] for h in hist]
    perfect = make_zipf(len(hist))
    return scaled == approx(perfect, rel=rel)
```

-   Can now `import zipf`, `from zipf import is_zipf`, etc.

```python
from zipf import make_zipf, is_zipf

generated = make_zipf(5)
print('generated distribution: {}'.format(generated))
generated[-1] *= 2
print('passes test with default tolerance: {}'.format(is_zipf(generated)))
print('passes test with tolerance of 1.0: {}'.format(is_zipf(generated, rel=1.0)))
```
```
generated distribution: [1.0, 0.5, 0.3333333333333333, 0.25, 0.2]
passes test with default tolerance: False
passes test with tolerance of 1.0: True
```

-   Running this program creates a sub-directory called `__pycache__`
    -   Holds the compiled version of the imported files
    -   Almost always put `__pycache__` in `.gitignore`
-   When `import` executes, it checks in order:
    -   Is this module already in memory?
    -   Is the cached compiled version younger than the source file?
-   What if we want to be able to import *and* to be able to run as a program?
    -   Python creates a variable called `__name__` in each module
    -   If the module is the main program, that variable is assigned the string `'__main__'`
    -   Otherwise, it has the module's name

```python
import sys
from pytest import approx

USAGE = '''zipf num [num...]: are the given values a Zipfy?'''
RELATIVE_ERROR = 0.05


def make_zipf(length):
    ...as before...

def is_zipf(hist, rel=RELATIVE_ERROR):
    ...as before...


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print(USAGE)
    else:
        values = [int(a) for a in sys.argv[1:]]
        result = is_zipf(values)
        print('{}: {}'.format(result, values))
    sys.exit(0)
```

-   Code guarded by `if __name__ == '__main__'` isn't executed when file loaded by something else
-   Can test by re-running `use.py`
    -   The usage message doesn't appear, which means the main block wasn't executed, which is what we want
    -   So now we can go back and put its content in a function and call that function, because we are good people

## How Can I Install a Python Package? {#s:package-install}

-   `pip install package`
    -   Checks to see if the package is already installed (or needs to be upgraded)
    -   Downloads from [PyPI][pypi] (the Python Package Index)
    -   Unpacks and installs
-   May require admin privileges to write files, depending on where Python is installed
-   `pip install -r filename` will install dependencies listed in a file
    -   File is conventionally called `requirements.txt` and placed in the project's root directory
-   Can be just a list of package names
-   Or specify exact versions, minimum versions, etc.

```
request
scipy==1.1.0
tdda>=1.0
```

-   `pip freeze` will print exact versions of all installed packages
    -   Save this when producing reports ([s:publish](#CHAPTER))

## How Can I Create an Installable Python Package? {#s:package-package}

-   Next step: put the two functions in their own files underneath a `zipf` package
    -   Would probably keep them in the same file in a real project, because they're small and closely related
    -   But this will illustrate the key ideas
-   A [package](#g:package) is a directory that contains a file called `__init__.py`, and may contain other files or sub-directories containing files
    -   `__init__.py` can contain useful code
    -   Or it can be empty, but it has to be there to tell Python that this directory is a package
-   Files and directories are:

```
+- use.py
+- zipf
    +- __init__.py
```

-   `zipf/__init__.py` contains the functions and `RELATIVE_ERROR`
-   Import and use as before
    -   The `__pycache__` directory is created inside `zipf`

-   Now split code between two files to show how that works
    -   Put the generator in `zipf/generate.py`
    -   `__init__.py` must now import that
    -   But can do so using `from . import ...` (where "." means the same thing it does in the Unix shell)
    -   Client code now uses `zipf.generate.make_zipf`

```python
import sys
from pytest import approx
from . import generate

RELATIVE_ERROR = 0.05


def is_zipf(hist, rel=RELATIVE_ERROR):
    assert len(hist) > 0, 'Cannot test Zipfiness without data'
    scaled = [h/hist[0] for h in hist]
    perfect = generate.make_zipf(len(hist))
    return scaled == approx(perfect, rel=rel)
```
```python
import zipf

generated = zipf.generate.make_zipf(5)
print('generated distribution: {}'.format(generated))
generated[-1] *= 2
print('passes test with default tolerance: {}'.format(zipf.is_zipf(generated)))
print('passes test with tolerance of 1.0: {}'.format(zipf.is_zipf(generated, rel=1.0)))
```

## How Can I Distribute Software Packages That I Have Created? {#s:package-distribute}

-   Yes, people can clone your repository and copy files from that
-   But it's much friendlier to create something they can install
-   Unfortunately, Python has several ways to do this
-   We will show [setuptools][setuptools], which is the tried-and-true approach
    -   `conda` is the modern does-everything solution, but has larger startup overhead
-   Create a file in the directory *above* the root directory of the package called `setup.py`
    -   Must be called exactly that

```
+- setup.py
+- use.py
+- zipf
    +- __init__.py
    +- generate.py
```


-   Add exactly and only these lines

```
from setuptools import setup, find_packages

setup(
    name='zipf',
    version='0.1',
    author='Greg Wilson',
    packages=find_packages()
)
```

-   `find_packages` returns a list of things worth packaging
-   Run `python setup.py sdist` to create a source distribution

```
$ python setup.py sdist
running sdist
running egg_info
creating zipf.egg-info
writing zipf.egg-info/PKG-INFO
writing dependency_links to zipf.egg-info/dependency_links.txt
writing top-level names to zipf.egg-info/top_level.txt
writing manifest file 'zipf.egg-info/SOURCES.txt'
reading manifest file 'zipf.egg-info/SOURCES.txt'
writing manifest file 'zipf.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
warning: check: missing required meta-data: url

warning: check: missing meta-data: if 'author' supplied, 'author_email' must be supplied too

creating zipf-0.1
creating zipf-0.1/zipf
creating zipf-0.1/zipf.egg-info
copying files to zipf-0.1...
copying setup.py -> zipf-0.1
copying zipf/__init__.py -> zipf-0.1/zipf
copying zipf/generate.py -> zipf-0.1/zipf
copying zipf.egg-info/PKG-INFO -> zipf-0.1/zipf.egg-info
copying zipf.egg-info/SOURCES.txt -> zipf-0.1/zipf.egg-info
copying zipf.egg-info/dependency_links.txt -> zipf-0.1/zipf.egg-info
copying zipf.egg-info/top_level.txt -> zipf-0.1/zipf.egg-info
Writing zipf-0.1/setup.cfg
creating dist
Creating tar archive
removing 'zipf-0.1' (and everything under it)
```

-   Creates `dist/zipf-0.1.tar.gz`

```
$ tar ztvf dist/zipf-0.1.tar.gz 
drwxr-xr-x  0 standage staff       0 20 Aug 15:36 zipf-0.1/
-rw-r--r--  0 standage staff     180 20 Aug 15:36 zipf-0.1/PKG-INFO
-rw-r--r--  0 standage staff      38 20 Aug 15:36 zipf-0.1/setup.cfg
-rw-r--r--  0 standage staff     145 20 Aug 13:40 zipf-0.1/setup.py
drwxr-xr-x  0 standage staff       0 20 Aug 15:36 zipf-0.1/zipf/
-rw-r--r--  0 standage staff     317 20 Aug 13:34 zipf-0.1/zipf/__init__.py
-rw-r--r--  0 standage staff     163 20 Aug 13:34 zipf-0.1/zipf/generate.py
drwxr-xr-x  0 standage staff       0 20 Aug 15:36 zipf-0.1/zipf.egg-info/
-rw-r--r--  0 standage staff       1 20 Aug 15:36 zipf-0.1/zipf.egg-info/dependency_links.txt
-rw-r--r--  0 standage staff     180 20 Aug 15:36 zipf-0.1/zipf.egg-info/PKG-INFO
-rw-r--r--  0 standage staff     154 20 Aug 15:36 zipf-0.1/zipf.egg-info/SOURCES.txt
-rw-r--r--  0 standage staff       5 20 Aug 15:36 zipf-0.1/zipf.egg-info/top_level.txt
```

-   Next step is to test installation...
-   ...but first we should clean up the warnings about `README.md`, `url`, and `author_email`

## How Can I Manage the Packages My Projects Need? {#s:package-virtualenv}

-   Want to test the package we just created
-   But *don't* want to damage the packages we already have installed
-   And may not have permission to write into the directory that contains system-wide packages
    -   E.g., on a cluster
-   Solution: use a [virtual environment](#g:virtual-environment)
    -   Slowly being superceded by more general solutions like [Docker][docker],
        but still the easiest solution for most of us
-   `pip install virtualenv`
-   `virtualenv test`
    -   Creates a new directory called `test`
    -   That directory contains `bin`, `lib`, and so on
    -   `test/bin/python` checks for packages in `test/lib` *before* checking the system-wide install
-   Switch to the envrionment with `source test/bin/activate`
    -   `source` is a Unix shell command meaning "run all the commands from a file in this currently-active shell"
    -   Just typing `test/bin/activate` on its own would run those commans in a sub-shell
-   Can switch back to default with `deactivate`
-   Common to create `$HOME/envs` to store all environments
-   Note how every command now displays `(test)` when that virtual environment is active

```
$ cd ~
$ mkdir envs

$ which python
/Users/standage/anaconda3/bin/python

$ virtualenv envs/test
Using base prefix '/Users/standage/anaconda3'
New python executable in /Users/standage/envs/test/bin/python
Installing setuptools, pip, wheel...done.

$ which python
/Users/standage/anaconda3/bin/python

$ source envs/test/bin/activate
(test) 

$ which python
/Users/standage/envs/test/bin/python
(test)

$ deactivate

$ which python
/Users/standage/anaconda3/bin/python
```

-   Now test installation

```
$ pip install ./src/package/05/dist/zipf-0.1.tar.gz 
Processing ./src/package/05/dist/zipf-0.1.tar.gz
Building wheels for collected packages: zipf
  Running setup.py bdist_wheel for zipf ... done
  Stored in directory: /Users/stanage/Library/Caches/pip/wheels/6b/de/80/d72bb0d6e7c65b6e413f0cf10f04b4bbccb329767853fe1644
Successfully built zipf
Installing collected packages: zipf
Successfully installed zipf-0.1
(test)

$ python
>>> import zipf
>>> zipf.RELATIVE_ERROR
0.05

$ pip uninstall zipf
Uninstalling zipf-0.1:
  Would remove:
    /Users/standage/envs/test/lib/python3.6/site-packages/zipf-0.1.dist-info/*
    /Users/standage/envs/test/lib/python3.6/site-packages/zipf/*
Proceed (y/n)? y
  Successfully uninstalled zipf-0.1
(test)
```

-   One environment per project, one project per environment
-   Uses more disk space than absolutely necessary...
-   ...but less than most of your data sets...
-   ...and saves a *lot* of pain

## Summary {#s:package-summary}

FIXME: create concept map for packages

{% include links.md %}
