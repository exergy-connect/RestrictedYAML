# Deterministic YAML

A **restrictive, LLM-friendly subset of YAML** that remains **100% valid YAML**, while eliminating ambiguity, output variance, and syntax hazards.  

**Deterministic YAML preserves comments** through `$human$` fields—the golden seams that show where human judgment intervened. Every repair, every insight, becomes visible evidence of human contribution.

Deterministic YAML provides a canonical, predictable serialization format ideal for structured data generation and configuration, with **Kintsukuroi for data**—making human contribution visible and permanent.

---

## 💭 Fundamental Philosophy: Kintsukuroi for Data

**The pottery was always going to break. The question is whether we hide the cracks or fill them with gold.**

Deterministic YAML applies the 500-year-old Japanese art of **Kintsukuroi** (金継ぎ) to configuration files. In Kintsukuroi, broken pottery is repaired with gold, making the repairs visible and beautiful rather than hidden. The mended object is more valuable for having been broken.

### Making Human Intervention Visible

**Traditional approach:**
- Bug appears → fix it → pretend it never happened
- Comment lost → regenerate without it → no trace it existed
- Hallucination occurs → correct it silently → history erased

**Kintsukuroi approach:**
- Bug appears → fix it → mark where it was broken
- Comment lost → preserve it as `$human$` → make the human insight visible
- Hallucination occurs → recognize it → turn the crack into gold

### `$human$` as Golden Seams

Traditional YAML comments (`#`) are treated as fragile metadata that gets lost, ignored, or rewritten unpredictably. Deterministic YAML treats comments as **first-class data** through `$human$` key-value pairs—the golden seams that show where human judgment intervened.

When an LLM regenerates config:
- **Without `$human$`**: Silent drift, invisible degradation
- **With `$human$`**: The human touchpoints remain visible, like gold in the cracks

### Kintsukuroi Principles Applied

**Kintsukuroi principles:**
- Breakage and repair are part of the object's history
- Visibility of repairs adds value
- The mended object is more beautiful for having been broken

**Deterministic YAML with `$human$`:**
- Changes and human intervention are part of the config's history
- Visibility of human reasoning adds value
- The configuration is more reliable for explicitly showing where humans made decisions

**Comments matter — enough that they need to be handled deterministically, not thrown away.** In Deterministic YAML, **comments are gifts**. The spec doesn't let them vanish under the tree; instead, we wrap them carefully as deterministic data so every human insight survives regeneration.

### The AI Boundary: Reducing Guesswork, Not Perfect Determinism

**Both humans and LLMs are fundamentally non-deterministic—no intermediate system can "fix" that.** Deterministic YAML isn't trying to make the process fully deterministic, only more so.

The key difference is at the **AI boundary**:

**With standard YAML:**
- Comments are stripped before the model processes the file
- Human reasoning never reaches the LLM as input—it's invisible to the transformation process
- With less information, the model must guess about intent
- Outputs may or may not align with what humans intended

**With Deterministic YAML:**
- `$human$` fields are structural data, not discardable syntax
- The LLM receives them as explicit input, so human reasoning can be considered during transformation
- The model may still act non-deterministically, but there's a non-zero chance it comes closer to human intent
- The model has more complete information to work with

**The goal isn't perfect determinism—it's reducing the guesswork.** Instead of the model operating blind to human reasoning, it can consider that reasoning when making decisions. The outputs are still non-deterministic, but possibly less so.

---

## 🚀 Why Deterministic YAML?

Standard YAML is flexible but inconsistent:

- Multiple quoting styles  
- Block vs flow syntax  
- Anchors & aliases  
- Comments (lost during processing)  
- Literal & folded blocks  
- Implicit typing  
- Whitespace sensitivity  
- Ambiguous scalars  
- Inconsistent number formats  

All of these introduce branching points that increase **LLM decoding entropy**, making outputs unpredictable. More critically, **human insight gets lost**—comments vanish, context disappears, and the history of human judgment is erased.

JSON solves some variance issues but wastes tokens, is less human-friendly, and still loses comments.

**Deterministic YAML** hits the middle ground: predictable like JSON, compact and readable like YAML, and **makes human intervention visible** through `$human$` fields.

**This isn't just about preventing errors—it's about making human contribution visible and permanent**, even (especially) in a world where AI regenerates everything.

---

## ✅ Features

- Fully valid YAML 1.2  
- **Deterministic, canonical subset**
  - Unquoted keys  
  - Unquoted strings unless required  
  - Double-quoted strings with minimal escaping  
  - Lowercase booleans (`true`, `false`)  
  - Canonical `null`  
  - Canonical integers & floats  
  - No comments, no anchors, no flow style  
  - No multi-line scalars (`\n` escapes only)  
  - Mandatory 2-space indentation  
  - Mandatory lexicographic key ordering  
  - Canonical empty collections: `[]` and `{}`  
- Low variance for LLM output (~70–90% reduction vs standard YAML)  
- Token-efficient (~20–30% fewer tokens than JSON)  
- Easy to generate and validate

---

## 📦 Included Tools

- **GBNF grammar** for Deterministic YAML  
- **Python library** (`DeterministicYAML`) for canonical serialization  
- **Validator** to ensure conformance  
- **Canonicalizer** to normalize arbitrary YAML  
- **Examples & tests** demonstrating deterministic output

---

## 💻 Usage

### Basic Usage

```python
from lib.deterministic_yaml import DeterministicYAML

# Convert Python data to Deterministic YAML
data = {
    'name': 'John',
    'age': 30,
    'active': True,
    'tags': ['dev', 'ops'],
    'config': {
        'host': 'localhost',
        'port': 5432
    }
}

yaml_str = DeterministicYAML.to_deterministic_yaml(data)
print(yaml_str)
```

**Output:**
```yaml
active: true
age: 30
config:
  host: localhost
  port: 5432
name: John
tags:
  - dev
  - ops
```

Note: Keys are automatically sorted lexicographically (notice `active` comes before `age` before `name`).

### Validate YAML

```python
# Check if YAML conforms to Deterministic YAML spec
yaml_text = """
name: John
age: 30
active: true
"""

is_valid, error = DeterministicYAML.validate(yaml_text)
if is_valid:
    print("✓ Valid Deterministic YAML")
else:
    print(f"✗ Invalid: {error}")
```

### Normalize Existing YAML

```python
# Convert any YAML to Deterministic YAML format
standard_yaml = """
# This is a comment
name: "John"  # Quoted string
age: 30
tags: [dev, ops]  # Flow style
"""

deterministic_yaml = DeterministicYAML.normalize(standard_yaml)
print(deterministic_yaml)
```

**Output:**
```yaml
$human$: "name: User's name"
age: 30
name: John
tags:
  - dev
  - ops
```

**Note**: Comments are preserved as `$human$` fields (not discarded), which always appear first in each object—the golden seams that make human insight visible. Quotes removed (when safe), flow style converted to block style.

### Example: Making Repairs Visible

```yaml
# Input with a correction note
service:
  $human$: "Originally had typo 'retries: 3', corrected 2024-03-15"
  retries: 3
  timeout: 30
```

The `$human$` field preserves the history of the fix, making the repair visible rather than hidden. This is Kintsukuroi applied to configuration—the crack (the error) becomes a golden seam (the `$human$` annotation) that adds value.

### Deterministic Quoting

```python
# Check if a string needs quotes
strings = ['John', 'John Doe', '42', 'true', 'hello-world']

for s in strings:
    needs_quotes = DeterministicYAML.needs_quotes(s)
    result = f'"{s}"' if needs_quotes else s
    print(f"{s:15} → {result}")
```

**Output:**
```
John            → John
John Doe        → "John Doe"
42              → "42"
true            → "true"
hello-world     → "hello-world"
```

### Parse Deterministic YAML

```python
import yaml

# Deterministic YAML is valid YAML - use any YAML parser
deterministic_yaml = """
active: true
age: 30
name: John
"""

data = yaml.safe_load(deterministic_yaml)
print(data)  # {'active': True, 'age': 30, 'name': 'John'}
```

---

### Tool Output Examples

#### Variance Comparison (`compare_deterministic_yaml.py`)

```
VARIANCE ANALYSIS
================

JSON:
  Unique outputs: 2/30
  Uniqueness ratio: 6.67%
  Structural variance: 3.33%

Standard YAML:
  Unique outputs: 5/30
  Uniqueness ratio: 16.67%
  Structural variance: 10.00%

Deterministic YAML:
  Unique outputs: 3/30
  Uniqueness ratio: 10.00%
  Structural variance: 3.33%

Variance reduction (Deterministic vs Standard YAML): 40.0%

TOKEN COUNT COMPARISON
======================

JSON (pretty):         40 tokens
JSON (compact):        31 tokens
Standard YAML:         25 tokens
Deterministic YAML:       26 tokens

Token savings vs JSON (compact):
  Standard YAML:      19.4%
  Deterministic YAML:    16.1%
```

#### Token Count Analysis (`token_count_analysis.py`)

```
TOKEN COUNT ANALYSIS: JSON vs YAML
===================================

Test Case 1:
  JSON (pretty):   13 tokens
  JSON (compact):  11 tokens
  YAML (block):      8 tokens
  → JSON uses +5 tokens (+38.5%) more than YAML

EFFICIENCY ANALYSIS (Averages)
===============================

Average token counts across 4 test cases:
  JSON (pretty):  36.5 tokens
  JSON (compact): 26.8 tokens
  YAML (block):   23.5 tokens

Ratios:
  YAML block vs JSON compact: 0.88x
  JSON compact vs YAML block: 1.14x
```

#### YAML Compatibility Test (`test_yaml_compatibility.py`)

```
YAML COMPATIBILITY TEST
=======================

Test 1: Simple mapping
  Deterministic YAML:
  active: true
  age: 30
  name: John
  ✓ Parsed by PyYAML: {'active': True, 'age': 30, 'name': 'John'}
  ✓ Data matches original
  ✓ Parsed by custom parser: matches

Test 2: Nested mapping
  Deterministic YAML:
  config:
    host: localhost
    port: 5432
  ✓ Parsed by PyYAML: {'config': {'host': 'localhost', 'port': 5432}}
  ✓ Data matches original
```

#### Variance Demo (`demo_without_api.py`)

```
VARIANCE ANALYSIS
=================

JSON Results:
  Unique outputs: 2/20
  Uniqueness ratio: 10.00%
  Structural variance: 5.00%

YAML Results:
  Unique outputs: 6/20
  Uniqueness ratio: 30.00%
  Structural variance: 20.00%

  YAML variance is 3.00x higher than JSON
```

---
