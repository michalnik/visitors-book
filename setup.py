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
        "django~=3.2",
        "djangorestframework~=3.12",
        "djangorestframework-simplejwt~=4.8",
        "psycopg2-binary~=2.9",
        "requests~=2.27",
    ],
    extras_require={
        "devel": [
            "ipython~=7.31",
            "rich~=11.0",
            "mock~=4.0",
            "pylint~=2.12",
            "pylint-django~=2.5",
        ]
    }
)
