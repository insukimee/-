# -*- coding: utf-8 -*-
"""Generate PWA PNG icons with no external deps (pure stdlib PNG encoder).

Draws a dark rounded tile with three ascending green bars (a rising-chart
motif) plus a gold baseline — the MarketInsight app icon.
"""
import struct
import zlib
import os

BG = (13, 13, 13)        # #0D0D0D
GREEN = (22, 199, 132)   # #16C784
GOLD = (201, 168, 76)    # #C9A84C


def _png(width, height, rgba):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0
        raw.extend(rgba[y * width * 4:(y + 1) * width * 4])
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    idat = zlib.compress(bytes(raw), 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def make_icon(size, maskable=False):
    buf = bytearray(size * size * 4)

    def put(x, y, rgb, a=255):
        if 0 <= x < size and 0 <= y < size:
            i = (y * size + x) * 4
            buf[i] = rgb[0]; buf[i+1] = rgb[1]; buf[i+2] = rgb[2]; buf[i+3] = a

    # Background: full-bleed for maskable, rounded tile otherwise.
    radius = 0 if maskable else int(size * 0.22)
    for y in range(size):
        for x in range(size):
            if radius:
                inside = True
                for cx, cy in ((radius, radius), (size-radius, radius),
                               (radius, size-radius), (size-radius, size-radius)):
                    if ((x < radius and y < radius) or (x > size-radius and y < radius) or
                            (x < radius and y > size-radius) or (x > size-radius and y > size-radius)):
                        if (x-cx)**2 + (y-cy)**2 > radius**2:
                            inside = False
                            break
                if not inside:
                    continue
            put(x, y, BG)

    # Safe area (maskable keeps content within ~64% center).
    pad = size * (0.26 if maskable else 0.20)
    plot_l, plot_r = pad, size - pad
    plot_b = size - pad
    plot_top = pad
    plot_w = plot_r - plot_l
    plot_h = plot_b - plot_top

    # Gold baseline.
    base_y = int(plot_b)
    for x in range(int(plot_l), int(plot_r)):
        for t in range(max(1, int(size * 0.012))):
            put(x, base_y + t, GOLD)

    # Three ascending green bars.
    n = 3
    gap = plot_w * 0.10
    bw = (plot_w - gap * (n - 1)) / n
    heights = [0.42, 0.68, 1.0]
    for k in range(n):
        bx = plot_l + k * (bw + gap)
        bh = plot_h * heights[k]
        by = plot_b - bh
        for x in range(int(bx), int(bx + bw)):
            for y in range(int(by), int(plot_b)):
                put(x, y, GREEN)

    return _png(size, size, buf)


def main():
    os.makedirs("icons", exist_ok=True)
    targets = [
        ("icons/icon-192.png", 192, False),
        ("icons/icon-512.png", 512, False),
        ("icons/icon-180.png", 180, False),    # apple-touch-icon
        ("icons/maskable-512.png", 512, True),
        ("icons/favicon-32.png", 32, False),
    ]
    for path, size, mask in targets:
        with open(path, "wb") as f:
            f.write(make_icon(size, mask))
        print("wrote", path)


if __name__ == "__main__":
    main()
