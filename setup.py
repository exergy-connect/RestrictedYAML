"""
Setup script for Deterministic YAML CLI tool.

Copyright (c) 2025 Exergy ∞ LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='deterministic-yaml',
    version='1.0.0',
    description='Deterministic YAML CLI tool for CI/CD pipelines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Exergy ∞ LLC',
    author_email='',
    url='https://github.com/exergy-connect/DeterministicYAML',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.10',
    install_requires=[
        'click>=8.1.0',          # CLI framework
        'ruamel.yaml>=0.18.0',   # YAML parsing with comment preservation
        'rich>=13.0.0',          # Terminal output formatting
        'pyyaml>=6.0.2',         # YAML parsing (fallback when ruamel unavailable)
    ],
    entry_points={
        'console_scripts': [
            'dyaml=dyaml.__main__:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
    ],
    keywords='yaml deterministic ci-cd llm',
)

