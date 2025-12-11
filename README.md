# Restricted YAML

A **deterministic, LLM-friendly subset of YAML** that remains **100% valid YAML**, while eliminating ambiguity, output variance, and syntax hazards.  
Restricted YAML provides a canonical, predictable serialization format ideal for structured data generation and configuration.

---

## 🚀 Why Restricted YAML?

Standard YAML is flexible but inconsistent:

- Multiple quoting styles  
- Block vs flow syntax  
- Anchors & aliases  
- Comments  
- Literal & folded blocks  
- Implicit typing  
- Whitespace sensitivity  
- Ambiguous scalars  
- Inconsistent number formats  

All of these introduce branching points that increase **LLM decoding entropy**, making outputs unpredictable.  

JSON solves some of these issues but wastes tokens and is less human-friendly.  

**Restricted YAML** hits the middle ground: predictable like JSON, compact and readable like YAML.

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

- **GBNF grammar** for Restricted YAML  
- **Python library** (`RestrictedYAML`) for canonical serialization  
- **Validator** to ensure conformance  
- **Canonicalizer** to normalize arbitrary YAML  
- **Examples & tests** demonstrating deterministic output

---
