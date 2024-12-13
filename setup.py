from distutils.core import setup

VERSION = '2.0.0'
DESCRIPTION = 'A custom python applications logging handler. Use custom JSON format and sends logs via Telegram Bot Api.'
LONG_DESCRIPTION = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read()


setup(
    name='python-app-logger',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords=['telegram', 'logging'],
    packages=['python_app_logger'],
    url='https://github.com/vfabi/python-app-logger',
    download_url='https://github.com/vfabi/python-app-logger/archive/v%s.zip' % VERSION,
    setup_requires=['wheel'],
    install_requires=[
        'wheel',
        'requests',
        'python-telegram-handler @ git+https://github.com/vfabi/python-telegram-handler.git@1.0.1'
    ],
    dependency_links=[
        "git+https://github.com/vfabi/python-telegram-handler.git@1.0.1"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Logging'
    ],
    license='Apache License',
    author='vfabi',
    author_email='vaad.fabi@gmail.com'
)
