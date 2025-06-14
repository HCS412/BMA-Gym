# merge.py

import hashlib
import numpy as np
from typing import Dict, List, Tuple

class Adapter:
    def __init__(self, delta_weights: Dict[str, np.ndarray], gate: float = 1.0):
        self.delta_weights = delta_weights  # dict of layer_name -> delta tensor
        self.gate = gate

    def scale(self, alpha: float):
        for k in self.delta_weights:
            self.delta_weights[k] *= alpha * self.gate

class TrunkModel:
    def __init__(self, weights: Dict[str, np.ndarray]):
        self.weights = weights
        self.history = []

    def apply_merge(self, adapters: List[Adapter], rollback_threshold: float, val_loss_fn) -> bool:
        # Store original weights
        original = {k: v.copy() for k, v in self.weights.items()}
        self.history.append(original)

        # Merge in
        for adapter in adapters:
            for layer, delta in adapter.delta_weights.items():
                if layer in self.weights:
                    self.weights[layer] += delta
                else:
                    self.weights[layer] = delta.copy()

        # Validate and possibly rollback
        val_loss = val_loss_fn(self.weights)
        print(f"Validation loss after merge: {val_loss:.4f}")

        if val_loss > rollback_threshold:
            print("Rolling back due to validation drop.")
            self.weights = original
            return False
        return True

    def hash_weights(self) -> str:
        """Generate Merkle-like root from weights for audit logging."""
        concat = b"".join([v.tobytes() for k, v in sorted(self.weights.items())])
        return hashlib.sha256(concat).hexdigest()

    def log_audit(self, val_loss: float, filepath: str):
        with open(filepath, 'a') as f:
            audit_line = f"Hash: {self.hash_weights()} | Val Loss: {val_loss:.4f}\n"
            f.write(audit_line)
            print(f"Logged audit: {audit_line.strip()}")


def weighted_merge(adapters: List[Adapter], alphas: List[float]) -> List[Adapter]:
    for adapter, alpha in zip(adapters, alphas):
        adapter.scale(alpha)
    return adapters


def dummy_val_loss(weights: Dict[str, np.ndarray]) -> float:
    """Mock validation loss function for demonstration purposes."""
    return np.random.uniform(0.0, 1.0)  # Simulate val loss


# Example usage:
if __name__ == "__main__":
    base_weights = {"layer1": np.ones((3, 3)), "layer2": np.ones((2, 2))}
    trunk = TrunkModel(weights=base_weights)

    adapters = [
        Adapter(delta_weights={"layer1": np.random.randn(3, 3), "layer2": np.random.randn(2, 2)}, gate=1.0),
        Adapter(delta_weights={"layer1": np.random.randn(3, 3), "layer2": np.random.randn(2, 2)}, gate=0.8)
    ]

    alphas = [0.6, 0.4]
    adapters = weighted_merge(adapters, alphas)

    merged = trunk.apply_merge(adapters, rollback_threshold=0.7, val_loss_fn=dummy_val_loss)
    if merged:
        trunk.log_audit(val_loss=dummy_val_loss(trunk.weights), filepath="merge_audit.log")
