# wikidata-rubq-hf

Huggingface Dataset wrapper for Wikidata-RuBQ 2.0 dataset

### Usage

```bash
git clone git@github.com:s-nlp/wikidata-rubq-hf.git wikidata_rubq
```

```python3
from datasets import load_dataset;
load_dataset('wikidata_rubq.py', 'multiple_en', cache_dir='.', ignore_verifications=True)
```
