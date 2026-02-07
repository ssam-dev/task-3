# Simple Markov Chain Text Generator

This project implements a minimal text generation algorithm using Markov chains. It supports word-level and character-level models with configurable n-gram order. Inspired by the concepts in the article: Text Generation with Markov Chains: An Introduction to using Markovify (Towards Data Science).

Reference: https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33/

## Features
- Word- or character-level modeling
- Configurable state size (order) for n-grams
- Optional sentence-aware starts and early stop at sentence end (word mode)
- Lightweight, pure Python—no external dependencies

## Quick Start

1. Ensure you have Python 3.9+ installed.
2. Use the provided sample corpus in `data/corpus.txt` or point to your own.

### Run the Custom Implementation (No Dependencies Required)

```bash
# Word-level, bigram model (default)
python main.py

# With custom settings
python main.py --corpus-path data/corpus.txt --mode word --order 2 --length 50 --stop-at-sentence

# Character-level, 4-gram model
python main.py --corpus-path data/corpus.txt --mode char --order 4 --length 300

# Start with a specific word (if present in starts)
python main.py --corpus-path data/corpus.txt --mode word --order 2 --length 60 --seed To --stop-at-sentence
```

### Run the Markovify Implementation

First, install dependencies:
```bash
pip install -r requirements.txt
```

Then run:
```bash
# Generate 5 sentences using markovify (use state-size 1 for small corpus)
python markovify_main.py --state-size 1

# Generate 10 short sentences
python markovify_main.py --samples 10 --short-max 100 --state-size 1
```

📖 **For detailed usage instructions, troubleshooting, and explanation of how text generation works, see [USAGE.md](USAGE.md)**

## How It Works
- The model builds a transition table mapping each n-token state to counts of the next token.
- Generation samples next tokens proportional to observed frequencies: $P(x_{t+1}\mid x_{t-n+1..t})$.
- For word mode, sentence-ending tokens (`.`, `!`, `?`) mark possible start states, improving coherence.

## Notes
- Higher `order` yields more coherent text but risks overfitting.
- Clean, domain-specific corpora produce better results.
- For a library-based approach, consider [markovify](https://pypi.org/project/markovify/), as discussed in the reference article.

## License
Public domain sample corpus provided; generated text is synthetic.
