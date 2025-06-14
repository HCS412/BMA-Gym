# fork.py
import torch
import copy

def fork_clones(trunk_model, num_clones=200, adapter_rank=16):
    clones = []
    for _ in range(num_clones):
        adapter = torch.nn.Linear(trunk_model.hidden_size, trunk_model.hidden_size)  # placeholder LoRA
        clone = {
            "trunk": copy.deepcopy(trunk_model),
            "adapter": adapter,
            "diary": []
        }
        clones.append(clone)
    return clones
