# -*- coding: utf-8 -*-

from setuptools import setup

DESCRIPTION = """
This django app intended for writing HTTP log to database
and/or watch last user activity.

Features:
  - DB router for writing logs to another database.
  - Filters for ignoring some queries by URL, HTTP methods and response codes.
  - Saving anonymous activity as fake user.

More: https://github.com/scailer/django-user-activity-log
"""

setup(
    name='django-user-activity-log',
    version='0.0.16',
    author='JP Jorissen (forked from Dmitriy Vlasov\'s version)',
    author_email='jjorissen52@gmail.com',

    include_package_data=True,
    packages=[
        'activity_log',
        'activity_log.migrations',
        'activity_log.management',
        'activity_log.management.commands',
    ],

    url='https://github.com/scailer/django-user-activity-log/',
    license='MIT license',
    description='HTTP queries logger with flexible filters.',
    long_description=DESCRIPTION,

    install_requires=[
    ],

    classifiers=(
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)
