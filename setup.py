#!/usr/bin/env python3
from setuptools import setup

setup(
    name="visitors-book",
    version="0.0.1",
    description="Restaurant visit diary REST API",
    author="Michal Mladek",
    author_email="michal.mladek.78@gmail.com",
    url="https://github.com/michalnik/visitors-book",
    install_requires=[
        "django<3.3",
        "djangorestframework<3.13",
        "djangorestframework-simplejwt",
        "psycopg2-binary",
        "requests",
    ],
    extras_require={
        "devel": [
            "coverage~=6.2",
            "ipython~=7.31",
            "rich~=11.0",
            "mock~=4.0",
            "pylint~=2.12",
            "pylint-django~=2.5",
        ]
    }
)
