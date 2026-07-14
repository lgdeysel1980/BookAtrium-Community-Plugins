# Generated catalogue

CI / `scripts/generate_index.py` write `index.json` and `index.json.gz` here.

An empty catalogue (zero plugins) is valid. Contributors edit `plugins/*.json`, regenerate this folder, and commit the generated files. CI regenerates independently and fails if output is stale.

Live endpoints:

```text
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json
https://raw.githubusercontent.com/lgdeysel1980/BookAtrium-Community-Plugins/main/generated/index.json.gz
```

```bash
python scripts/generate_index.py --plugins-dir plugins --output-dir generated
```
