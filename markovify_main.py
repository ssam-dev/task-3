import argparse
from pathlib import Path
import markovify
import re


def parse_args():
    p = argparse.ArgumentParser(description="Markovify text generator (word-level)")
    p.add_argument("--corpus-path", type=str, default="data/corpus.txt", help="Path to training text corpus")
    p.add_argument("--state-size", type=int, default=3, help="Markov state size (n-gram order)")
    p.add_argument("--samples", type=int, default=5, help="Number of sentences to generate")
    p.add_argument("--short-max", type=int, default=0, help="If >0, generate short sentences up to this many chars")
    p.add_argument("--tries", type=int, default=100, help="Generation attempts per sentence")
    p.add_argument("--start", type=str, default=None, help="Optional starting word for sentence generation")
    return p.parse_args()


def main():
    args = parse_args()
    corpus_path = Path(args.corpus_path)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus not found: {corpus_path}")
    text = corpus_path.read_text(encoding="utf-8")
    # Split into rough sentences by punctuation; feed to NewlineText
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 3]
    if not sentences:
        sentences = [text.strip()]
    prepared = "\n".join(sentences)
    model = markovify.NewlineText(prepared, state_size=args.state_size)

    print("\n=== Markovify Generated Text ===\n")
    for i in range(args.samples):
        if args.short_max and args.short_max > 0:
            sent = model.make_short_sentence(
                max_chars=args.short_max,
                tries=args.tries,
                max_overlap_ratio=0.95,
                max_overlap_total=60,
            )
        else:
            if args.start:
                sent = model.make_sentence_with_start(
                    args.start,
                    strict=False,
                    tries=args.tries,
                    max_overlap_ratio=0.95,
                    max_overlap_total=60,
                )
            else:
                sent = model.make_sentence(
                    tries=args.tries,
                    well_formed=False,
                    max_overlap_ratio=0.95,
                    max_overlap_total=60,
                )
        print(sent or "<no sentence>")


if __name__ == "__main__":
    main()
