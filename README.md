/home/sahmad/.bashrc: line 41: unexpected EOF while looking for matching `"'
/home/sahmad/.bashrc: line 42: syntax error: unexpected end of file
# TE family and locus expression analysis with TEtranscripts

Reproducible Snakemake workflow for quantifying transposable element (TE) expression from coordinate-sorted RNA-seq BAM files at both the TE family level (`TEcount`) and individual locus level (`TElocal`). The workflow preserves the analysis settings used in the originating analysis while exposing all dataset-specific inputs through a small configuration file.

The repository follows the configuration-driven Snakemake layout used in [crazyhottommy/RNA-seq-analysis](https://github.com/crazyhottommy/RNA-seq-analysis/tree/master/RNA-seq-snakemake-pipeline), with sample metadata separated from workflow code.

## What the workflow does

For every sample in `config/samples.tsv`, the workflow validates inputs, runs `TEcount` for TE family quantification, runs `TElocal` for individual locus quantification, and collects per-sample tables into count matrices. Both branches use positional sorting, `--mode multi`, reverse strandedness, and configurable CPU resources.

No FASTQ, BAM, annotation, or project-specific path is included in this repository.

## Installation

```bash
git clone https://github.com/dr-farhan/TE-family-and-locus-expression-analysis-using-TEtranscript.git
cd TE-family-and-locus-expression-analysis-using-TEtranscript
mamba env create -f envs/te-transcripts.yaml
mamba activate te-transcripts
```

If your site provides TEtranscripts through a module, activate Snakemake separately and set `software.tecount` and `software.telocal` in `config/config.yaml` to the available commands.

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

## Reproducibility

The default settings are recorded in `config/config.yaml`; change them in a project-specific config file rather than editing the Snakefile. The workflow does not download reference files or embed data. Record the annotation release and reference genome in your project metadata before running.

## License

MIT. See [LICENSE](LICENSE).
