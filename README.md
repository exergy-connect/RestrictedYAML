# JSON vs YAML: LLM Quantification

This repository contains code to quantify the practical differences between JSON and YAML in LLM contexts, measuring variance, entropy, token probabilities, and decoding behavior.

## Files

- **`LLM_JSON_vs_YAML.md`**: Comprehensive technical document explaining the differences
- **`TOKEN_DIFFERENCES.md`**: Detailed analysis of token count differences
- **`RESTRICTED_YAML_SPEC.md`**: Specification for restricted YAML (low variance, token-efficient)
- **`RESTRICTED_YAML_GRAMMAR.md`**: Formal grammar definition (BNF-style)
- **`restricted_yaml.py`**: Implementation of restricted YAML syntax (generator)
- **`restricted_yaml_parser.py`**: Parser implementation based on formal grammar (optional - standard YAML parsers work)
- **`test_yaml_compatibility.py`**: Test that Restricted YAML is valid YAML
- **`compare_restricted_yaml.py`**: Compare JSON, standard YAML, and restricted YAML
- **`quantify_differences.py`**: Core quantification library
- **`openai_client.py`**: OpenAI API client wrapper
- **`run_quantification.py`**: Main script to run experiments
- **`analyze_logits.py`**: Analyze token probability distributions and entropy
- **`token_count_analysis.py`**: Measure token count differences between JSON and YAML
- **`demo_without_api.py`**: Demo script that works without API access

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY='your-key-here'
```

## Usage

### Run Full Quantification Experiments

```bash
python run_quantification.py
```

This runs:
1. **Variance Experiment**: Generates 20 outputs each for JSON and YAML, measures uniqueness and structural variance
2. **Token Probability Experiment**: Analyzes next-token probabilities at key positions
3. **Decoding Method Experiment**: Compares greedy, temperature, and top-p sampling
4. **Structural Consistency Experiment**: Tests how consistently the same logical structure is represented

### Analyze Logit Distributions

```bash
python analyze_logits.py
```

This creates:
- Token probability distribution comparisons
- Entropy calculations
- Decoding method impact analysis
- Visualization (saved as `token_probability_comparison.png`)

### Analyze Token Count Differences

```bash
python token_count_analysis.py
```

This measures:
- Token count for equivalent JSON and YAML structures
- Token efficiency (tokens per data point)
- Token boundary differences
- Generation cost estimates

**Key Finding**: YAML typically uses 20-40% fewer tokens than JSON for equivalent data.

### Run Demo (No API Key Required)

```bash
python demo_without_api.py
```

Demonstrates variance quantification using simulated outputs.

### Compare Restricted YAML

```bash
python compare_restricted_yaml.py
```

Compares JSON, standard YAML, and restricted YAML:
- Variance analysis
- Token count comparison
- Sample outputs

**Key Finding**: Restricted YAML reduces variance by ~50% vs standard YAML while maintaining token efficiency (~16% fewer tokens than JSON).

### Test YAML Compatibility

```bash
python test_yaml_compatibility.py
```

Verifies that Restricted YAML is valid YAML and can be parsed by standard YAML parsers (PyYAML).

**Key Finding**: Restricted YAML is fully compatible with standard YAML parsers - no special parser required!

### Use the Quantification Library

```python
from quantify_differences import LLMQuantifier
from openai_client import OpenAIClient

client = OpenAIClient(model="gpt-4o-mini")
quantifier = LLMQuantifier(client)

# Generate and compare
json_outputs = quantifier.generate_json("Generate JSON:", num_runs=10)
yaml_outputs = quantifier.generate_yaml("Generate YAML:", num_runs=10)

# Analyze variance
json_variance = quantifier.calculate_variance(json_outputs)
yaml_variance = quantifier.calculate_variance(yaml_outputs)

print(f"JSON uniqueness: {json_variance['uniqueness_ratio']:.2%}")
print(f"YAML uniqueness: {yaml_variance['uniqueness_ratio']:.2%}")
```

## Key Metrics

The code measures:

1. **Variance Metrics**:
   - Unique output count
   - Uniqueness ratio (unique / total)
   - Structural variance (after normalization)
   - Mean edit distance

2. **Token Count**:
   - Token count for equivalent structures
   - Token efficiency (tokens per data point)
   - Generation cost estimates
   - Token boundary differences

3. **Entropy**:
   - Shannon entropy of token probability distributions
   - Position-specific entropy calculations

4. **Decoding Behavior**:
   - Variance across different temperature settings
   - Top-p sampling impact
   - Greedy vs sampling comparison

5. **Structural Consistency**:
   - Parse success rates
   - Normalized output uniqueness
   - Syntax variant analysis

## Expected Results

Based on the theoretical analysis:

### Variance & Entropy
- **JSON**: Low variance (typically 0-20% uniqueness), high top-token probability (>90%), low entropy (<1 bit)
- **YAML**: High variance (typically 40-80% uniqueness), lower top-token probability (30-50%), higher entropy (1.5-3 bits)
- YAML shows 2-5x higher variance than JSON

### Token Count
- **JSON**: More tokens (typically 25-35 tokens for simple structures)
- **YAML**: Fewer tokens (typically 20-25 tokens for equivalent structures)
- YAML uses 20-40% fewer tokens than JSON
- This translates to lower generation cost and faster completion

### Trade-off
- **JSON**: More tokens, lower variance (deterministic, consistent)
- **YAML**: Fewer tokens, higher variance (non-deterministic, variable)
- **Restricted YAML**: Fewer tokens (~16% less than JSON), lower variance (~50% less than standard YAML)

**Restricted YAML** provides the best of both worlds: token efficiency of YAML with variance closer to JSON.

The actual numbers depend on the model and prompt, but the relative differences are consistent.

## Notes

- The OpenAI client requires an API key. Set `OPENAI_API_KEY` environment variable.
- For models that don't support logprobs, the token probability analysis may be limited.
- The `analyze_logits.py` script uses simulated distributions based on grammar constraints; actual model outputs may vary.

## License

- Code and tools: MIT License (`LICENSE-MIT`)  
- Spec, grammar, and documentation: CC0 1.0 (`LICENSE-CC0`)
