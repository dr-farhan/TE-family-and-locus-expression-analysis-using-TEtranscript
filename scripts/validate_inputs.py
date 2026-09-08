#!/usr/bin/env python3
"""Validate a sample sheet and reference inputs before quantification."""
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("samples")
parser.add_argument("genes")
parser.add_argument("te_family")
parser.add_argument("te_locus")
parser.add_argument("bams", nargs="+")
args = parser.parse_args()

sheet = pd.read_csv(args.samples, sep="\t", dtype=str).fillna("")
if list(sheet.columns[:2]) != ["sample", "bam"]:
    raise ValueError("The sample sheet must start with columns: sample and bam")
if sheet["sample"].duplicated().any():
    raise ValueError("Sample names must be unique")
for path in [args.genes, args.te_family, args.te_locus, *args.bams]:
    if not Path(path).is_file():
        raise FileNotFoundError(path)
print(f"Validated {len(sheet)} samples and three annotation files.")
