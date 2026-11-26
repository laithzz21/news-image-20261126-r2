#!/usr/bin/env python3
"""news-image-20261126 — front-page image for the make.fun news-image bounty.

The bundled ``entry.png`` is the finished front page "THE WORLD TODAY —
Thursday 26 November 2026", a 1024x1024 newspaper front page. It carries
six genuine stories reported on Thursday 26 November 2026:

  * SPACE — Muhammad Zeeshan Ali becomes the first foreign astronaut
    to visit China's Tiangong station, aboard Shenzhou-24.
  * WAR — Russia's own figures show nearly 500,000 people lost in
    the Ukraine war; Kyiv says five Russian jets were hit in an
    airfield strike.
  * RESCUE — Colombian police storm a Cartagena supermarket and free
    20 people held hostage for 17 hours.
  * TRADE — The US is preparing to unveil a new plan for tariffs on
    global trading partners.
  * PACIFIC — Solomon Islands signs a security treaty with Australia.
  * SEOUL — South Korea's education minister resigns over an exam
    cheating scandal.

Footer ticker: Thanksgiving in America, Mumbai marking 18 years
since the 26/11 attacks, Venezuela revealing $237bn of public debt,
and North Korea ordering Switzerland to close its Pyongyang office.

This program does not render or draw anything: it validates the
bundled ``entry.png`` next to this script (PNG magic bytes, IHDR
dimensions 1024x1024, bit depth 8, colour type 2 = RGB, file size at
most 1 MiB, and the expected SHA-256 digest) and copies it
byte-identical to the output path. Standard library only — no PIL,
no network, no clock, no random numbers. Running the program twice
writes byte-identical PNG files.

Usage:
    python3 main.py [--verify] [--help]

Output path resolution, in order: $MAKEFUN_OUTPUT_DIR, then
$MAKEFUN_OUTPUT, then /output/entry.png; fallbacks ./output/entry.png
and a per-entry /tmp path. Parent directories are created first, and
the program never writes into the repository directory.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

EXPECTED_SHA256 = (
    "53b61fdf0849a1c1d8c241750042d683aba673f848423178135711da780fd49d"
)
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
EXPECTED_BIT_DEPTH = 8
EXPECTED_COLOUR_TYPE = 2  # RGB
MAX_SIZE = 1024 * 1024  # 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def read_source():
    """Return the bundled entry.png bytes, or None on error."""
    source = Path(__file__).resolve().parent / "entry.png"
    try:
        return source.read_bytes()
    except OSError as exc:
        print(f"error: cannot read bundled entry.png: {exc}", file=sys.stderr)
        return None


def validate_png(data):
    """Check the PNG header, IHDR fields, size and SHA-256 digest.

    Returns an error string, or None when the bytes are valid.
    """
    if len(data) > MAX_SIZE:
        return f"entry.png is {len(data)} bytes, over the 1 MiB limit"
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        return "entry.png does not start with the PNG magic bytes"
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        return "entry.png has no valid IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    bit_depth, colour_type = data[24], data[25]
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return f"entry.png is {width}x{height}, expected 1024x1024"
    if bit_depth != EXPECTED_BIT_DEPTH:
        return f"entry.png bit depth is {bit_depth}, expected 8"
    if colour_type != EXPECTED_COLOUR_TYPE:
        return f"entry.png colour type is {colour_type}, expected 2 (RGB)"
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        return (
            "entry.png SHA-256 does not match the expected digest "
            f"(got {digest})"
        )
    return None


def output_candidates():
    """Yield output paths in resolution order."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield Path(env_dir) / "entry.png"
    env_out = os.environ.get("MAKEFUN_OUTPUT")
    if env_out:
        yield Path(env_out)
    yield Path("/output/entry.png")
    yield Path.cwd() / "output" / "entry.png"
    yield Path("/tmp/news-image-20261126-r2/entry.png")


def write_output(data):
    """Write data to the first usable candidate path.

    Returns the path written, or None when every candidate failed.
    """
    last_error = None
    for path in output_candidates():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            # Confirm the file round-trips byte-identical before trusting it.
            if path.read_bytes() != data:
                raise OSError(f"written file differs from source: {path}")
        except OSError as exc:
            last_error = exc
            continue
        return path
    print(f"error: could not write output: {last_error}", file=sys.stderr)
    return None


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        print()
        print("Options: --verify  validate the bundled image and exit")
        print("         --help     show this help and exit")
        return 0

    data = read_source()
    if data is None:
        return 1

    error = validate_png(data)
    if error is not None:
        return fail(error)

    if "--verify" in argv:
        print(
            f"entry.png OK: {len(data)} bytes, "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT} RGB, "
            f"sha256 {EXPECTED_SHA256}"
        )
        return 0

    path = write_output(data)
    if path is None:
        return 1
    print(f"wrote {path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
