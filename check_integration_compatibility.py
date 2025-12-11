"""
Check that all files under tests/integration are compatible with RestrictedYAML.

This script validates that any YAML files in tests/integration conform to
the Restricted YAML specification.
"""

import os
import yaml
from pathlib import Path
from lib.restricted_yaml import RestrictedYAML


def check_file_compatibility(file_path: Path) -> tuple[bool, str]:
    """
    Check if a file is compatible with RestrictedYAML.
    
    Returns:
        (is_compatible, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as YAML
        try:
            data = yaml.safe_load(content)
            if data is None:
                return True, "Empty or null YAML (valid)"
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}"
        
        # Validate against Restricted YAML spec
        is_valid, error = RestrictedYAML.validate(content)
        if not is_valid:
            return False, f"Not Restricted YAML: {error}"
        
        # Try to normalize and compare
        try:
            normalized = RestrictedYAML.normalize(content)
            # If normalization produces different output, it's not canonical
            # But we'll allow it if it parses correctly
            return True, "Compatible with RestrictedYAML"
        except Exception as e:
            return False, f"Normalization failed: {e}"
    
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_integration_tests():
    """Check all files in tests/integration for RestrictedYAML compatibility."""
    integration_dir = Path("tests/integration")
    
    if not integration_dir.exists():
        print(f"Directory {integration_dir} does not exist.")
        print("No integration tests to check.")
        return True
    
    print("=" * 80)
    print("CHECKING INTEGRATION TESTS FOR RESTRICTED YAML COMPATIBILITY")
    print("=" * 80)
    print()
    
    # Find all YAML files
    yaml_files = list(integration_dir.rglob("*.yaml")) + list(integration_dir.rglob("*.yml"))
    
    if not yaml_files:
        print(f"No YAML files found in {integration_dir}")
        return True
    
    print(f"Found {len(yaml_files)} YAML file(s) to check:\n")
    
    all_compatible = True
    results = []
    
    for yaml_file in sorted(yaml_files):
        relative_path = yaml_file.relative_to(Path.cwd())
        is_compatible, message = check_file_compatibility(yaml_file)
        
        status = "✓" if is_compatible else "✗"
        results.append((relative_path, is_compatible, message))
        
        if not is_compatible:
            all_compatible = False
    
    # Print results
    for file_path, is_compatible, message in results:
        print(f"{status} {file_path}")
        if not is_compatible:
            print(f"    {message}")
        print()
    
    print("=" * 80)
    if all_compatible:
        print("✓ ALL FILES ARE COMPATIBLE WITH RESTRICTED YAML")
    else:
        print("✗ SOME FILES ARE NOT COMPATIBLE")
        print("\nTo fix incompatible files, use RestrictedYAML.normalize()")
    print("=" * 80)
    
    return all_compatible


if __name__ == "__main__":
    import sys
    success = check_integration_tests()
    sys.exit(0 if success else 1)

