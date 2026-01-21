import random
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class MarkovChain:
    """
    Simple Markov chain text generator supporting word- and character-level models.

    - order: n-gram order (state size). For words, 1-3 usually works; for chars, 2-5.
    - mode: 'word' or 'char'.
    """

    def __init__(self, order: int = 2, mode: str = "word") -> None:
        if mode not in ("word", "char"):
            raise ValueError("mode must be 'word' or 'char'")
        if order < 1:
            raise ValueError("order must be >= 1")
        self.order = order
        self.mode = mode
        self.transitions: Dict[Tuple[str, ...], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.start_states: List[Tuple[str, ...]] = []

    @staticmethod
    def _tokenize_words(text: str) -> List[str]:
        # Words and punctuation as separate tokens
        return re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)

    @staticmethod
    def _detokenize_words(tokens: List[str]) -> str:
        # Basic detokenizer: join words with spaces; attach punctuation properly
        out: List[str] = []
        no_space_before = set(", . ! ? : ; ) ] } ' \"".split())
        no_space_after = set("( [ { \" '")
        for i, tok in enumerate(tokens):
            if not out:
                out.append(tok)
                continue
            prev = out[-1]
            if tok in no_space_before:
                out.append(tok)
            elif prev in no_space_after:
                out.append(tok)
            else:
                out.append(" " + tok)
        return "".join(out)

    def _tokenize(self, text: str) -> List[str]:
        return list(text) if self.mode == "char" else self._tokenize_words(text)

    def _detokenize(self, tokens: List[str]) -> str:
        return "".join(tokens) if self.mode == "char" else self._detokenize_words(tokens)

    def train(self, text: str) -> None:
        tokens = self._tokenize(text)
        if len(tokens) <= self.order:
            return
        # Identify plausible start positions (sentence starts for words; beginning for chars)
        start_indexes = [0]
        if self.mode == "word":
            enders = {".", "!", "?"}
            for i, t in enumerate(tokens[:-1]):
                if t in enders:
                    start_indexes.append(i + 1)
        # Build transitions and start states
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i : i + self.order])
            next_tok = tokens[i + self.order]
            self.transitions[state][next_tok] += 1
        # Collect start states (must have a following token)
        for i in start_indexes:
            if i + self.order < len(tokens):
                self.start_states.append(tuple(tokens[i : i + self.order]))
        # Fallback if no start states found
        if not self.start_states:
            self.start_states = list(self.transitions.keys())

    def _weighted_choice(self, counts: Dict[str, int]) -> Optional[str]:
        if not counts:
            return None
        choices, weights = zip(*counts.items())
        return random.choices(list(choices), weights=list(weights), k=1)[0]

    def generate(
        self,
        length: int = 50,
        seed: Optional[str] = None,
        stop_at_sentence: bool = False,
    ) -> str:
        if not self.transitions:
            return ""
        # Seed handling: find a start state beginning with seed if provided
        if seed:
            candidates = [s for s in self.start_states if s[0].lower() == seed.lower()]
            state = random.choice(candidates) if candidates else random.choice(self.start_states)
        else:
            state = random.choice(self.start_states)
        out: List[str] = list(state)
        enders = {".", "!", "?"}
        while len(out) < length:
            next_tok = self._weighted_choice(self.transitions.get(state, {}))
            if next_tok is None:
                break
            out.append(next_tok)
            state = tuple(out[-self.order :])
            if stop_at_sentence and self.mode == "word" and next_tok in enders:
                break
        return self._detokenize(out)


def build_and_generate(
    text: str,
    order: int = 2,
    mode: str = "word",
    length: int = 50,
    seed: Optional[str] = None,
    stop_at_sentence: bool = False,
) -> str:
    mc = MarkovChain(order=order, mode=mode)
    mc.train(text)
    return mc.generate(length=length, seed=seed, stop_at_sentence=stop_at_sentence)
