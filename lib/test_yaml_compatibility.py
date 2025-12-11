"""
Test that Restricted YAML is valid YAML.

Restricted YAML is a subset of standard YAML, so any YAML parser
should be able to parse it correctly.
"""

import yaml
from restricted_yaml import RestrictedYAML
from restricted_yaml_parser import parse_restricted_yaml


def test_yaml_compatibility():
    """Test that Restricted YAML can be parsed by standard YAML parsers."""
    print("=" * 80)
    print("YAML COMPATIBILITY TEST")
    print("=" * 80)
    print("\nTesting that Restricted YAML is valid YAML (parsable by PyYAML)...\n")
    
    test_cases = [
        {
            'name': 'Simple mapping',
            'data': {'name': 'John', 'age': 30, 'active': True}
        },
        {
            'name': 'Nested mapping',
            'data': {
                'config': {
                    'host': 'localhost',
                    'port': 5432
                }
            }
        },
        {
            'name': 'List',
            'data': {'tags': ['dev', 'ops', 'important']}
        },
        {
            'name': 'Mixed structure',
            'data': {
                'name': 'John',
                'age': 30,
                'active': True,
                'tags': ['important', 'urgent'],
                'config': {
                    'host': 'localhost',
                    'port': 5432
                }
            }
        },
        {
            'name': 'With quoted strings',
            'data': {
                'description': 'A string with spaces',
                'path': '/usr/local/bin',
                'empty': ''
            }
        },
        {
            'name': 'With null and booleans',
            'data': {
                'value': None,
                'active': True,
                'inactive': False
            }
        },
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        data = test_case['data']
        
        # Generate Restricted YAML
        restricted_yaml = RestrictedYAML.to_restricted_yaml(data)
        
        print(f"  Restricted YAML:")
        print(f"  {restricted_yaml.replace(chr(10), chr(10) + '  ')}")
        
        # Try to parse with PyYAML
        parsed_by_pyyaml = yaml.safe_load(restricted_yaml)
        print(f"  ✓ Parsed by PyYAML: {parsed_by_pyyaml}")
        
        # Verify data equivalence
        assert parsed_by_pyyaml == data, f"Data mismatch for {test_case['name']}: original={data}, parsed={parsed_by_pyyaml}"
        print(f"  ✓ Data matches original")
        
        # Also test with our custom parser
        parsed_by_custom = parse_restricted_yaml(restricted_yaml)
        assert parsed_by_custom == data, f"Custom parser mismatch for {test_case['name']}: original={data}, parsed={parsed_by_custom}"
        print(f"  ✓ Parsed by custom parser: matches")
        
        print()
    
    print("=" * 80)
    print("✓ ALL TESTS PASSED")
    print("\nRestricted YAML is fully compatible with standard YAML parsers!")
    print("=" * 80)


def test_round_trip():
    """Test round-trip: data -> Restricted YAML -> parse -> same data."""
    print("\n" + "=" * 80)
    print("ROUND-TRIP TEST")
    print("=" * 80)
    print("\nTesting round-trip through Restricted YAML...\n")
    
    test_data = {
        'name': 'John',
        'age': 30,
        'active': True,
        'tags': ['dev', 'ops'],
        'config': {
            'host': 'localhost',
            'port': 5432
        }
    }
    
    # Generate Restricted YAML
    restricted_yaml = RestrictedYAML.to_restricted_yaml(test_data)
    print("Restricted YAML:")
    print(restricted_yaml)
    print()
    
    # Parse with PyYAML
    parsed_pyyaml = yaml.safe_load(restricted_yaml)
    print(f"Parsed by PyYAML: {parsed_pyyaml}")
    print(f"Matches original: {parsed_pyyaml == test_data}")
    assert parsed_pyyaml == test_data, "PyYAML parsed data doesn't match original"
    
    # Parse with custom parser
    parsed_custom = parse_restricted_yaml(restricted_yaml)
    print(f"Parsed by custom parser: {parsed_custom}")
    print(f"Matches original: {parsed_custom == test_data}")
    assert parsed_custom == test_data, "Custom parser parsed data doesn't match original"
    
    # Round-trip: parse and regenerate
    regenerated = RestrictedYAML.to_restricted_yaml(parsed_pyyaml)
    print(f"\nRegenerated Restricted YAML:")
    print(regenerated)
    print(f"Matches original YAML: {regenerated == restricted_yaml}")
    assert regenerated == restricted_yaml, "Regenerated YAML doesn't match original"


if __name__ == "__main__":
    test_yaml_compatibility()
    test_round_trip()

