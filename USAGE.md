# How to Run the Text Generation Project

This guide provides step-by-step terminal commands to run the text generation project.

## Prerequisites

Make sure you have Python 3.9+ installed:
```bash
python --version
```

## Quick Start - Running the Custom Implementation

The custom implementation (`main.py`) requires **no external dependencies**. You can run it immediately:

```bash
# Navigate to project directory
cd /home/runner/work/task-3/task-3

# Run with default settings (word-level, 2-gram model, 50 tokens)
python main.py
```

### Example Commands for main.py

```bash
# Generate 50 words using word-level bigram model
python main.py --corpus-path data/corpus.txt --mode word --order 2 --length 50

# Stop at sentence end for more natural output
python main.py --mode word --order 2 --length 50 --stop-at-sentence

# Character-level generation (300 characters)
python main.py --mode char --order 4 --length 300

# Start with a specific word (e.g., "To")
python main.py --mode word --order 2 --length 60 --seed To --stop-at-sentence

# Use a higher order for more coherent text (but may overfit)
python main.py --mode word --order 3 --length 100 --stop-at-sentence
```

## Running the Markovify Implementation

The `markovify_main.py` uses the external `markovify` library for text generation.

### Step 1: Install Dependencies

```bash
# Install markovify library
pip install -r requirements.txt
```

### Step 2: Run Markovify Implementation

**Note:** The default corpus is small, so you may need to use `--state-size 1` or `2` for better results, or provide a larger corpus.

```bash
# Generate 5 sentences (use state-size 1 for small corpus)
python markovify_main.py --state-size 1

# Generate 10 sentences
python markovify_main.py --samples 10 --state-size 1

# Generate shorter sentences (max 100 characters)
python markovify_main.py --samples 5 --short-max 100 --state-size 1

# Start sentences with a specific word
python markovify_main.py --samples 5 --start To --state-size 1

# Use different state size (n-gram order)
python markovify_main.py --state-size 2 --samples 5 --tries 500
```

### Example Commands for markovify_main.py

```bash
# Generate 3 short sentences (max 80 chars) - for small corpus use state-size 1
python markovify_main.py --samples 3 --short-max 80 --state-size 1

# Generate sentences starting with "Fair" (needs larger corpus or lower state-size)
python markovify_main.py --samples 5 --start Fair --state-size 1

# Use bigram model (state-size 2) for more random output
python markovify_main.py --state-size 2 --samples 10 --tries 500
```

## Using Your Own Text Corpus

To use your own text file:

```bash
# For custom implementation
python main.py --corpus-path /path/to/your/text.txt --mode word --order 2 --length 50

# For markovify implementation
python markovify_main.py --corpus-path /path/to/your/text.txt --samples 5
```

## How Text Generation Works

### Markov Chain Basics

The text generation algorithm uses **Markov chains**, a statistical model that predicts the next word (or character) based on the previous N words/characters, where N is the "order" or "state size".

### Step-by-Step Process:

1. **Training Phase:**
   - The algorithm reads your corpus (training text)
   - It breaks the text into tokens (words or characters)
   - It builds a transition table: for each sequence of N tokens (called a "state"), it records what tokens can follow and how often
   - Example: After seeing "to be", it might record that "or" appears 5 times, "," appears 2 times, etc.

2. **Generation Phase:**
   - Start with a random state (or a seed word if provided)
   - Look up possible next tokens in the transition table
   - Choose the next token randomly, weighted by frequency (more common tokens are more likely)
   - Add the token to output and update the state (shift window)
   - Repeat until reaching desired length or sentence end

### Example Walkthrough:

Given corpus: "To be or not to be"

**With order=2 (bigrams):**
- States: ["To be", "be or", "or not", "not to", "to be"]
- If we start with "To be", the next word can only be "or"
- Current state becomes "be or", next word must be "not"
- And so on...

**With order=1 (unigrams):**
- States: ["To", "be", "or", "not", "to"]
- After "To", possible next words: "be" (50%) or nothing more
- After "be", possible next words: "or" (50%), "," (50%)
- More variation, less coherence

### Parameters Explained:

- **--mode word/char**: Use words or characters as tokens
  - Word mode: More natural language, requires more training data
  - Character mode: Can generate new "words", works with less data

- **--order N**: Size of the context window (N-gram)
  - order=1: Very random, little coherence
  - order=2: Balanced (default for words)
  - order=3+: More coherent but may just copy training text

- **--length N**: How many tokens to generate
  - For words: 50-100 is reasonable
  - For characters: 200-500 works well

- **--seed**: Starting word/character
  - Helps guide generation toward specific topics
  - Must exist in the corpus

### Why It Works:

The algorithm captures local patterns in language:
- Common word combinations ("not to be", "it is a")
- Grammar patterns (verb follows subject)
- Writing style (formal vs casual)

### Limitations:

- No long-term coherence (forgets context beyond order N)
- Can't understand meaning or logic
- May generate nonsensical combinations not in training data
- Quality depends heavily on corpus size and quality

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'markovify'"
**Solution:** Install dependencies first:
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError: Corpus not found"
**Solution:** Make sure the corpus file exists:
```bash
ls -la data/corpus.txt
# Or specify correct path with --corpus-path
```

### Poor Quality Output
**Solutions:**
- Use a larger, higher-quality corpus
- Adjust the order (try 2-3 for word mode, 3-5 for char mode)
- Use `--stop-at-sentence` flag for more natural endings
- Make sure your corpus has proper punctuation

## Understanding the Difference

### Custom Implementation (main.py)
- Pure Python, no dependencies
- Educational code, easy to understand
- Supports both word and character modes
- Good for learning how Markov chains work

### Markovify Implementation (markovify_main.py)
- Uses the popular `markovify` library
- More features and optimizations
- Better for production use
- Sentence-aware generation
- More control over output quality

## Common Use Cases

```bash
# Quick random text with your own corpus
python main.py --corpus-path mybook.txt --length 100 --stop-at-sentence

# Generate poetry-like text (character mode)
python main.py --corpus-path poems.txt --mode char --order 5 --length 500

# Generate technical text with domain-specific corpus
python markovify_main.py --corpus-path documentation.txt --samples 10 --state-size 3

# Short social media posts
python markovify_main.py --corpus-path tweets.txt --short-max 140 --samples 20
```

## Additional Resources

- Original Article: [Text Generation with Markov Chains: An Introduction to using Markovify](https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33/)
- Markovify Documentation: https://github.com/jsvine/markovify
- See README.md for project overview
