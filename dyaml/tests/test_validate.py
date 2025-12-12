"""
Tests for dyaml validate command.

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

import pytest
from dyaml.core.validator import validate_string, ValidationResult


def test_validate_accepts_correct_dyaml():
    """Test that valid Deterministic YAML passes validation."""
    valid_yaml = """name: John
age: 30
active: true
"""
    
    result = validate_string(valid_yaml)
    assert result.valid
    assert len(result.errors) == 0


def test_validate_rejects_comments():
    """Test that YAML with comments is rejected."""
    invalid_yaml = """# Comment
name: John
age: 30
"""
    
    result = validate_string(invalid_yaml)
    assert not result.valid
    # Should have specific error about comments on line 1
    comment_errors = [e for e in result.errors if 'comment' in e.message.lower()]
    assert len(comment_errors) > 0 and any(e.line == 1 for e in comment_errors), "Should have comment-related error on line 1"


def test_validate_rejects_flow_style():
    """Test that flow style is rejected."""
    invalid_yaml = """config: {key: value}
"""
    
    result = validate_string(invalid_yaml)
    # Flow style should be rejected
    assert not result.valid
    # Should have error about flow style
    flow_errors = [e for e in result.errors if 'flow' in e.message.lower()]
    assert len(flow_errors) > 0, "Should have flow style error"


def test_validate_checks_indentation():
    """Test that tabs are rejected."""
    invalid_yaml = """name:\tJohn
age: 30
"""
    
    result = validate_string(invalid_yaml)
    assert not result.valid
    # Should have specific error about tabs
    tab_errors = [e for e in result.errors if 'tab' in e.message.lower()]
    assert len(tab_errors) > 0, "Should have tab-related error"
    # Error should be on line 1 where the tab is
    assert any(e.line == 1 for e in tab_errors), "Tab error should be on line 1"

