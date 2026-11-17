# 🇵🇰 Urdu Open-Source AI Model

**Open datasets, models and benchmarks for Urdu and Roman Urdu.**
اردو اور رومن اردو کے لیے اوپن سورس ڈیٹا سیٹ، ماڈل اور بینچ مارک۔

Urdu is spoken by more than 230 million people, yet it is poorly supported by today's AI models. Most people also type Urdu in **Roman script** (e.g. *"aap kaise hain?"*), and almost no open data exists for it. This project fixes that.

## 🎯 Goals

| # | Component | Status |
|---|-----------|--------|
| 1 | **Roman Urdu ↔ Urdu parallel dataset** | 🟡 In progress |
| 2 | **Urdu instruction dataset** (Q&A pairs) | ⚪ Planned |
| 3 | **Fine-tuned small Urdu model** (1B–3B) | ⚪ Planned |
| 4 | **Urdu benchmark** to evaluate any LLM | ⚪ Planned |
| 5 | **Live demo** on Hugging Face Spaces | ⚪ Planned |

## 📁 Repository structure

```
data/        datasets and samples
scripts/     cleaning and processing tools
training/    fine-tuning notebooks
eval/        Urdu benchmark
demo/        Gradio demo app
```

## 🚀 Quick start

```bash
git clone https://github.com/Shehroz-901/Urdu---open-source-AI-model.git
cd Urdu---open-source-AI-model
pip install -r requirements.txt

# Clean and validate the sample dataset
python scripts/clean_text.py data/sample/roman_urdu_parallel_sample.jsonl data/clean.jsonl
```

## 📊 Data format

Each line in a `.jsonl` file is one pair:

```json
{"roman": "aap kaise hain?", "urdu": "آپ کیسے ہیں؟"}
```

## 🤝 Contributing

Everyone can help — even without coding! You can add Roman Urdu ↔ Urdu sentence pairs, review data, or write Q&A pairs. See [CONTRIBUTING.md](CONTRIBUTING.md).

ہر کوئی مدد کر سکتا ہے، کوڈنگ کے بغیر بھی۔

## 🤗 Hugging Face

Datasets and models will be published at: [huggingface.co/Shehrozsami](https://huggingface.co/Shehrozsami)

## 📜 License

Code: Apache-2.0. Each dataset lists its own license on its Hugging Face page.
