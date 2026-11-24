#!/usr/bin/env python3
"""Fortune in a Pot -- make.fun entry.

Writes a single kind, funny fortune for a houseplant to ``entry.txt``
in the output directory (``$MAKEFUN_OUTPUT_DIR``, default ``/output``).

The fortune is fixed on purpose: the entry is judged on this exact
text, so the program is deterministic by design and every run writes
the same bytes. It stays within the gate (1-120 characters) and reads
like a prediction for the plant on the windowsill.
"""

import os
import sys

FORTUNE = (
    "You will outgrow this pot by spring, and your keeper, "
    "who talks to you daily, will pretend it was the fertilizer."
)

MAX_CHARS = 120


def main() -> int:
    fortune = FORTUNE.strip()
    # The gate reads the file as one line of text: it must be 1-120
    # characters, not only white space, and carry no line break of its own.
    if not 1 <= len(fortune) <= MAX_CHARS:
        print(
            f"fortune is {len(fortune)} characters; must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if fortune != fortune.strip() or "\n" in fortune or "\r" in fortune:
        print("fortune must be a single clean line", file=sys.stderr)
        return 1
    try:
        fortune.encode("utf-8")
    except UnicodeEncodeError:
        print("fortune is not valid UTF-8 text", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    entry_path = os.path.join(out_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(fortune + "\n")

    # Confirm the file on disk holds exactly the fortune we meant.
    with open(entry_path, "r", encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != fortune + "\n":
        print("entry.txt on disk does not match the fortune", file=sys.stderr)
        return 1

    print(on_disk.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
