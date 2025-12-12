"""
CLI entry point for dyaml tool.

This allows running: python -m dyaml <command>
Or after installation: dyaml <command>

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

import sys
import click
from pathlib import Path

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))

from .cli.convert import convert
from .cli.validate import validate
from .cli.normalize import normalize
from .cli.diff import diff
from .cli.check_drift import check_drift


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Deterministic YAML CLI Tool
    
    A production-ready CLI for converting, validating, and normalizing
    Deterministic YAML files in CI/CD pipelines.
    """
    pass


# Register all commands
cli.add_command(convert)
cli.add_command(validate)
cli.add_command(normalize)
cli.add_command(diff)
cli.add_command(check_drift)


if __name__ == '__main__':
    cli()

