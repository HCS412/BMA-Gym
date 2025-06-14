# diary.py

import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

class DiaryEntry:
    def __init__(self, prompt: str, cot: str, prediction: str, loss: float, uncertainty: float, todo: Optional[str] = None):
        self.timestamp = datetime.utcnow().isoformat()
        self.prompt = prompt
        self.cot = cot
        self.prediction = prediction
        self.loss = loss
        self.uncertainty = uncertainty
        self.todo = todo or ""

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "cot": self.cot,
            "prediction": self.prediction,
            "loss": self.loss,
            "uncertainty": self.uncertainty,
            "todo": self.todo,
            "hash": self.hash()
        }

    def hash(self) -> str:
        entry_str = f"{self.prompt}{self.cot}{self.prediction}"
        return hashlib.sha256(entry_str.encode()).hexdigest()


class Diary:
    def __init__(self, clone_id: str, save_dir: str = "logs/diaries"):
        self.clone_id = clone_id
        self.entries: List[DiaryEntry] = []
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def add_entry(self, entry: DiaryEntry):
        self.entries.append(entry)

    def flush_to_file(self):
        filepath = os.path.join(self.save_dir, f"diary_{self.clone_id}.json")
        with open(filepath, 'w') as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=2)
        print(f"Diary flushed to {filepath} with {len(self.entries)} entries.")

    def compress(self) -> Dict[str, float]:
        """Return summary statistics: average loss and uncertainty."""
        if not self.entries:
            return {"avg_loss": 0.0, "avg_uncertainty": 0.0}

        total_loss = sum(e.loss for e in self.entries)
        total_uncertainty = sum(e.uncertainty for e in self.entries)
        return {
            "avg_loss": total_loss / len(self.entries),
            "avg_uncertainty": total_uncertainty / len(self.entries)
        }

    def latest_entry(self) -> Optional[DiaryEntry]:
        return self.entries[-1] if self.entries else None

    def load_from_file(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        self.entries = [DiaryEntry(**entry) for entry in data]

    def summarize_todo_list(self) -> List[str]:
        return [entry.todo for entry in self.entries if entry.todo]

    def __len__(self):
        return len(self.entries)

# Example usage:
if __name__ == "__main__":
    diary = Diary(clone_id="clone_42")
    diary.add_entry(DiaryEntry(prompt="2+2", cot="Think of apples", prediction="4", loss=0.01, uncertainty=0.02))
    diary.add_entry(DiaryEntry(prompt="3*3", cot="Like a tic-tac-toe board", prediction="9", loss=0.05, uncertainty=0.01, todo="Double check chain-of-thought"))
    diary.flush_to_file()
    print("Compressed summary:", diary.compress())
    print("Todos:", diary.summarize_todo_list())
