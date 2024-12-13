#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from telegram_handler.handlers import TelegramHandler
from .utils import SeverityFilter, CustomJSONFormatter, CustomHtmlFormatter, JSONHTTPHandler


DEFAULT_LOGLEVEL = 'DEBUG'
DEFAULT_LOGGER_NAME = 'app'


def get_logger(app_name, app_version=None, app_environment=None, loglevel=DEFAULT_LOGLEVEL, logger_name=DEFAULT_LOGGER_NAME, **channels):
    '''
    Args:
        app_name (str): application name.
        app_version (str): application version. Optional.
        app_environment (str): application environment. Optional.
        loglevel (str): loglevel (severity). For main JSON stream handler. Optional. Possible values: DEBUG,INFO,WARNING,ERROR,CRITICAL.
        logger_name (str): logger name. Optional.
        channels (dict): dict of channels configuration.  Optional. Example:
            {
                'telegram': {
                    'telegram_bot_token': '1234567890:AAEwtYwterrqqq4RhXhl637vvvvvv',
                    'telegram_chat_ids': {
                        'critical':'-1002233445566',
                        'debug':'-2001133445533',
                        'warning':'-300223349900'
                    }
                },
                'webhook': {
                    'url': 'https://webhooks.example.com/webhooks',
                    'loglevel': 'WARNING'  # DEBUG,INFO,WARNING,ERROR,CRITICAL
                }
            }
    '''

    logger = logging.getLogger(logger_name)

    # Formatters
    formatter_json = CustomJSONFormatter('{"app": {"name": "%(app_name)s", "localtime": "%(asctime)s", "environment": "%(app_environment)s", "severity": "%(levelname)s", "message": %(message)s, "version": "%(app_version)s", "logger": "%(name)s", "source": "%(pathname)s:%(funcName)s(%(lineno)d)", "source_pathname": "%(pathname)s", "source_funcname": "%(funcName)s", "source_lineno": "%(lineno)d"}}')
    formatter_telegram = CustomHtmlFormatter(
        use_emoji=True,
        fmt='<b>%(app_name)s (%(app_version)s)</b>  <b>%(levelname)s</b>\n\n<b>Message:</b> <code>%(message)s</code>\n<b>Environment:</b> %(app_environment)s\n<b>Source:</b> %(pathname)s:%(funcName)s(%(lineno)d)\n<b>Datetime:</b> %(asctime)s\n<b>Logger:</b> %(name)s\n'
    )

    # Handler JSON (main)
    handler_json = logging.StreamHandler()
    handler_json.setFormatter(formatter_json)
    handler_json.setLevel(loglevel)
    logger.addHandler(handler_json)

    # Handler Webhook
    if channels.get('webhook'):
        channel = channels['webhook']

        if channel.get('url'):
            handler_webhook = JSONHTTPHandler(url=channel['url'])
            handler_webhook.setFormatter(formatter_json)
            if channel.get('loglevel'):
                # loglevel_webhook = getattr(logging, channel['loglevel'].upper(), None)
                handler_webhook.setLevel(channel['loglevel'])
            else:
                handler_webhook.setLevel(loglevel)
            logger.addHandler(handler_webhook)

    # Handler Telegram
    if channels.get('telegram'):
        channel = channels['telegram']

        if channel.get('telegram_bot_token') and len(channel.get('telegram_chat_ids')) > 0:
            if channel['telegram_chat_ids'].get('critical'):
                handler_telegram_critical = TelegramHandler(level=logging.CRITICAL, token=channel['telegram_bot_token'], chat_id=channel['telegram_chat_ids']['critical'], message_thread_id='0')
                handler_telegram_critical.setFormatter(formatter_telegram)
                handler_telegram_critical.setLevel('CRITICAL')
                handler_telegram_critical.addFilter(SeverityFilter(logging.CRITICAL))
                logger.addHandler(handler_telegram_critical)
            if channel['telegram_chat_ids'].get('error'):
                handler_telegram_error = TelegramHandler(level=logging.ERROR, token=channel['telegram_bot_token'], chat_id=channel['telegram_chat_ids']['error'], message_thread_id='0')
                handler_telegram_error.setFormatter(formatter_telegram)
                handler_telegram_error.setLevel('ERROR')
                handler_telegram_error.addFilter(SeverityFilter(logging.ERROR))
                logger.addHandler(handler_telegram_error)
            if channel['telegram_chat_ids'].get('warning'):
                handler_telegram_warning = TelegramHandler(level=logging.WARNING, token=channel['telegram_bot_token'], chat_id=channel['telegram_chat_ids']['warning'], message_thread_id='0')
                handler_telegram_warning.setFormatter(formatter_telegram)
                handler_telegram_warning.setLevel('WARNING')
                handler_telegram_warning.addFilter(SeverityFilter(logging.WARNING))
                logger.addHandler(handler_telegram_warning)
            if channel['telegram_chat_ids'].get('info'):
                handler_telegram_info = TelegramHandler(level=logging.INFO, token=channel['telegram_bot_token'], chat_id=channel['telegram_chat_ids']['info'], message_thread_id='0')
                handler_telegram_info.setFormatter(formatter_telegram)
                handler_telegram_info.setLevel('INFO')
                handler_telegram_info.addFilter(SeverityFilter(logging.INFO))
                logger.addHandler(handler_telegram_info)
            if channel['telegram_chat_ids'].get('debug'):
                handler_telegram_debug = TelegramHandler(level=logging.DEBUG, token=channel['telegram_bot_token'], chat_id=channel['telegram_chat_ids']['debug'], message_thread_id='0')
                handler_telegram_debug.setFormatter(formatter_telegram)
                handler_telegram_debug.setLevel('DEBUG')
                handler_telegram_debug.addFilter(SeverityFilter(logging.DEBUG))
                logger.addHandler(handler_telegram_debug)

    # Extend formatter with additional fields
    logger_adapter = logging.LoggerAdapter(
        logger,
        {
            "app_name": app_name,
            "app_version": app_version,
            "app_environment": app_environment
        }
    )

    logger_adapter.logger.setLevel(loglevel)

    # DEBUG:  -->
    # print('-----')
    # for handler in logger.handlers:
    #     print(f'Handler: {handler.__class__.__name__} - {logging.getLevelName(handler.level)}')
    # print('-----')
    # DEBUG:  <--

    return logger_adapter
