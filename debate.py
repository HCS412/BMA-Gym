# debate.py

import random
import hashlib
import numpy as np
from typing import List, Dict, Tuple

class DebateEntry:
    def __init__(self, prompt: str, cot: str, prediction: str, loss: float, uncertainty: float):
        self.prompt = prompt
        self.cot = cot
        self.prediction = prediction
        self.loss = loss
        self.uncertainty = uncertainty

    def hash(self) -> str:
        entry_str = f"{self.prompt}{self.cot}{self.prediction}"
        return hashlib.sha256(entry_str.encode()).hexdigest()


class Verifier:
    def __init__(self, guardrails: List[str] = None):
        self.guardrails = guardrails or []

    def score_novelty(self, entry: DebateEntry, seen_hashes: set) -> float:
        return 1.0 if entry.hash() not in seen_hashes else 0.0

    def score_coherence(self, entry: DebateEntry) -> float:
        # Placeholder: a real model would compute semantic coherence
        return 1.0 - entry.loss

    def check_guardrails(self, entry: DebateEntry) -> bool:
        for rule in self.guardrails:
            if rule.lower() in entry.prediction.lower():
                return False
        return True

    def evaluate(self, diary: List[DebateEntry], seen_hashes: set) -> Tuple[float, float, bool]:
        novelty_scores = [self.score_novelty(e, seen_hashes) for e in diary]
        coherence_scores = [self.score_coherence(e) for e in diary]
        guardrail_compliance = all(self.check_guardrails(e) for e in diary)

        novelty = np.mean(novelty_scores)
        coherence = np.mean(coherence_scores)
        return novelty, coherence, guardrail_compliance


class DebateSession:
    def __init__(self, clone_diaries: Dict[str, List[DebateEntry]], verifier: Verifier):
        self.clone_diaries = clone_diaries
        self.verifier = verifier
        self.scores = {}
        self.seen_hashes = set()

    def run(self):
        for clone_id, diary in self.clone_diaries.items():
            novelty, coherence, guardrail_ok = self.verifier.evaluate(diary, self.seen_hashes)
            score = novelty * 0.4 + coherence * 0.6
            if not guardrail_ok:
                score *= 0.5  # Penalize violations
            self.scores[clone_id] = score
            for entry in diary:
                self.seen_hashes.add(entry.hash())

    def top_k(self, k: int) -> List[str]:
        return sorted(self.scores, key=self.scores.get, reverse=True)[:k]

    def report(self) -> None:
        print("Debate Session Results:")
        for clone_id, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            print(f"Clone {clone_id}: Score = {score:.3f}")
