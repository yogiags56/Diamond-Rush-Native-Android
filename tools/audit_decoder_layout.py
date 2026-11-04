#!/usr/bin/env python3
"""Corpus audit for the class-f image decoder's verified metadata prefix.

A successful result means the decoder's header, palette block and cumulative
image offsets are bounded. It does NOT mean pixel payloads have been decoded.
Other sections are classified as unrecognized/other-entrypoint, not corrupt.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_decoder_layout import probe, FormatError

def audit(root: Path):
    manifest = json.loads((root / "manifest.json").read_text())
    rows = []
    for item in manifest:
        data = (root / item["output"]).read_bytes()
        try:
            r = probe(data)
            rows.append({
                "file": item["output"], "resource": item["resource"],
                "section": item["section"], "bytes": len(data),
                "status": "bounded_image_metadata",
                "image_count": r.image_count, "palette_format": r.palette_format,
                "palette_groups": r.palette_groups, "palette_colors": r.palette_colors,
                "metadata_end": r.metadata_end,
                "pixel_data_bytes_after_metadata": len(data) - r.metadata_end
            })
        except FormatError as e:
            rows.append({
                "file": item["output"], "resource": item["resource"],
                "section": item["section"], "bytes": len(data),
                "status": "unclassified_for_this_decoder", "reason": str(e)
            })
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sections", type=Path, default=Path(__file__).resolve().parents[1]/"reference"/"sections")
    ap.add_argument("--json", type=Path)
    a=ap.parse_args()
    rows=audit(a.sections)
    counts={}
    for row in rows: counts[row["status"]]=counts.get(row["status"],0)+1
    print(f"sections={len(rows)}")
    for k,v in sorted(counts.items()): print(f"{k}={v}")
    print("bounded image metadata:")
    for r in rows:
        if r["status"]=="bounded_image_metadata":
            print(f'{r["file"]}: images={r["image_count"]}, palette={r["palette_format"]}, '
                  f'groups={r["palette_groups"]}, colors={r["palette_colors"]}, '
                  f'pixel_tail={r["pixel_data_bytes_after_metadata"]} bytes')
    if a.json: a.json.write_text(json.dumps({"summary":counts,"sections":rows},indent=2)+"\n")
if __name__=="__main__": main()
