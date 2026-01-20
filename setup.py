#!/usr/bin/env python3
"""
Setup script for Pig3on
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="pig3on",
    version="1.0.0",
    description="P2P File Transfer System for WiFi and Bluetooth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/Murali47k/pig3on",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pig3on=pig3on:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: File Sharing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="file-transfer p2p wifi bluetooth sharing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pig3on/issues",
        "Source": "https://github.com/yourusername/pig3on",
    },
)