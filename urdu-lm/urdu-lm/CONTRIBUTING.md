# Contributing / مدد کیسے کریں

Shukriya! Har madad qeemti hai.

## 1. Sentence pairs add karein (coding ki zaroorat nahi)

`data/sample/roman_urdu_parallel_sample.jsonl` jaisa format use karein — har line ek pair:

```json
{"roman": "mujhe chai pasand hai", "urdu": "مجھے چائے پسند ہے"}
```

**Rules:**
- Sirf apne likhe hue jumle, ya aise source se jis ka license ijazat deta ho
- Koi personal maloomat (naam, phone number, address) nahi
- Gaali ya nafrat wala content nahi
- Roman Urdu waise hi likhein jaise log asal mein likhte hain (spellings mein farq theek hai)

## 2. Code mein madad

1. Repo fork karein
2. Nayi branch banayein: `git checkout -b my-feature`
3. Changes karein aur `python scripts/clean_text.py` chala kar check karein
4. Pull Request bhejein

## 3. Review

Open issues aur PRs mein data ki ghaltiyan pakarna bhi bari madad hai.
