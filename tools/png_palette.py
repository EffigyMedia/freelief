"""Re-encode an opaque RGB PNG as a 256-color palette PNG, with the standard library only.

The size plan of the design (section 9, AUD-124) names a smaller 512 px icon as its first saving.
The icon is flat color with soft edges: the 255 most frequent colors are kept exactly, and each rarer
color (an edge pixel) takes its nearest kept color. Run by tools/make_icons.py after each render.
"""

import struct
import zlib
from collections import Counter
from pathlib import Path

PNG_SIGNATURE = bytes([0x89]) + b"PNG" + bytes([13, 10, 26, 10])


def _chunks(data):
    i = 8
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        yield data[i + 4:i + 8], data[i + 8:i + 8 + n]
        i += 12 + n


def _read_rgb(data):
    ihdr, idat = None, b""
    for kind, body in _chunks(data):
        if kind == b"IHDR":
            ihdr = body
        elif kind == b"IDAT":
            idat += body
    width, height, depth, color = struct.unpack(">IIBB", ihdr[:10])
    if depth != 8 or color not in (2, 6):
        raise ValueError("only 8-bit RGB or RGBA PNGs are re-encoded")
    bpp = 3 if color == 2 else 4
    raw = zlib.decompress(idat)
    stride, rows, prev, p = width * bpp, [], bytearray(width * bpp), 0
    for _ in range(height):
        kind, line = raw[p], bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if kind == 1:
                line[x] = (line[x] + a) & 255
            elif kind == 2:
                line[x] = (line[x] + b) & 255
            elif kind == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif kind == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line
    if bpp == 4 and any(row[x] != 255 for row in rows for x in range(3, len(row), 4)):
        raise ValueError("the image has transparency; it is left as it is")
    return width, height, [b"".join(row[x:x + 3] for x in range(0, len(row), bpp)) for row in rows]


def _chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)


def to_palette(path: Path) -> tuple[int, int]:
    """Re-encode `path` in place. Returns (bytes before, bytes after)."""
    data = path.read_bytes()
    width, height, rows = _read_rgb(data)
    count = Counter(row[x:x + 3] for row in rows for x in range(0, len(row), 3))
    palette = [color for color, _ in count.most_common(256)]
    index = {color: i for i, color in enumerate(palette)}
    nearest = {}

    def find(color):
        if color in index:
            return index[color]
        if color not in nearest:
            nearest[color] = min(range(len(palette)),
                                 key=lambda i: sum((palette[i][k] - color[k]) ** 2 for k in range(3)))
        return nearest[color]

    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw += bytes(find(row[x:x + 3]) for x in range(0, len(row), 3))
    out = (PNG_SIGNATURE + _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0))
           + _chunk(b"PLTE", b"".join(palette)) + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _chunk(b"IEND", b""))
    path.write_bytes(out)
    return len(data), len(out)
