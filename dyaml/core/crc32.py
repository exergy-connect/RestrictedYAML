"""
CRC32 checksum utilities for $human$ field integrity.

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

import zlib
import base64
import re
from typing import Optional, Tuple


CRC32_PATTERN = re.compile(r'\[crc32:([A-Za-z0-9+/=]+)\]$')


def calculate_crc32(text: str) -> str:
    """
    Calculate CRC32 checksum for text and return as base64-encoded string.
    
    Args:
        text: Text to calculate checksum for
        
    Returns:
        Base64-encoded CRC32 checksum (without padding if possible)
    """
    crc = zlib.crc32(text.encode('utf-8')) & 0xffffffff
    # Convert to bytes (4 bytes for CRC32)
    crc_bytes = crc.to_bytes(4, byteorder='big')
    # Encode to base64 and remove padding
    encoded = base64.b64encode(crc_bytes).decode('ascii').rstrip('=')
    return encoded


def extract_crc32(value: str) -> Tuple[Optional[str], str]:
    """
    Extract CRC32 marker from $human$ field value.
    
    Args:
        value: The $human$ field value (may contain CRC32 marker)
        
    Returns:
        Tuple of (crc32_value, content_without_marker)
        If no marker found, returns (None, original_value)
    """
    match = CRC32_PATTERN.search(value)
    if match:
        crc32_value = match.group(1)
        # Remove the marker from the value
        content = value[:match.start()]
        return crc32_value, content
    return None, value


def add_crc32(value: str) -> str:
    """
    Add CRC32 checksum marker to $human$ field value.
    
    If the value already has a CRC32 marker, it is replaced with a new one.
    
    Args:
        value: The $human$ field value
        
    Returns:
        Value with CRC32 marker appended
    """
    # Remove existing CRC32 marker if present
    _, content = extract_crc32(value)
    # Calculate CRC32 for the content
    crc32 = calculate_crc32(content)
    # Append the marker
    return f"{content}[crc32:{crc32}]"


def validate_crc32(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate CRC32 checksum in $human$ field value.
    
    Args:
        value: The $human$ field value (may contain CRC32 marker)
        
    Returns:
        Tuple of (is_valid, error_message)
        If no marker present, returns (True, None) - validation passes
        If marker present and valid, returns (True, None)
        If marker present and invalid, returns (False, error_message)
    """
    crc32_value, content = extract_crc32(value)
    
    if crc32_value is None:
        # No marker present - validation passes (CRC32 is optional)
        return True, None
    
    # Calculate expected CRC32
    expected_crc32 = calculate_crc32(content)
    
    # Compare (handle base64 padding differences)
    # Normalize both by adding padding if needed
    def normalize_base64(s: str) -> str:
        # Add padding if needed
        missing_padding = len(s) % 4
        if missing_padding:
            s += '=' * (4 - missing_padding)
        return s
    
    normalized_expected = normalize_base64(expected_crc32)
    normalized_actual = normalize_base64(crc32_value)
    
    if normalized_expected == normalized_actual:
        return True, None
    else:
        return False, f"CRC32 mismatch: expected {expected_crc32}, got {crc32_value}"

