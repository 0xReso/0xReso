#!/usr/bin/env python3
"""Adjust the generated editorial header after Readme Atelier runs.

The public GitHub location field is the placeholder "Unknown". The portrait
caption should read Delhi, India, which is what the public site shows.
The left label is rewritten to the portfolio's "+ (01)  Profile" form.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "atelier"

def main() -> None:
    if not ROOT.exists():
        return
    for path in ROOT.glob("header*.svg"):
        text = path.read_text(encoding="utf-8")
        updated = text.replace(">Unknown</text>", ">Delhi, India</text>")
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
