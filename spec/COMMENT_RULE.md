# Formal Rule: Comments in Deterministic YAML

## Rule Statement

**Comments are explicitly forbidden in Deterministic YAML.**

The YAML comment syntax (`#`) is not part of the Deterministic YAML grammar and may not appear in Deterministic YAML documents except as part of a quoted string value.

## Formal Definition

### Prohibition

The `#` character is **not** a valid token in Deterministic YAML grammar, except when it appears inside a double-quoted string value.

**Forbidden forms:**
- Line comments: `# This is a comment`
- Inline comments: `key: value  # comment`
- Block comments: Multiple consecutive `#` lines
- Any occurrence of `#` outside quoted strings

### Grammar Exclusion

In the formal grammar (BNF/GBNF), comments are explicitly excluded:

```
# Comments are not part of the grammar
# The '#' character is not defined as a production rule
# There is no COMMENT ::= "#" ... rule
```

The grammar defines only:
- Mappings (key-value pairs)
- Lists (sequences)
- Scalars (values)
- Whitespace and indentation

**Comments are not a production rule.**

## Sanctioned Alternative: `$human$` Fields

When documentation is needed, use a `$human$` key-value pair:

```yaml
$human$: "This is documentation"
name: John
age: 30
```

### Rules for `$human$` Fields

1. **Key**: Must be exactly `$human$` (dollar signs indicate human-authored context)
2. **Value**: Must be a quoted string (since it typically contains spaces/punctuation), or a structured object
3. **Position**: `$human$` keys always appear **first** within their parent object
4. **Single field**: Only one `$human$` field per object is allowed (use structured value if multiple annotations needed)
5. **Nested**: `$human$` can appear at any nesting level
6. **Empty values**: Empty `$human$` values are stripped during normalization

### Examples

**Simple comment:**
```yaml
$human$: "User profile"
name: John
age: 30
```

**Nested comments:**
```yaml
$human$: "Main configuration"
config:
  $human$: "Database settings"
  host: localhost
  port: 5432
```

**Structured `$human$` value** (for multiple annotations):
```yaml
$human$:
  comment: "Updated connection limits"
  author: "alice@example.com"
  date: "2024-03-15"
connection_pool:
  min_size: 10
  max_size: 100
```

## Rationale

### Philosophy: To Comment is Human

**Comments are human insight that must be preserved, not ignored.** They represent valuable context, explanations, and documentation that should survive all data operations.

### Why Forbid YAML Comments (`#`)?

1. **Lost during processing**: YAML comments are metadata that gets discarded during:
   - Round-trip parsing (most parsers ignore comments)
   - Normalization (comments stripped)
   - Regeneration (comments not preserved)
   - Data transformation (comments vanish)

2. **Variance**: Same logical data can have different comments
   ```yaml
   # Version 1
   name: John
   
   # Version 2 (different comment, same data)
   name: John  # User name
   ```

3. **Non-deterministic**: Comments break canonical representation
   - Same data → different YAML (due to comments)
   - Breaks determinism requirement

4. **LLM Entropy**: Comments create branching points
   - Model must decide: include comment? What comment?
   - Increases output variance

5. **Parsing Ambiguity**: Comments can be ambiguous
   - Inline comments: `key: value # comment` - is `#` part of value?
   - Whitespace sensitivity

### Why `$human$` Fields?

**Comments matter — enough that they need to be handled deterministically, not thrown away.**

1. **Semantically clear**: Instantly communicates "this is human-authored context"
2. **Preserved as data**: Comments are part of the data structure, ensuring they survive all operations
3. **Deterministic**: Same data → same YAML (comments included)
4. **Round-trip safe**: Comments survive regeneration, normalization, and any YAML parser
5. **Always first**: `$human$` appears first in each object, making human context immediately visible
6. **Explicit**: Clear, unambiguous syntax
7. **LLM-friendly**: No ambiguity about where/how to include documentation
8. **Human insight preserved**: The human touch of comments is maintained, not discarded
9. **Machine-readable signal**: LLMs can learn to recognize and preserve this pattern
10. **Namespace safety**: Extremely unlikely to collide with real field names

## Validation

A Deterministic YAML validator must:

1. **Reject** any occurrence of `#` outside quoted strings
2. **Accept** `$human$` fields as regular key-value pairs (but only one per object)
3. **Report** line numbers where `#` appears
4. **Verify** that `$human$` appears first in each object (if present)

### Validation Example

```python
from lib.deterministic_yaml import DeterministicYAML

yaml_text = """
# This is a comment (INVALID)
name: John
age: 30  # inline comment (INVALID)
"""

is_valid, error = DeterministicYAML.validate(yaml_text)
# Returns: (False, "Line 2: Comments not allowed; Line 3: Comments not allowed")
```

## GBNF Grammar Reflection

The GBNF grammar (`deterministic_yaml.gbnf`) explicitly excludes comments:

- No `COMMENT` production rule
- No `#` token definition
- Grammar only defines: mappings, lists, scalars, whitespace

The grammar comment section states:
```
# Comments are EXPLICITLY FORBIDDEN
# The '#' character is not part of this grammar.
# Use $human$ key-value pairs for documentation instead.
```

## Implementation

### Parser Behavior

A Deterministic YAML parser must:
- **Reject** input containing `#` outside quoted strings
- **Accept** `$human$` as a valid key (always appears first in each object)
- **Report** validation errors with line numbers

### Normalizer Behavior

A Deterministic YAML normalizer must:
- **Remove** all comments (lines starting with `#`, inline `# comment`)
- **Preserve** data structure
- **Convert** comments to `$human$` fields (preserving human insight as data)
- **Strip** empty `$human$` values

## Summary

| Aspect | Standard YAML | Deterministic YAML |
|--------|---------------|-----------------|
| Comments | Allowed (`#`) | **Forbidden** |
| Documentation | Comments | `$human$` fields |
| Determinism | Low (comments vary) | High (comments are data) |
| LLM-friendly | No (ambiguous) | Yes (explicit) |

**Formal Rule**: `#` is not a valid token in Deterministic YAML grammar. Use `$human$: "documentation"` for documentation needs.

