from setuptools import setup

setup(
    name = 'present',
    author = 'Alex Telon',
    author_email = 'alex.telon@cybercom.com',
    version = '0.1.0',
    packages = ['present'],
    entry_points = {
        'console_scripts': [
            'present = present.__main__:main'
        ]
    })