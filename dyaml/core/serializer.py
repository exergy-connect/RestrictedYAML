"""
Deterministic YAML serialization.

This module provides serialization of Python data structures to
Deterministic YAML format, ensuring canonical output.

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
from pathlib import Path
from typing import Any

# Add lib directory to path to import existing DeterministicYAML
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))

try:
    from deterministic_yaml import DeterministicYAML
except ImportError:
    # Fallback if not available
    DeterministicYAML = None


def to_deterministic_yaml(data: Any) -> str:
    """
    Serialize Python data structure to Deterministic YAML string.
    
    Args:
        data: Python data structure (dict, list, scalar)
        
    Returns:
        Deterministic YAML string
    """
    if DeterministicYAML:
        return DeterministicYAML.to_deterministic_yaml(data)
    else:
        # Fallback implementation (simplified)
        import yaml
        return yaml.dump(data, sort_keys=True, default_flow_style=False, allow_unicode=True)

