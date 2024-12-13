#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
from copy import copy
import requests
from telegram_handler.formatters import HtmlFormatter
from telegram_handler.utils import escape_html


class EMOJI:
    '''Note: more details and examples at https://www.webfx.com/tools/emoji-cheat-sheet/'''

    WHITE_CIRCLE = '⚪'
    GREEN_CIRCLE = '🟢'
    BLUE_CIRCLE = '🔵'
    YELLOW_CIRCLE = '🟡'
    ORANGE_CIRCLE = '🟠'
    RED_CIRCLE = '🔴'


class SeverityFilter(object):

    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level


class CustomHtmlFormatter(HtmlFormatter):
    '''Custom HTML formatter for the Telegram.'''

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
                record.levelname = EMOJI.YELLOW_CIRCLE + ' ' + record.levelname
            elif record.levelno == logging.ERROR:
                record.levelname = EMOJI.ORANGE_CIRCLE + ' ' + record.levelname
            elif record.levelno == logging.CRITICAL:
                record.levelname = EMOJI.RED_CIRCLE + ' ' + record.levelname
            else:
                record.levelname = EMOJI.BLUE_CIRCLE + ' ' + record.levelname

        if hasattr(self, '_style'):
            return self._style.format(record)
        else:
            # py2.7 branch
            return self._fmt % record.__dict__


class CustomJSONFormatter(logging.Formatter):
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


class JSONHTTPHandler(logging.Handler):
    '''JSON HTTP handler to send records using HTTP/JSON.'''

    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record):
        try:
            log_entry = self.format(record)
            headers = {'Content-Type': 'application/json'}
            requests.post(self.url, data=log_entry, headers=headers, timeout=10)
        except Exception:
            self.handleError(record)
