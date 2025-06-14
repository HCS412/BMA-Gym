# tasks.py
"""
Defines symbolic benchmark tasks for BMA-Gym, such as Symbol Swap, Logic Grid,
and GSM-Hard. Each task class provides a `sample()` method returning a prompt
and ground-truth answer.
"""

import random


class SymbolSwapTask:
    """
    Toy benchmark where symbols (e.g., A, B, C) are mapped to words.
    Tests logical consistency and reasoning with aliasing.
    """
    def __init__(self):
        self.symbol_map = {
            'A': 'apple',
            'B': 'banana',
            'C': 'carrot'
        }

    def sample(self):
        # Random substitution
        prompt = "If A is B and B is C, what is A?"
        answer = "carrot"
        return prompt, answer


class LogicGridTask:
    """
    Mimics logic puzzles (e.g., "Tom has blue shoes, Jane has red shoes...").
    Requires deduction.
    """
    def __init__(self):
        self.setups = [
            ("Tom wears blue, Jane wears red. Who wears blue?", "Tom"),
            ("If Alex is older than Sam, and Sam is older than Max, who is oldest?", "Alex")
        ]

    def sample(self):
        return random.choice(self.setups)


class GSMHardTask:
    """
    Hard math QA examples like those in GSM8K.
    """
    def __init__(self):
        self.examples = [
            ("If 5 apples cost $3, how much do 15 apples cost?", "$9"),
            ("There are 24 students in a class. If 3/4 are present, how many are absent?", "6")
        ]

    def sample(self):
        return random.choice(self.examples)


def load_task(name):
    """Factory function to load a named task."""
    if name == "symbol_swap":
        return SymbolSwapTask()
    elif name == "logic_grid":
        return LogicGridTask()
    elif name == "gsm_hard":
        return GSMHardTask()
    else:
        raise ValueError(f"Unknown task name: {name}")
