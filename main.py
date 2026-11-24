"""Entry point for the Nov 24, 2026 make.fun news-image bounty.

The grader runs in a bare python:3.13-slim container with no Pillow and no
fonts, so this file uses only the standard library: it copies the finished
front page (committed next to this script) to /output/entry.png.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    # The image is committed in this repo; the grader copies it, nothing is
    # generated or downloaded at run time, so the run is fully offline.
    if not os.path.isfile(SRC):
        print("error: entry.png must sit next to main.py in the repo root",
              file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote", DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
