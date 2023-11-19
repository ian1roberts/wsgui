"""wssgui package setup module"""
from setuptools import find_packages, setup

config = {
    "version": "0.1.0",
    "name": "wssgui",
    "description": "<MODULE_DESCRIPTION>",
    "url": "",
    "author": "Ian Roberts",
    "author_email": "ian.roberts@cantab.net",
    "packages": find_packages(
        include=[
            "wssgui",
            "wssgui.*",
        ]
    )
}

setup(**config)
