"""
Tests for CRC32 checksum functionality.

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
from dyaml.core.crc32 import calculate_crc32, add_crc32, extract_crc32, validate_crc32
from dyaml.core.converter import add_crc32_to_human_fields
from dyaml.core.validator import validate_string
from dyaml.core.parser import parse_yaml_string_with_comments
from dyaml.core.converter import convert_yaml_to_deterministic
from dyaml.core.serializer import to_deterministic_yaml


def test_calculate_crc32():
    """Test CRC32 calculation."""
    text = "Test comment"
    crc = calculate_crc32(text)
    
    # CRC32 should be base64-encoded string
    assert isinstance(crc, str)
    assert len(crc) > 0
    # Should be deterministic
    assert calculate_crc32(text) == crc


def test_calculate_crc32_deterministic():
    """Test that CRC32 calculation is deterministic."""
    text = "Same text"
    crc1 = calculate_crc32(text)
    crc2 = calculate_crc32(text)
    
    assert crc1 == crc2


def test_add_crc32():
    """Test adding CRC32 marker to value."""
    value = "Test comment"
    result = add_crc32(value)
    
    assert result.startswith(value)
    assert "[crc32:" in result
    assert result.endswith("]")
    # Should extract the CRC32 correctly
    crc_value, content = extract_crc32(result)
    assert crc_value is not None
    assert content == value


def test_add_crc32_replaces_existing():
    """Test that adding CRC32 replaces existing marker."""
    value = "Test comment[crc32:OLD]"
    result = add_crc32(value)
    
    # Should have new CRC32, not old one
    assert "[crc32:OLD]" not in result
    assert "[crc32:" in result
    # Content should be preserved
    crc_value, content = extract_crc32(result)
    assert content == "Test comment"


def test_extract_crc32():
    """Test extracting CRC32 from value."""
    value = "Test comment[crc32:abc123]"
    crc_value, content = extract_crc32(value)
    
    assert crc_value == "abc123"
    assert content == "Test comment"


def test_extract_crc32_no_marker():
    """Test extracting CRC32 when no marker present."""
    value = "Test comment"
    crc_value, content = extract_crc32(value)
    
    assert crc_value is None
    assert content == value


def test_validate_crc32_valid():
    """Test validating valid CRC32 checksum."""
    value = "Test comment"
    value_with_crc = add_crc32(value)
    
    is_valid, error = validate_crc32(value_with_crc)
    assert is_valid
    assert error is None


def test_validate_crc32_invalid():
    """Test validating invalid CRC32 checksum."""
    value = "Test comment[crc32:INVALID]"
    
    is_valid, error = validate_crc32(value)
    assert not is_valid
    assert error is not None
    assert "mismatch" in error.lower() or "invalid" in error.lower()


def test_validate_crc32_no_marker():
    """Test validating value without CRC32 marker."""
    value = "Test comment"
    
    is_valid, error = validate_crc32(value)
    # No marker means validation passes (CRC32 is optional)
    assert is_valid
    assert error is None


def test_add_crc32_to_human_fields():
    """Test adding CRC32 to $human$ fields in data structure."""
    data = {
        '$human$': 'Test comment',
        'name': 'John',
        'config': {
            '$human$': 'Config comment',
            'timeout': 30
        }
    }
    
    result = add_crc32_to_human_fields(data)
    
    # Root $human$ should have CRC32
    assert '[crc32:' in result['$human$']
    assert result['name'] == 'John'
    
    # Nested $human$ should have CRC32
    assert '[crc32:' in result['config']['$human$']
    assert result['config']['timeout'] == 30


def test_convert_with_crc32():
    """Test convert command with CRC32 checksums."""
    yaml_input = """# Comment
name: John
age: 30
"""
    
    data, comments = parse_yaml_string_with_comments(yaml_input)
    deterministic_data = convert_yaml_to_deterministic(data, comments, preserve_comments=True, add_crc32_checksums=True)
    output = to_deterministic_yaml(deterministic_data)
    
    # Should have $human$ field with CRC32
    assert '$human$' in output
    assert '[crc32:' in output
    # Should preserve data
    assert 'name: John' in output
    assert 'age: 30' in output


def test_validate_with_crc32_valid():
    """Test validation with valid CRC32 checksum."""
    from dyaml.core.crc32 import add_crc32
    
    yaml_str = f'''$human$: "{add_crc32("Test comment")}"
name: John
'''
    
    result = validate_string(yaml_str)
    assert result.valid
    assert len(result.errors) == 0


def test_validate_with_crc32_invalid():
    """Test validation with invalid CRC32 checksum."""
    yaml_str = '''$human$: "Test comment[crc32:INVALID]"
name: John
'''
    
    result = validate_string(yaml_str)
    assert not result.valid
    # Should have CRC32 validation error
    crc_errors = [e for e in result.errors if 'crc32' in e.message.lower() or 'mismatch' in e.message.lower()]
    assert len(crc_errors) > 0


def test_validate_without_crc32():
    """Test validation without CRC32 marker (should pass)."""
    yaml_str = '''$human$: "Test comment"
name: John
'''
    
    result = validate_string(yaml_str)
    assert result.valid
    assert len(result.errors) == 0


def test_crc32_with_newlines():
    """Test CRC32 with newline escapes."""
    value = "Line one.\\nLine two.\\nLine three."
    value_with_crc = add_crc32(value)
    
    is_valid, error = validate_crc32(value_with_crc)
    assert is_valid
    assert '[crc32:' in value_with_crc
    # Should extract correctly
    crc_value, content = extract_crc32(value_with_crc)
    assert content == value


def test_crc32_multiple_human_fields():
    """Test CRC32 with multiple nested $human$ fields."""
    data = {
        '$human$': 'Root comment',
        'service': {
            '$human$': 'Service comment',
            'name': 'auth'
        }
    }
    
    result = add_crc32_to_human_fields(data)
    
    # Both should have CRC32
    assert '[crc32:' in result['$human$']
    assert '[crc32:' in result['service']['$human$']
    # Data should be preserved
    assert result['service']['name'] == 'auth'

