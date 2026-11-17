"""
Clean and validate a Roman Urdu <-> Urdu parallel dataset.

Usage:
    python scripts/clean_text.py INPUT.jsonl OUTPUT.jsonl

Input: one JSON object per line: {"roman": "...", "urdu": "..."}
What it does:
  - Unicode NFC normalization
  - Replaces Arabic look-alike letters with the correct Urdu letters
  - Removes URLs, emails, extra spaces and invisible characters
  - Drops rows that are empty, too short, too long, or not really Urdu
  - Removes exact duplicates
  - Prints a short report
"""

import json
import re
import sys
import unicodedata

# Arabic letters that often appear in Urdu text by mistake -> correct Urdu letter
ARABIC_TO_URDU = {
    "ي": "ی",  # ي -> ی
    "ى": "ی",  # ى -> ی
    "ك": "ک",  # ك -> ک
    "ه": "ہ",  # ه -> ہ
    "ة": "ۃ",  # ة -> ۃ
}

URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
INVISIBLE_RE = re.compile(r"[​-‏‪-‮⁦-⁩﻿]")
SPACE_RE = re.compile(r"\s+")
URDU_CHAR_RE = re.compile(r"[؀-ۿ]")
LATIN_CHAR_RE = re.compile(r"[A-Za-z]")

MIN_CHARS = 2
MAX_CHARS = 500
MIN_URDU_RATIO = 0.6   # share of letters in the urdu field that must be Urdu script
MIN_LATIN_RATIO = 0.6  # share of letters in the roman field that must be Latin


def basic_clean(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = URL_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = INVISIBLE_RE.sub("", text)
    return SPACE_RE.sub(" ", text).strip()


def clean_urdu(text: str) -> str:
    text = basic_clean(text)
    for wrong, right in ARABIC_TO_URDU.items():
        text = text.replace(wrong, right)
    return text


def clean_roman(text: str) -> str:
    return basic_clean(text)


def script_ratio(text: str, pattern: re.Pattern) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if pattern.match(c)) / len(letters)


def check_row(roman: str, urdu: str):
    """Return None if the row is fine, otherwise a short reason string."""
    if not roman or not urdu:
        return "empty"
    if len(roman) < MIN_CHARS or len(urdu) < MIN_CHARS:
        return "too_short"
    if len(roman) > MAX_CHARS or len(urdu) > MAX_CHARS:
        return "too_long"
    if script_ratio(urdu, URDU_CHAR_RE) < MIN_URDU_RATIO:
        return "urdu_not_urdu_script"
    if script_ratio(roman, LATIN_CHAR_RE) < MIN_LATIN_RATIO:
        return "roman_not_latin_script"
    return None


def main(in_path: str, out_path: str) -> None:
    seen = set()
    kept = 0
    dropped = {}

    with open(in_path, encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        for line_no, line in enumerate(fin, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                dropped["bad_json"] = dropped.get("bad_json", 0) + 1
                print(f"  line {line_no}: bad JSON, skipped")
                continue

            roman = clean_roman(str(row.get("roman", "")))
            urdu = clean_urdu(str(row.get("urdu", "")))

            reason = check_row(roman, urdu)
            if reason is None:
                key = (roman.lower(), urdu)
                if key in seen:
                    reason = "duplicate"
                else:
                    seen.add(key)

            if reason:
                dropped[reason] = dropped.get(reason, 0) + 1
                continue

            fout.write(json.dumps({"roman": roman, "urdu": urdu}, ensure_ascii=False) + "\n")
            kept += 1

    total_dropped = sum(dropped.values())
    print(f"\n✅ Kept: {kept}   ❌ Dropped: {total_dropped}")
    for reason, count in sorted(dropped.items(), key=lambda x: -x[1]):
        print(f"   - {reason}: {count}")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
