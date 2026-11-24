#!/usr/bin/env python3
"""Assemble split incoming/*.b64.partNN files when a sibling .ready marker exists."""
from __future__ import annotations

import glob
import os
import sys

ready_files = glob.glob("incoming/**/*.ready", recursive=True)
for ready in ready_files:
    stem = ready[: -len(".ready")]
    parts = sorted(glob.glob(stem + ".b64.part[0-9][0-9]"))
    if not parts:
        print(f"no parts for {ready}", file=sys.stderr)
        sys.exit(1)
    assembled = stem + ".b64"
    print("assemble", assembled, "from", parts)
    with open(assembled, "wb") as out:
        for path in parts:
            out.write(open(path, "rb").read())
    for path in parts:
        os.remove(path)
    os.remove(ready)
    print("wrote", assembled, os.path.getsize(assembled))
