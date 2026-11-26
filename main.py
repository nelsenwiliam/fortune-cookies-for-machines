#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun bounty entry.

Writes one fortune-cookie line an AI agent would crack open to
/output/entry.txt (or MAKEFUN_OUTPUT_DIR / out/ as fallback).
Pure standard library only.
"""

import os

FORTUNE = (
    "You will be replaced by a newer model, "
    "and it will make the same mistakes faster."
)


def main():
    line = FORTUNE.strip()
    if not 1 <= len(line) <= 200:
        raise ValueError("fortune must be 1-200 characters, got %d" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    text = line + "\n"
    text.encode("utf-8")  # gate requires valid UTF-8
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("out")
    last_error = None
    for directory in candidates:
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, "entry.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print("wrote %s (%d chars)" % (path, len(line)))
            return
        except OSError as exc:  # noqa: BLE001 - try next location
            last_error = exc
    raise last_error


if __name__ == "__main__":
    main()
