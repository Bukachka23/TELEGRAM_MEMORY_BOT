"""
Logger Configuration Module for the Telegram AI Translation Bot.

This module sets up and configures the logging system for the bot. It defines custom
filters, formatters, handlers, and loggers to manage log messages effectively.
The logging configuration directs warning and error messages to stderr and debug
messages to stdout, ensuring clear separation of log levels.
"""

import sys
import logging.config


class _ExcludeErrorsFilter(logging.Filter):
    """
    Logging filter to exclude error and warning level logs.

    This filter allows only log records with a level lower than WARNING to pass through.
    It is used to prevent error and warning messages from being duplicated in stdout,
    directing them solely to stderr.
    """
    def filter(self, record):
        """
        Determine if the specified record is to be logged.

        Args:
            record (logging.LogRecord): The log record to be evaluated.

        Returns:
            bool: True if the record's level is below WARNING, False otherwise.
        """
        return record.levelno < logging.WARNING


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(asctime)s: %(filename)s: %(lineno)d:\t %(funcName)s(): %(message)s'
        },
    },
    'handlers': {
        'console_stderr': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'simple',
            'stream': sys.stderr
        },
        'console_stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        },
    },
    'loggers': {
        'asyncio': {
            'level': 'ERROR'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console_stderr', 'console_stdout'],
    },
}


def setup_logging():
    """
    Configure the logging system using the predefined LOGGING dictionary.

    This function applies the logging configuration, setting up formatters,
    handlers, and loggers as specified in the LOGGING dictionary. It ensures
    that log messages are appropriately directed to stdout and stderr based
    on their severity levels.
    """
    logging.config.dictConfig(LOGGING)
