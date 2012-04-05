"""Use this to output (cumulatively) text at the bottom of the HTML page.
NOTE: This module is for convenience only and uses pyjamas.logging, a ported
version of Python's logging module. You can use Pyjamas' logging directly as
you would with Python, at your option."""

from pyjamas import logging

__logger = logging.getAppendLogger(__name__, logging.DEBUG, '%(message)s')

def setLogger(logger):
    """
    Replace the logger currently in use by a new one, e.g.
    log.setLogger(logging.getXxxxLogger()) ... Xxxx = Alert, Append, Console
    """
    global __logger
    __logger = logger

def debug(msg, *args, **kwargs):
    __logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    __logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    __logger.warning(msg, *args, **kwargs)

warn = warning

def error(msg, *args, **kwargs):
    __logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    __logger.critical(msg, *args, **kwargs)

fatal = critical

def exception(msg, *args):
    __logger.exception(msg, *args)


def write(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    __logger.debug(text)

def writebr(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    write(text + "\n")
