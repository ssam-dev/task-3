# Quick Command Reference

Copy and paste these commands into your terminal to run the text generation project.

## Run the Custom Implementation (No Installation Required)

```bash
# Navigate to project directory
cd task-3

# Basic run with default settings
python main.py

# Generate 50 words and stop at sentence end
python main.py --mode word --order 2 --length 50 --stop-at-sentence

# Character-level generation
python main.py --mode char --order 4 --length 300

# Start with a specific word
python main.py --mode word --seed To --length 50 --stop-at-sentence
```

## Run the Markovify Implementation

```bash
# Step 1: Install markovify library (one-time setup)
pip install -r requirements.txt

# Step 2: Generate text (use state-size 1 for small corpus)
python markovify_main.py --state-size 1

# Generate multiple sentences
python markovify_main.py --samples 10 --state-size 1

# Generate short sentences (good for tweets, etc)
python markovify_main.py --samples 5 --short-max 100 --state-size 1
```

## What These Commands Do

- `python main.py` - Runs the custom Markov chain implementation
- `python markovify_main.py` - Runs the library-based implementation
- `--mode word` - Use word-level generation (default)
- `--mode char` - Use character-level generation
- `--order N` - Set n-gram size (higher = more coherent, but may overfit)
- `--length N` - Generate N tokens
- `--stop-at-sentence` - Stop when reaching a sentence-ending punctuation
- `--seed Word` - Start generation with a specific word
- `--state-size N` - Markovify's equivalent of order
- `--samples N` - Generate N sentences

## Troubleshooting

If you get "ModuleNotFoundError: No module named 'markovify'":
```bash
pip install markovify
```

For complete documentation, see USAGE.md
