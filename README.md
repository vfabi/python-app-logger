# python-app-logger

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/vfabi/python-app-logger)
![GitHub last commit](https://img.shields.io/github/last-commit/vfabi/python-app-logger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Python applications custom logging handler. Use custom JSON format and sends logs via Telegram Bot API.

## Status

Production ready

## Features
- Custom JSON stream logging handler
- Custom Telegram logging handler
- Telegram logging handler loglevel (severity) routing

## Usage

### Setup
Just run: `pip install git+https://github.com/vfabi/python-app-logger`

### Application integration
`get_logger()` function arguments:  

Name | Type | Description | Mandatory | Default | Example
--- | --- | --- | --- | --- | ---
app_name | str | application short name | True | | `myapp` |
app_version | str | application version | False | | `1.0.1` |
app_environment | str | application environment | False | | `dev` |
loglevel | str | loglevel (severity) | False | `DEBUG` | Possible values: `DEBUG`,`INFO`,`WARNING`,`ERROR`,`CRITICAL`|
logger_name | str | logger name | False | `main` | `myapp` |
telegram_bot_id | str | Telegram bot id | False | | `1234567890:AAEwtYwterrqqq4RhXhl637vvvvvv` |
telegram_chat_ids | dict | dict with severity - Telegram chat id mapping | False | | `{'debug': '1234567890', 'info': '22334455', 'critical': '9988776655'}` |


Example:

```python
from python_app_logger import get_logger

# Set logger configuration
logger = get_logger(
    app_name='myApp',
    app_version='1.0.1',
    app_environment='dev',
    telegram_bot_id='1234567890:AAEwtYwterrqqq4RhXhl637vvvvvv',
    telegram_chat_ids={
        'critical':'-1002233445566',
        'debug':'-2001133445533',
        'warning':'-300223349900'
    }    
)

# Invoke from application
logger.debug({'message':'DEBUG_MESSAGE', 'submessage':'TEST'})
logger.info('INFO_MESSAGE')
logger.warning('WARNING_MESSAGE')
logger.critical('CRITICAL_MESSAGE')
```

## Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## License
Apache 2.0
