# Generated catalogue

CI / `scripts/generate_index.py` / `BookAtrium.PluginRegistryBuilder` write `index.json` and `index.json.gz` here.

Contributors edit `plugins/*.json`, regenerate this folder, and commit the generated files. CI regenerates independently and fails if output is stale.

```bash
python scripts/generate_index.py --plugins-dir plugins --output-dir generated
# or (private monorepo):
dotnet run --project BookAtrium.PluginRegistryBuilder -- --plugins-dir plugins --output-dir generated --publication
```
