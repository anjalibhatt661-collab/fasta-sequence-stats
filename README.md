# FASTA Sequence Stats

A small, dependency-free Python script that reads a FASTA file and reports basic properties of every sequence in it: **length**, **GC content**, and **base composition**.

## What it does

- Parses FASTA with code (no hand-counting). Handles multi-record files, multi-line sequences, blank lines, lowercase bases, and `.gz` files.
- For each sequence reports: length, GC %, and counts of A, C, G, T, U, N and "other" characters.
- Prints an overall summary line (number of sequences, total length, overall GC %).
- Works on any FASTA file: just point it at a different path.

## Requirements

Python 3.6+ (standard library only, nothing to install).

## How to run

```bash
python fasta_stats.py example.fasta
```

Save the table to a file as well:

```bash
python fasta_stats.py example.fasta -o output.tsv
```

Any other FASTA works the same way, for example a public dataset:

```bash
python fasta_stats.py my_genome.fasta
python fasta_stats.py proteins_or_genes.fasta.gz
```

## Example output

Running on the included `example.fasta` gives (see `output.tsv`):

```
id      length  gc_percent  A   C   G   T   U  N  other
seq1    74      54.05       16  18  22  18  0  0  0
seq2    32      87.50       2   14  14  2   0  0  0
seq3    36      0.00        16  0   0   18  0  2  0
# sequences=3 total_length=142 overall_gc_percent=48.57
```

## Decisions made

- **GC % is computed over unambiguous bases only** (A, C, G, T/U). `N` and other ambiguity codes are excluded from the denominator so they do not artificially lower GC content. The raw `N` and `other` counts are still reported.
- **Sequence ID** is the first word of the header line.
- **Case-insensitive**: sequences are upper-cased before counting.
- **Output is tab-separated** so it opens directly in Excel, pandas, or R.
- If a sequence has no A/C/G/T/U bases at all, GC % is reported as `NA` instead of dividing by zero.

## Files

| File | Purpose |
|---|---|
| `fasta_stats.py` | The script |
| `example.fasta` | Small sample input (3 records) |
| `output.tsv` | Output produced by running the script on the sample |
| `README.md` | This file |
