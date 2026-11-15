#!/usr/bin/env python3
"""Adjust the generated editorial cards after Readme Atelier runs.

The public GitHub location field is the placeholder "Unknown". The portrait
caption should read Delhi, India, which is what the public site shows.
The left label is rewritten to the portfolio's "+ (01)  Profile" form.

The minimal theme's ink and paper are not configurable. After the accent
override, this remaps those baked colors to black and white so the cards
stay on black, white, and #1D9BF0. Empty heatmap cells use the same inks
at low opacity. Hex replacements cannot hit the embedded font, which is
base64 and contains no '#' bytes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "atelier"

SKY = "#1D9BF0"
LIGHT = {
    "#ff4d00": SKY,
    "#FF4D00": SKY,
    "#1d9bf0": SKY,
    "#f2f2f0": "#ffffff",
    "#262626": "#000000",
    "#6a6a6a": "#000000",
}
DARK = {
    "#ff4d00": SKY,
    "#FF4D00": SKY,
    "#1d9bf0": SKY,
    "#0f0f0f": "#000000",
    "#ececea": "#ffffff",
    "#9a9a96": "#ffffff",
}


def recolor(text: str, dark: bool) -> str:
    if dark:
        text = text.replace('fill="#202020"', 'fill="#ffffff" fill-opacity="0.18"')
        table = DARK
    else:
        text = text.replace('fill="#e2e2de"', 'fill="#000000" fill-opacity="0.12"')
        table = LIGHT
    for src, dst in table.items():
        text = text.replace(src, dst)
    return text


def main() -> None:
    if not ROOT.exists():
        return
    for path in sorted(ROOT.glob("*.svg")):
        text = path.read_text(encoding="utf-8")
        updated = recolor(text, "-dark" in path.name)
        if path.name.startswith("header"):
            updated = updated.replace(">Unknown</text>", ">Delhi, India</text>")
            updated = updated.replace("+ (Profile)", "+ (01)  Profile")
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"patched {path.name}")
        else:
            print(f"unchanged {path.name}")
    # Cards we do not publish: repo links would leave https://0xreso.dev,
    # and stack / social cards pull in brand icons.
    for pattern in ("repo-*.svg", "social-*.svg", "stack-*.svg", "footer*.svg"):
        for path in ROOT.glob(pattern):
            path.unlink()
            print(f"removed {path.name}")

    readme = ROOT.parent / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        start = text.find("<!-- readme-atelier:start -->")
        end = text.find("<!-- readme-atelier:end -->")
        if start != -1 and end != -1:
            block = text[start:end]
            # Full-width cards stay readable on a phone. 49% shrinks the type
            # below a legible size in GitHub's mobile column.
            stacked = block.replace('width="49%"', 'width="100%"')
            if stacked != block:
                readme.write_text(text[:start] + stacked + text[end:], encoding="utf-8")
                print("stacked stats and languages to full width")


if __name__ == "__main__":
    main()
