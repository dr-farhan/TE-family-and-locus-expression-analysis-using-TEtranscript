from pathlib import Path
import yaml

root = Path(__file__).parents[1]
config = yaml.safe_load((root / "config/config.yaml").read_text())
assert config["quantification"]["mode"] == "multi"
assert config["quantification"]["stranded"] == "reverse"
assert config["resources"]["threads"] == 16
assert (root / "workflow/Snakefile").is_file()
assert (root / "envs/te-transcripts.yaml").is_file()
print("Repository structure and preserved quantification defaults are valid.")
