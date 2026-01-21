import argparse
from pathlib import Path
from src.markov_chain import MarkovChain


def parse_args():
    p = argparse.ArgumentParser(description="Simple Markov chain text generator")
    p.add_argument("--corpus-path", type=str, default="data/corpus.txt", help="Path to training text corpus")
    p.add_argument("--mode", type=str, choices=["word", "char"], default="word", help="Model type: word or char")
    p.add_argument("--order", type=int, default=2, help="n-gram order (state size)")
    p.add_argument("--length", type=int, default=50, help="Number of tokens to generate")
    p.add_argument("--seed", type=str, default=None, help="Optional starting word/char")
    p.add_argument("--stop-at-sentence", action="store_true", help="Stop when sentence ends (word mode only)")
    return p.parse_args()


def main():
    args = parse_args()
    corpus_path = Path(args.corpus_path)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus not found: {corpus_path}")
    text = corpus_path.read_text(encoding="utf-8")
    mc = MarkovChain(order=args.order, mode=args.mode)
    mc.train(text)
    generated = mc.generate(length=args.length, seed=args.seed, stop_at_sentence=args.stop_at_sentence)
    print("\n=== Generated Text ===\n")
    print(generated)


if __name__ == "__main__":
    main()
