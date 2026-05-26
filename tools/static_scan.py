#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

RESOURCE_PATTERNS = {
    "ROB": [r"rob.*(head|tail|ptr|full)"],
    "RS": [r"issue.*(slot|queue)", r"rs.*(alloc|free)"],
    "LSQ": [r"ldq", r"stq", r"loadqueue", r"storequeue"],
    "MSHR": [r"mshr", r"lfb", r"linebuffer"],
    "WB": [r"writebuffer", r"storebuffer"],
    "BTB": [r"btb.*(entry|index|hit)"],
    "RSB": [r"rsb", r"returnstack", r"ras"],
    "TLB": [r"tlb", r"ptw", r"pagewalk"],
}
COMPILED_RESOURCE_PATTERNS = {
    resource: [re.compile(p) for p in patterns]
    for resource, patterns in RESOURCE_PATTERNS.items()
}

# Heuristic confidence for static regex hits:
# - base score starts at 0.4 when any pattern matches
# - each additional matched pattern adds 0.2
# - cap at 0.95 to keep room for manual review
BASE_CONFIDENCE = 0.4
PATTERN_HIT_BONUS = 0.2
MAX_CONFIDENCE = 0.95


def scan_file(path: Path, core: str):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    lower = text.lower()
    findings = []
    for resource, patterns in COMPILED_RESOURCE_PATTERNS.items():
        matched = []
        for regex in patterns:
            m = regex.search(lower)
            if m:
                matched.append(m.group(0))
        if matched:
            confidence = min(BASE_CONFIDENCE + PATTERN_HIT_BONUS * len(matched), MAX_CONFIDENCE)
            findings.append(
                {
                    "core": core,
                    "module": path.name,
                    "resource_type": resource,
                    "signals": sorted(set(matched)),
                    "capacity_hint": "unknown",
                    "confidence": round(confidence, 2),
                    "evidence_path": str(path),
                }
            )
    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan RTL tree and emit resource candidates in JSONL")
    parser.add_argument("--core", required=True, choices=["boom", "rocket", "cva6"])
    parser.add_argument("--rtl-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ext", nargs="*", default=[".scala", ".sv", ".v"], help="File extensions")
    args = parser.parse_args()

    root = Path(args.rtl_root)
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix in args.ext]

    with Path(args.output).open("w", encoding="utf-8") as fp:
        for path in files:
            for finding in scan_file(path, args.core):
                fp.write(json.dumps(finding, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
