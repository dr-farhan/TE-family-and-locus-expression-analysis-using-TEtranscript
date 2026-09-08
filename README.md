# TE family and locus expression analysis with TEtranscripts

Snakemake workflow for quantifying transposable element (TE) expression from coordinate-sorted RNA-seq BAM files at both the TE family level (`TEcount`) and individual locus level (`TElocal`). 


## What the workflow does

For every sample in `config/samples.tsv`, the workflow runs `TEcount` for TE family quantification, runs `TElocal` for individual locus quantification, and collects per-sample tables into count matrices. 

## Installation

```bash
git clone https://github.com/dr-farhan/TE-family-and-locus-expression-analysis-using-TEtranscript.git
cd TE-family-and-locus-expression-analysis-using-TEtranscript
mamba env create \
    -f envs/te-transcripts.yaml

conda activate te-transcripts
```

If your site provides TEtranscripts through a module, activate Snakemake separately and set `software.tecount` and `software.telocal` in `config/config.yaml`.

## Prepare inputs

Copy the template sample sheet and replace the example row:

```bash
cp config/samples.tsv config/my_samples.tsv
```

The sample sheet is tab-separated:

```text
sample\tbam
sample_01\t/path/to/sample_01.sorted.bam
sample_02\t/path/to/sample_02.sorted.bam
```

Set the annotation paths in a project-specific copy of `config/config.yaml`:

```yaml
annotations:
  genes_gtf: /path/to/genes.gtf
  te_family_gtf: /path/to/te_family.gtf
  te_locus_gtf: /path/to/te_locus.gtf.locInd
```

The family annotation should be compatible with TEtranscripts. The locus annotation must be the `.locInd` annotation required by `TElocal`.

## Run

```bash
snakemake --configfile config/config.yaml --cores 1 --dry-run
snakemake --configfile config/config.yaml --cores 16 --use-conda
```

Run one branch by targeting its matrix:

```bash
snakemake --configfile config/config.yaml --cores 16 --use-conda \
  results/family/count_matrices/te_family_counts.tsv
```

Inspect the workflow graph with `snakemake --forceall --dag | dot -Tpng > workflow_dag.png`. Outputs are written below `results/family/` and `results/locus/`; per-sample TEtranscripts tables are retained alongside merged matrices.

## License

MIT. See [LICENSE](LICENSE).
