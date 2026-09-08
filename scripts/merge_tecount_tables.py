#!/usr/bin/env python3
"""Merge TEtranscripts per-sample count tables into TE and gene matrices."""
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input-files", nargs="+", required=True)
parser.add_argument("--te-output", required=True)
parser.add_argument("--gene-output", required=True)
args = parser.parse_args()

def read_table(path):
    frame = pd.read_csv(path, sep="\t", comment="#")
    if frame.shape[1] < 2:
        raise ValueError(f"Expected an identifier and count columns in {path}")
    identifier = frame.columns[0]
    count_column = frame.columns[-1]
    frame = frame[[identifier, count_column]].copy()
    frame.columns = ["feature", Path(path).name.removesuffix(".cntTable")]
    return frame.set_index("feature")

tables = [read_table(path) for path in args.input_files]
matrix = pd.concat(tables, axis=1).fillna(0)
matrix = matrix.loc[~matrix.index.astype(str).str.startswith("__")]
matrix.index.name = "feature"

# TEtranscripts TE identifiers contain the family/class separators, while
# gene identifiers are normally plain symbols or stable gene IDs.
te_mask = matrix.index.astype(str).str.contains(":", regex=False)
gene_mask = ~te_mask
Path(args.te_output).parent.mkdir(parents=True, exist_ok=True)
Path(args.gene_output).parent.mkdir(parents=True, exist_ok=True)
matrix.loc[te_mask].to_csv(args.te_output, sep="\t")
matrix.loc[gene_mask].to_csv(args.gene_output, sep="\t")
print(f"Wrote {te_mask.sum()} TE features to {args.te_output}")
print(f"Wrote {gene_mask.sum()} gene features to {args.gene_output}")
