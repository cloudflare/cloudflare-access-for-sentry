#!/usr/bin/env python
"""
sentry-cloudflare-access-auth
==============
An extension for Sentry which authenticates users previously
authenticated through Cloudflare Access.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "sentry>=8.0.0",
    "PyJWT==1.7.*",
    "requests==2.16.*"
]

setuptools.setup(
    name="sentry-cloudflare-access-auth", # Replace with your own username
    version="0.0.1",
    author="Felipe Nascimento",
    author_email="felipe.nascimento1@gmail.com",
    description="An extension for Sentry which authenticates users previously authenticated through Cloudflare Access.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipebn/priv_cloudlare_access_sentry",
    packages=setuptools.find_packages(),
    package_data={'': ['templates/*.html']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.6",
)