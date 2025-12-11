"""
Check that all YAML files in netlab tests/integration are compatible with RestrictedYAML.

This script validates that YAML files in the netlab project's tests/integration
directory conform to the Restricted YAML specification.
"""

import os
import yaml
from pathlib import Path
import sys

# Add lib to path to import RestrictedYAML
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from restricted_yaml import RestrictedYAML


def check_file_compatibility(file_path: Path) -> tuple[bool, str, str]:
    """
    Check if a file is compatible with RestrictedYAML.
    
    Returns:
        (is_compatible, message, normalized_yaml)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as YAML
        try:
            data = yaml.safe_load(content)
            if data is None:
                return True, "Empty or null YAML (valid)", content
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}", ""
        
        # Validate against Restricted YAML spec
        is_valid, error = RestrictedYAML.validate(content)
        if not is_valid:
            # Try to normalize
            try:
                normalized = RestrictedYAML.normalize(content)
                return False, f"Not Restricted YAML: {error} (but can be normalized)", normalized
            except Exception as norm_e:
                return False, f"Not Restricted YAML: {error} (normalization failed: {norm_e})", ""
        
        # If valid, try to normalize to see if it's canonical
        try:
            normalized = RestrictedYAML.normalize(content)
            if normalized.strip() == content.strip():
                return True, "Compatible and canonical", normalized
            else:
                return True, "Compatible but not canonical (can be normalized)", normalized
        except Exception as e:
            return True, f"Compatible (normalization warning: {e})", content
    
    except Exception as e:
        return False, f"Error reading file: {e}", ""


def check_netlab_tests():
    """Check all YAML files in netlab tests/integration for RestrictedYAML compatibility."""
    netlab_dir = Path("/home/jeroen/Projects/netlab")
    integration_dir = netlab_dir / "tests" / "integration"
    
    if not integration_dir.exists():
        print(f"Directory {integration_dir} does not exist.")
        return False
    
    print("=" * 80)
    print("CHECKING NETLAB INTEGRATION TESTS FOR RESTRICTED YAML COMPATIBILITY")
    print("=" * 80)
    print()
    
    # Find all YAML files
    yaml_files = list(integration_dir.rglob("*.yaml")) + list(integration_dir.rglob("*.yml"))
    
    if not yaml_files:
        print(f"No YAML files found in {integration_dir}")
        return True
    
    print(f"Found {len(yaml_files)} YAML file(s) to check:\n")
    
    compatible_count = 0
    incompatible_count = 0
    canonical_count = 0
    results = []
    
    for yaml_file in sorted(yaml_files):
        relative_path = yaml_file.relative_to(netlab_dir)
        is_compatible, message, normalized = check_file_compatibility(yaml_file)
        
        status = "✓" if is_compatible else "✗"
        if is_compatible:
            compatible_count += 1
            if "canonical" in message.lower() and "not" not in message.lower():
                canonical_count += 1
        else:
            incompatible_count += 1
        
        results.append((relative_path, is_compatible, message, normalized))
    
    # Print results
    for file_path, is_compatible, message, normalized in results:
        print(f"{status} {file_path}")
        print(f"    {message}")
        if not is_compatible and normalized:
            print(f"    Normalized version available (see below)")
        print()
    
    # Show summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files: {len(yaml_files)}")
    print(f"Compatible: {compatible_count}")
    print(f"Canonical: {canonical_count}")
    print(f"Incompatible: {incompatible_count}")
    print()
    
    if incompatible_count > 0:
        print("INCOMPATIBLE FILES (can be normalized):")
        for file_path, is_compatible, message, normalized in results:
            if not is_compatible and normalized:
                print(f"\n{file_path}:")
                print("  Original issues:", message)
                print("  Normalized Restricted YAML:")
                print("  " + "\n  ".join(normalized.split("\n")[:10]))
                if len(normalized.split("\n")) > 10:
                    print("  ... (truncated)")
    
    print("=" * 80)
    if incompatible_count == 0:
        print("✓ ALL FILES ARE COMPATIBLE WITH RESTRICTED YAML")
    else:
        print(f"✗ {incompatible_count} FILE(S) NEED NORMALIZATION")
        print("\nTo fix incompatible files, use RestrictedYAML.normalize()")
    print("=" * 80)
    
    return incompatible_count == 0


if __name__ == "__main__":
    success = check_netlab_tests()
    sys.exit(0 if success else 1)

