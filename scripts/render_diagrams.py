#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import struct
import subprocess
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP_RE = re.compile(r"\n?<!-- mermaid-source-sha256: [0-9a-f]{64} -->\s*$")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_KEYWORD = b"mermaid-source-sha256\x00"


def source_hash(source: Path) -> str:
    text = source.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stamp_svg(source: Path) -> None:
    svg = source.with_suffix(".svg")
    if not svg.is_file():
        raise FileNotFoundError(f"missing Mermaid render: {svg.relative_to(ROOT)}")
    text = svg.read_text(encoding="utf-8")
    text = STAMP_RE.sub("", text).rstrip()
    text += f"\n<!-- mermaid-source-sha256: {source_hash(source)} -->\n"
    svg.write_text(text, encoding="utf-8", newline="\n")


def stamp_png(source: Path) -> None:
    png = source.with_suffix(".png")
    if not png.is_file():
        return
    data = png.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"invalid PNG render: {png.relative_to(ROOT)}")

    chunks: list[bytes] = []
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        end = offset + 12 + length
        chunk = data[offset:end]
        chunk_type = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        if not (chunk_type == b"tEXt" and payload.startswith(PNG_KEYWORD)):
            chunks.append(chunk)
        offset = end

    payload = PNG_KEYWORD + source_hash(source).encode("ascii")
    chunk_type = b"tEXt"
    stamp = struct.pack(">I", len(payload)) + chunk_type + payload
    stamp += struct.pack(">I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF)
    iend = next(i for i, chunk in enumerate(chunks) if chunk[4:8] == b"IEND")
    chunks.insert(iend, stamp)
    png.write_bytes(PNG_SIGNATURE + b"".join(chunks))


def render(source: Path) -> None:
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        raise FileNotFoundError("npx is required to render Mermaid diagrams")

    relative = source.relative_to(ROOT)
    svg = source.with_suffix(".svg").relative_to(ROOT)
    command = [
        npx,
        "--yes",
        "@mermaid-js/mermaid-cli",
        "-i",
        str(relative),
        "-o",
        str(svg),
        "--backgroundColor",
        "white",
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    stamp_svg(source)

    png_path = source.with_suffix(".png")
    if png_path.exists():
        png = png_path.relative_to(ROOT)
        png_command = command[:-4] + ["-o", str(png), "--backgroundColor", "white", "--width", "1800"]
        subprocess.run(png_command, cwd=ROOT, check=True)
        stamp_png(source)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render and source-stamp Mermaid diagrams.")
    parser.add_argument("paths", nargs="*", help="Mermaid .mmd files relative to the repository root")
    args = parser.parse_args()

    sources = [ROOT / path for path in args.paths] if args.paths else sorted(ROOT.rglob("*.mmd"))
    for source in sources:
        if not source.is_file() or source.suffix != ".mmd":
            raise FileNotFoundError(f"invalid Mermaid source: {source}")
        render(source)
        print(source.relative_to(ROOT))


if __name__ == "__main__":
    main()
