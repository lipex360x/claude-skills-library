#!/usr/bin/env python3
"""Clean SRT auto-generated subtitles into plain text.

Usage:
  clean-srt.py <file.srt> [output.txt]

If output.txt is omitted, prints to stdout.
"""
import re
import sys


def clean_srt(filepath):
    with open(filepath) as f:
        content = f.read()

    lines = []
    prev = ""
    for line in content.split("\n"):
        line = line.strip()
        # Skip empty lines, sequence numbers, timestamps
        if not line or re.match(r"^\d+$", line) or re.match(r"\d{2}:\d{2}:\d{2}", line):
            continue
        # Strip HTML-style tags from auto-captions
        line = re.sub(r"<[^>]+>", "", line)
        if line and line != prev:
            lines.append(line)
            prev = line

    return " ".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: clean-srt.py <file.srt> [output.txt]", file=sys.stderr)
        sys.exit(1)

    text = clean_srt(sys.argv[1])
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            f.write(text)
    else:
        print(text)
