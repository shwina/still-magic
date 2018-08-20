---
permalink: "/en/logging/"
title: "Logging"
questions:
-   "How should I keep track of what I actually did?"
-   "How can I get my software to report errors?"
objectives:
-   "Explain the advantages of using a logging library rather than `print` statements in data science pipelines."
-   "Describe the intent of the five standard logging levels."
-   "Create and configure a simple logger."
-   "Define a custom format for log messages."
-   "Define a source name to use in consolidated logs."
keypoints:
-   "Use `logging` instead of `print` to report program activity."
-   "Separate  messages into `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL` levels."
-   "Use `logging.basicConfig` to define basic logging parameters."
-   "Always provide timestamps using YYYY-MM-DDTHH:MM:SS format."
-   "Use standard input and standard output for normal input and output, and send log messages to a file."
-   "Use `tail -f` to monitor log files."
---

-   Programs should report things that go wrong
    -   And optionally things that go right, to help track down the sources of errors
-   Adding `print` statements during debugging is a common approach
    -   But removing or commenting out, only to add them again, is tedious
    -   Especially when the software is in production
-   Instead, using the `logging` library
    -   Leave statements in
    -   Enable or disable in standard ways
    -   Send output to any of several places for collation and inspection

## Basic Usage {#s:logging-basic}

-   Standard levels (each more verbose than the next)
    -   `DEBUG`: very detailed information used for localizing errors
    -   `INFO`: confirmation that things are working as expected
    -   `WARNING`: something unexpected happened, but the program will keep going
    -   `ERROR`: something has gone badly wrong, but the program hasn't hurt anything
    -   `CRITICAL`: potential loss of data, security breach, etc.
-   Use `logging.debug`, `logging.info`, etc. to write messages at these levels
    -   By default, only `WARNING` and above are displayed
-   Messages appear on standard error so that flow of data in pipes (standard input to standard output) isn't affected
-   The source appears as well (in this case, called "root")

```python
import logging

logging.warning('This is a warning.')
logging.info('This is just for information.')
```
```stderr
WARNING:root:This is a warning.
```

-   Can configure logging to send messages to a file instead of to standard error
    -   Do this before any calls: it's not retroactive
-   And change the level
    -   Everything at or above the configured level is displayed

```python
logging.basicConfig(level=logging.DEBUG, filename='everything.log')
logging.debug('This is for debugging.')
logging.info('This is just for information.')
logging.warning('This is a warning.')
logging.error('Something went wrong.')
logging.critical('Something went seriously wrong.')
```
```
DEBUG:root:This is for debugging.
INFO:root:This is just for information.
WARNING:root:This is a warning.
ERROR:root:Something went wrong.
CRITICAL:root:Something went seriously wrong.
```

-   By default, `basicConfig` re-opens the file in append mode
-   Use `filemode='w'` to overwrite the existing log data
    -   Useful during debugging
    -   Think twice before doing in production

## Changing Format {#s:logging-format}

-   Library uses the conventions of an older form of string formatting
    -   `%(NAME)s` to insert a named value as a string
    -   `asctime` to get the current time
    -   `message` to get the message

```python
logging.basicConfig(format='%(asctime)s,%(levelname)s,%(message)s', datefmt='%Y-%m-%d')
logging.warning('This is a warning.')
```
```
2018-08-18,WARNING,This is a warning.
```

-   This looks like readable CSV data (on purpose)
    -   Call the log file `log.csv` and record everything needed to re-create the run
-   As noted in [s:config](#CHAPTER), record the configuration data as a single string
    -   Because CSV doesn't handle nested data...
    -   ...and you want to be able to read a single field, convert from YAML back to memory, and manipulate

## Handling Multiple Sources {#s:logging-source}

-   Can configure multiple loggers to write to the same output with different source names.
-   Again, reserve `stdin` and `stdout` for normal pipe operations

```python
# util.py
import logging

def create_logger(application, filename):

    # Create logger.
    logger = logging.getLogger(application)
    logger.setLevel(logging.WARNING)

    # Send messages to standard output.
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)

    # Define format.
    formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')

    # Stitch everything together.
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```
``python
# get_words.py
from util import create_logger

logger = create_logger('get_words', 'log.csv')

for word in ['first', 'second', 'third']:
    print(word)
    logger.debug('debug message')
    logger.warn('warn message')
    logger.critical('critical message')
```
```python
# count_words.py
import sys
from util import create_logger

logger = create_logger('count_words', 'log.csv')

count = 0
for line in sys.stdin:
    count += 1
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
print(count)
```
```
$ get_words.py | count_words.py
3
```
```
2018-08-18T17:31:01,get_words,WARNING,warn message
2018-08-18T17:31:01,get_words,CRITICAL,critical message
2018-08-18T17:31:01,get_words,WARNING,warn message
2018-08-18T17:31:01,get_words,CRITICAL,critical message
2018-08-18T17:31:01,get_words,WARNING,warn message
2018-08-18T17:31:01,get_words,CRITICAL,critical message
2018-08-18T17:31:01,count_words,WARNING,warn message
2018-08-18T17:31:01,count_words,ERROR,error message
2018-08-18T17:31:01,count_words,WARNING,warn message
2018-08-18T17:31:01,count_words,ERROR,error message
2018-08-18T17:31:01,count_words,WARNING,warn message
2018-08-18T17:31:01,count_words,ERROR,error message
```

-   All messages consolidated in one file for checking
    -   E.g., log the record key of every record put out at INFO level
    -   And then log the number of records aggregated, also at INFO level
    -   Checking tool loads CSV, selects appropriate records, and checks count
-   Many (many) other kinds of handlers
    -   Rotating files
    -   Send messages to HTTP server (i.e., a centralized logging system)
    -   System log
-   You probably don't need any of these
    -   But sys admins will be grateful that you used `logging`, because then they can set it up with very little work
-   Open a second window and use `tail -f log.csv` to monitor progress
-   Common to "tee" the logging
    -   Everything to a file
    -   Errors and critical messages to standard error

```
import sys
import logging

# Create logger.
logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)

# Define common format.
formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')

# Send all logging messages to a file.
toFile = logging.FileHandler('log.csv')
toFile.setLevel(logging.DEBUG)
toFile.setFormatter(formatter)

# Send errors and critical messages to standard error.
toScreen = logging.StreamHandler(sys.stderr)
toScreen.setLevel(logging.ERROR)
toScreen.setFormatter(formatter)

# Stitch everything together.
logger.addHandler(toFile)
logger.addHandler(toScreen)

# Try some messages.
logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')
```
```
$ python tee.py
2018-08-20T16:29:42,example,ERROR,error
2018-08-20T16:29:42,example,CRITICAL,critical
```
```
2018-08-20T16:29:42,example,DEBUG,debug
2018-08-20T16:29:42,example,INFO,info
2018-08-20T16:29:42,example,WARNING,warning
2018-08-20T16:29:42,example,ERROR,error
2018-08-20T16:29:42,example,CRITICAL,critical
```

### Exercises

FIXME: exercises

{% include links.md %}
