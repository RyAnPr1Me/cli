#!/usr/bin/env python3
"""Setup script for macOS CLI tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="macos-cli-tools",
    version="1.0.0",
    author="RyAnPr1Me",
    description="A powerful macOS compatible user space CLI with useful features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RyAnPr1Me/cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "mcli=mcli.cli:main",
        ],
    },
)
