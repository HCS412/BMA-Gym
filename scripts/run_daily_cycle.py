# run_daily_cycle.py
from fork import fork_clones
from roam import run_roam
from debate import select_top_clones
from merge import merge_into_trunk
import json

# Load dummy model and data
class DummyModel:
    def __init__(self): self.hidden_size = 768

with open("../benchmarks/symbol_swap_example.jsonl") as f:
    pool = [json.loads(line) for line in f]

# Step 1: Fork
trunk = DummyModel()
clones = fork_clones(trunk)

# Step 2: Roam
for clone in clones:
    run_roam(clone, pool)

# Step 3: Debate
top_clones = select_top_clones(clones)

# Step 4: Merge
trunk = merge_into_trunk(trunk, top_clones)
