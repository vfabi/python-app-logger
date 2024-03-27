#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
from copy import copy
from telegram_handler.handlers import TelegramHandler
from telegram_handler.formatters import HtmlFormatter
from telegram_handler.utils import escape_html


DEFAULT_LOGLEVEL = 'DEBUG'
DEFAULT_LOGGER_NAME = 'main'


class EMOJI:
    '''
    Note:
        More details and examples at https://www.webfx.com/tools/emoji-cheat-sheet/
    '''

    WHITE_CIRCLE = '⚪'
    GREEN_CIRCLE = '🟢'
    BLUE_CIRCLE = '🔵'
    RED_CIRCLE = '🔴'
    ORANGE_CIRCLE = '🟠'


class CustomHtmlFormatter(HtmlFormatter):
    '''
    Custom HTML formatter for the Telegram.
    '''

    def format(self, record):
        super(HtmlFormatter, self).format(record)

        if record.funcName:
            record.funcName = escape_html(str(record.funcName))
        if record.name:
            record.name = escape_html(str(record.name))
        if record.msg:
            record.msg = escape_html(record.getMessage())
        if self.use_emoji:
            if record.levelno == logging.DEBUG:
                record.levelname = EMOJI.WHITE_CIRCLE + ' ' + record.levelname
            elif record.levelno == logging.INFO:
                record.levelname = EMOJI.GREEN_CIRCLE + ' ' + record.levelname
            elif record.levelno == logging.WARNING:
                record.levelname = EMOJI.ORANGE_CIRCLE + ' ' + record.levelname
            else:
                record.levelname = EMOJI.RED_CIRCLE + ' ' + record.levelname

        if hasattr(self, '_style'):
            return self._style.format(record)
        else:
            # py2.7 branch
            return self._fmt % record.__dict__


class CustomJSONOpensearchFormatter(logging.Formatter):
    '''
    Custom JSON formatter to be compatible with Opensearch index format.

    Note:
        This formatter need to follow custom JSON format for the JSON nested 'message' field, to be always dict type.
        Need for the Opensearch/Elasticsearch correct indexing.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        record = copy(record)
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg)
            return super().format(record)
        if isinstance(record.msg, str):
            log = {
                'message': record.msg
            }
            record.msg = json.dumps(log)
            return super().format(record)


class SeverityFilter(object):

    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level


def get_logger(
        app_name,
        app_version,
        app_environment,
        loglevel=DEFAULT_LOGLEVEL,
        logger_name=DEFAULT_LOGGER_NAME,
        telegram_bot_id=None,
        telegram_chat_ids={}
    ):
    '''
    Args:
        app_name (str): application name.
        app_version (str): application version.
        app_environment (str): application environment.
        loglevel (str): loglevel (severity).
        logger_name (str): logger name.
        telegram_bot_id (str): Telegram bot id.
        telegram_chat_ids (dict): dict with severity - Telegram chat id mapping. Example: {'debug': '1234567890', 'info': '22334455', 'critical': '9988776655'}.
    '''

    logger = logging.getLogger(logger_name)

    # Stream JSON
    handler_json = logging.StreamHandler()
    formatter = CustomJSONOpensearchFormatter('{"app": {"name": "%(app_name)s", "localtime": "%(asctime)s", "environment": "%(app_environment)s", "severity": "%(levelname)s", "message": %(message)s, "version": "%(app_version)s", "logger": "%(name)s", "source": "%(pathname)s:%(funcName)s(%(lineno)d)", "source_pathname": "%(pathname)s", "source_funcname": "%(funcName)s", "source_lineno": "%(lineno)d"}}')
    handler_json.setFormatter(formatter)
    logger.setLevel(loglevel)
    logger.addHandler(handler_json)

    # Telegram
    telegram_formatter = CustomHtmlFormatter(
        use_emoji=True,
        fmt = '<b>%(app_name)s (%(app_version)s)</b>  <b>%(levelname)s</b>\n\n<b>Message:</b> <code>%(message)s</code>\n<b>Environment:</b> %(app_environment)s\n<b>Source:</b> %(pathname)s:%(funcName)s(%(lineno)d)\n<b>Datetime:</b> %(asctime)s\n<b>Logger:</b> %(name)s\n'
    )
    if telegram_bot_id and len(telegram_chat_ids) > 0:
        if telegram_chat_ids.get('critical'):
            handler_telegram_critical = TelegramHandler(level=logging.CRITICAL, token=telegram_bot_id, chat_id=telegram_chat_ids['critical'], message_thread_id='0')
            handler_telegram_critical.setLevel('CRITICAL')
            handler_telegram_critical.addFilter(SeverityFilter(logging.CRITICAL))
            handler_telegram_critical.setFormatter(telegram_formatter)
            logger.addHandler(handler_telegram_critical)
        if telegram_chat_ids.get('warning'):
            handler_telegram_warning = TelegramHandler(level=logging.WARNING, token=telegram_bot_id, chat_id=telegram_chat_ids['warning'], message_thread_id='0')
            handler_telegram_warning.setLevel('WARNING')
            handler_telegram_warning.addFilter(SeverityFilter(logging.WARNING))
            handler_telegram_warning.setFormatter(telegram_formatter)
            logger.addHandler(handler_telegram_warning)
        if telegram_chat_ids.get('info'):
            handler_telegram_info = TelegramHandler(level=logging.INFO, token=telegram_bot_id, chat_id=telegram_chat_ids['info'], message_thread_id='0')
            handler_telegram_info.setLevel('INFO')
            handler_telegram_info.addFilter(SeverityFilter(logging.INFO))
            handler_telegram_info.setFormatter(telegram_formatter)
            logger.addHandler(handler_telegram_info)
        if telegram_chat_ids.get('debug'):
            handler_telegram_debug = TelegramHandler(level=logging.DEBUG, token=telegram_bot_id, chat_id=telegram_chat_ids['debug'], message_thread_id='0')
            handler_telegram_debug.setLevel('DEBUG')
            handler_telegram_debug.addFilter(SeverityFilter(logging.DEBUG))
            handler_telegram_debug.setFormatter(telegram_formatter)
            logger.addHandler(handler_telegram_debug)

    # Extend formatter with additional fields
    logger = logging.LoggerAdapter(
        logger,
        {
            "app_name": app_name,
            "app_version": app_version,
            "app_environment": app_environment
        }
    )

    return logger
