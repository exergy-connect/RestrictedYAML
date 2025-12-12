"""
JSON Schema validation and encoding instruction processing.

This module handles JSON schema validation and applies custom encoding
instructions to fields (e.g., CRC32, parity check, lowercase conversion).

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

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import jsonschema
from jsonschema.validators import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
import yaml

from .crc32 import add_crc32, validate_crc32, extract_crc32


class SchemaValidationError(Exception):
    """Error during schema validation."""
    pass


class EncodingInstructionError(Exception):
    """Error applying encoding instructions."""
    pass


def load_schema(schema_path: str) -> Dict[str, Any]:
    """
    Load JSON schema from file.
    
    Args:
        schema_path: Path to schema file (JSON or YAML)
        
    Returns:
        Schema dictionary
    """
    path = Path(schema_path)
    if not path.exists():
        raise SchemaValidationError(f"Schema file not found: {schema_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try JSON first, then YAML
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise SchemaValidationError(f"Invalid schema file format: {e}")


def validate_against_schema(data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate data against JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    try:
        validate(instance=data, schema=schema)
        return True, []
    except JsonSchemaValidationError as e:
        errors = [f"{'.'.join(str(p) for p in e.path)}: {e.message}"]
        # Collect all errors
        for error in e.context:
            errors.append(f"{'.'.join(str(p) for p in error.path)}: {error.message}")
        return False, errors
    except jsonschema.SchemaError as e:
        return False, [f"Invalid schema: {e.message}"]


def _calculate_parity(value: str) -> int:
    """
    Calculate simple parity bit (even parity).
    
    Args:
        value: String value to calculate parity for
        
    Returns:
        Parity bit (0 or 1)
    """
    # Convert to bytes and count set bits
    byte_count = sum(bin(b).count('1') for b in value.encode('utf-8'))
    return byte_count % 2


def _validate_parity(value: str, expected_parity: int) -> bool:
    """
    Validate parity bit.
    
    Args:
        value: String value to validate
        expected_parity: Expected parity bit (0 or 1)
        
    Returns:
        True if parity matches
    """
    actual_parity = _calculate_parity(value)
    return actual_parity == expected_parity


def _apply_encoding_instruction(
    value: Any,
    instruction: Dict[str, Any],
    path: List[str]
) -> Any:
    """
    Apply a single encoding instruction to a value.
    
    Args:
        value: Value to encode
        instruction: Encoding instruction dictionary
        path: Current path in data structure
        
    Returns:
        Encoded value
    """
    if not isinstance(value, str):
        # Only string values can have encoding instructions
        return value
    
    # Extract existing CRC32 if present
    existing_crc32, content = extract_crc32(value)
    result = content  # Start with content without CRC32
    
    # Apply case transformations first (before CRC32)
    if instruction.get('lowercase', False):
        result = result.lower()
    elif instruction.get('uppercase', False):
        result = result.upper()
    
    # Apply CRC32 after case transformations
    if instruction.get('crc32', False):
        result = add_crc32(result)
    
    # Apply parity check (add parity bit as suffix)
    # Parity is calculated on the final value (including CRC32 if present)
    if instruction.get('parity', False):
        parity_bit = _calculate_parity(result)
        result = f"{result}[parity:{parity_bit}]"
    
    return result


def _get_encoding_instructions(
    schema: Dict[str, Any],
    path: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Get encoding instructions for a field at the given path.
    
    Looks for 'x-encoding' property in schema at the matching path.
    
    Args:
        schema: JSON schema dictionary
        path: Path to field (list of keys)
        
    Returns:
        Encoding instruction dictionary or None
    """
    current = schema
    
    # Navigate to the property in the schema
    for key in path:
        if 'properties' in current:
            if key in current['properties']:
                current = current['properties'][key]
            else:
                return None
        elif 'items' in current:
            # Array item - check if items has properties
            if 'properties' in current.get('items', {}):
                if key in current['items']['properties']:
                    current = current['items']['properties'][key]
                else:
                    return None
            else:
                return None
        else:
            return None
    
    # Check for x-encoding extension
    return current.get('x-encoding')


def apply_encoding_instructions(
    data: Any,
    schema: Dict[str, Any],
    path: Optional[List[str]] = None
) -> Any:
    """
    Recursively apply encoding instructions from schema to data.
    
    Args:
        data: Data structure to encode
        schema: JSON schema with x-encoding instructions
        path: Current path in data structure
        
    Returns:
        Data structure with encoding instructions applied
    """
    if path is None:
        path = []
    
    # Get encoding instructions for current path
    encoding = _get_encoding_instructions(schema, path)
    
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            key_path = path + [str(key)]
            # Recursively process nested structures
            result[key] = apply_encoding_instructions(value, schema, key_path)
        return result
    elif isinstance(data, list):
        result = []
        for i, item in enumerate(data):
            item_path = path + [str(i)]
            result.append(apply_encoding_instructions(item, schema, item_path))
        return result
    else:
        # Scalar value - apply encoding if instruction exists
        if encoding:
            return _apply_encoding_instruction(data, encoding, path)
        return data


def validate_encoding_instructions(
    data: Any,
    schema: Dict[str, Any],
    path: Optional[List[str]] = None,
    errors: Optional[List[str]] = None
) -> List[str]:
    """
    Validate that encoding instructions are correctly applied.
    
    Args:
        data: Data structure to validate
        schema: JSON schema with x-encoding instructions
        path: Current path in data structure
        errors: List to accumulate errors
        
    Returns:
        List of validation errors
    """
    if errors is None:
        errors = []
    if path is None:
        path = []
    
    # Get encoding instructions for current path
    encoding = _get_encoding_instructions(schema, path)
    
    if isinstance(data, dict):
        for key, value in data.items():
            key_path = path + [str(key)]
            validate_encoding_instructions(value, schema, key_path, errors)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            item_path = path + [str(i)]
            validate_encoding_instructions(item, schema, item_path, errors)
    else:
        # Scalar value - validate encoding
        if encoding and isinstance(data, str):
            # Validate CRC32
            if encoding.get('crc32', False):
                is_valid, error_msg = validate_crc32(data)
                if not is_valid:
                    path_str = '.'.join(path) if path else 'root'
                    errors.append(f"{path_str}: CRC32 validation failed: {error_msg}")
            
            # Validate parity
            if encoding.get('parity', False):
                # Extract parity bit from value (parity comes after CRC32 if both are present)
                if '[parity:' in data:
                    try:
                        # Find the parity marker (should be at the end)
                        parity_start = data.rfind('[parity:')
                        if parity_start >= 0:
                            parity_str = data[parity_start + 8:].split(']')[0]
                            expected_parity = int(parity_str)
                            # Content is everything before the parity marker
                            content = data[:parity_start]
                            if not _validate_parity(content, expected_parity):
                                path_str = '.'.join(path) if path else 'root'
                                errors.append(f"{path_str}: Parity check failed")
                        else:
                            path_str = '.'.join(path) if path else 'root'
                            errors.append(f"{path_str}: Invalid parity format")
                    except (ValueError, IndexError):
                        path_str = '.'.join(path) if path else 'root'
                        errors.append(f"{path_str}: Invalid parity format")
                else:
                    path_str = '.'.join(path) if path else 'root'
                    errors.append(f"{path_str}: Missing parity check")
    
    return errors

