# -*- coding: utf-8 -*-
"""Provisional US Market Insight icons.

Reuses the site's rising-bar motif from the repository gen_icons.py.
These files are a stand-in until the owner confirms the final artwork.
The 1024 master is the source a future iOS marketing icon would use.
"""
import os
import struct
import zlib

BG = (13, 13, 13)
GREEN = (22, 199, 132)
GOLD = (201, 168, 76)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "resources")


def _png(width, height, rgba):
    def chunk(typ, data):
        head = struct.pack(">I", len(data)) + typ + data
        return head + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw.extend(rgba[y * width * 4:(y + 1) * width * 4])
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")


def _draw(width, height, rounded=True, transparent=False, pad_ratio=0.20):
    buf = bytearray(width * height * 4)
    radius = int(min(width, height) * 0.22) if rounded else 0

    def put(x, y, rgb, alpha=255):
        if 0 <= x < width and 0 <= y < height:
            i = (y * width + x) * 4
            buf[i:i + 4] = bytes((rgb[0], rgb[1], rgb[2], alpha))

    for y in range(height):
        for x in range(width):
            if radius:
                inside = True
                corners = (
                    (radius, radius),
                    (width - radius, radius),
                    (radius, height - radius),
                    (width - radius, height - radius),
                )
                in_corner = (
                    (x < radius and y < radius)
                    or (x >= width - radius and y < radius)
                    or (x < radius and y >= height - radius)
                    or (x >= width - radius and y >= height - radius)
                )
                if in_corner:
                    for cx, cy in corners:
                        if (x - cx) ** 2 + (y - cy) ** 2 > radius ** 2 and (
                            (cx < width / 2) == (x < width / 2) and (cy < height / 2) == (y < height / 2)
                        ):
                            inside = False
                            break
                if not inside:
                    continue
            if not transparent:
                put(x, y, BG)

    pad_x = width * pad_ratio
    pad_y = height * pad_ratio
    plot_l, plot_r = pad_x, width - pad_x
    plot_b = height - pad_y
    plot_h = plot_b - pad_y
    plot_w = plot_r - plot_l
    base_y = int(plot_b)
    thickness = max(1, int(min(width, height) * 0.012))
    for x in range(int(plot_l), int(plot_r)):
        for t in range(thickness):
            put(x, base_y + t, GOLD)
    gap = plot_w * 0.10
    bar_w = (plot_w - gap * 2) / 3
    for index, height_ratio in enumerate((0.42, 0.68, 1.0)):
        bx = plot_l + index * (bar_w + gap)
        bar_h = plot_h * height_ratio
        for x in range(int(bx), int(bx + bar_w)):
            for y in range(int(plot_b - bar_h), int(plot_b)):
                put(x, y, GREEN)
    return _png(width, height, buf)


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    print("wrote", os.path.relpath(path, ROOT))


def main():
    _write(os.path.join(RES, "play", "icon-1024.png"), _draw(1024, 1024))
    _write(os.path.join(RES, "play", "icon-512.png"), _draw(512, 512))
    _write(os.path.join(RES, "play", "feature-graphic-1024x500.png"), _draw(1024, 500, rounded=False, pad_ratio=0.28))

    legacy = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    foreground = {
        "mipmap-mdpi": 108,
        "mipmap-hdpi": 162,
        "mipmap-xhdpi": 216,
        "mipmap-xxhdpi": 324,
        "mipmap-xxxhdpi": 432,
    }
    for folder, size in legacy.items():
        png = _draw(size, size, rounded=True)
        _write(os.path.join(RES, "android", folder, "ic_launcher.png"), png)
        _write(os.path.join(RES, "android", folder, "ic_launcher_round.png"), png)
    for folder, size in foreground.items():
        _write(
            os.path.join(RES, "android", folder, "ic_launcher_foreground.png"),
            _draw(size, size, rounded=False, transparent=True, pad_ratio=0.24),
        )

    adaptive = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
"""
    for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
        path = os.path.join(RES, "android", "mipmap-anydpi-v26", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(adaptive)
        print("wrote", os.path.relpath(path, ROOT))

    color = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#0D0D0D</color>
</resources>
"""
    color_path = os.path.join(RES, "android", "values", "ic_launcher_background.xml")
    os.makedirs(os.path.dirname(color_path), exist_ok=True)
    with open(color_path, "w", encoding="utf-8") as handle:
        handle.write(color)
    print("wrote", os.path.relpath(color_path, ROOT))


if __name__ == "__main__":
    main()
