#!/usr/bin/env python3
"""Report basic properties (length, GC content, composition) of FASTA sequences.

Usage:
    python fasta_stats.py INPUT.fasta [-o OUTPUT.tsv]

Works on any FASTA file (DNA or RNA, multi-record, multi-line, .gz supported).
Uses only the Python standard library.
"""
import argparse
import gzip
import sys
from collections import Counter


def parse_fasta(handle):
    """Yield (header, sequence) tuples from an open text file."""
    header, chunks = None, []
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(chunks)
            header, chunks = line[1:].strip(), []
        else:
            if header is None:
                raise ValueError("Invalid FASTA: sequence data before first '>' header")
            chunks.append(line.upper())
    if header is not None:
        yield header, "".join(chunks)


def open_any(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def gc_content(seq):
    """GC% over unambiguous bases (A, C, G, T/U). Returns None if none present."""
    counts = Counter(seq)
    gc = counts["G"] + counts["C"]
    acgt = gc + counts["A"] + counts["T"] + counts["U"]
    return 100.0 * gc / acgt if acgt else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("fasta", help="input FASTA file (.gz allowed)")
    ap.add_argument("-o", "--output", help="also write the table to this TSV file")
    args = ap.parse_args()

    cols = ["id", "length", "gc_percent", "A", "C", "G", "T", "U", "N", "other"]
    rows = []
    with open_any(args.fasta) as fh:
        for header, seq in parse_fasta(fh):
            c = Counter(seq)
            known = sum(c[b] for b in "ACGTUN")
            gc = gc_content(seq)
            rows.append([
                header.split()[0], len(seq),
                f"{gc:.2f}" if gc is not None else "NA",
                c["A"], c["C"], c["G"], c["T"], c["U"], c["N"], len(seq) - known,
            ])

    if not rows:
        sys.exit("No sequences found - is this a FASTA file?")

    lines = ["\t".join(cols)] + ["\t".join(map(str, r)) for r in rows]

    total = sum(r[1] for r in rows)
    total_gc = sum(r[5] + r[4] for r in rows)  # G + C
    total_acgt = sum(r[3] + r[4] + r[5] + r[6] + r[7] for r in rows)
    overall = f"{100.0 * total_gc / total_acgt:.2f}" if total_acgt else "NA"
    summary = f"# sequences={len(rows)} total_length={total} overall_gc_percent={overall}"

    out = "\n".join(lines) + "\n" + summary + "\n"
    print(out, end="")
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
