#!/usr/bin/env python3
"""news-image-20261117 entry program (Python 3.13 stdlib only).

Copies the pre-drawn entry.png sitting beside this file into the
grader's output directory ($MAKEFUN_OUTPUT_DIR, default /output).
Runs offline, writes identical bytes on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # verify the copy landed whole: sizes must match exactly
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy failed: size mismatch")
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
