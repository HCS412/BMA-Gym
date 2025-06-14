# train_loop.py

from models import TrunkModel, LoRAAdapter
from tasks import CuriositySampler, generate_task
from debate import DebateEntry, Verifier, DebateSession
from merge import merge_adapters
from diary import DiaryManager
import random
import uuid

# --- Config ---
NUM_CLONES = 200
ROAM_STEPS = 4
TOP_K = 25

def run_one_cycle():
    print("\n--- B&MA Daily Cycle Start ---")

    # Initialize Trunk Model
    trunk = TrunkModel(name="baseline_gpt")
    base_weights = trunk.get_weights()

    # Fork clones with adapters
    clones = {}
    for i in range(NUM_CLONES):
        adapter_id = f"clone_{i}_{uuid.uuid4().hex[:6]}"
        adapter = LoRAAdapter(base_weights)
        clones[adapter_id] = adapter

    # Roam: Sample tasks and generate diary entries
    diaries = {}
    for clone_id, adapter in clones.items():
        diary = []
        sampler = CuriositySampler(adapter)
        for step in range(ROAM_STEPS):
            prompt = generate_task(sampler)
            cot = f"Chain-of-thought for {prompt}"
            prediction = adapter.forward(prompt)
            loss = random.uniform(0.0, 1.0)  # Fake loss
            uncertainty = random.uniform(0.0, 1.0)  # Fake uncertainty
            entry = DebateEntry(prompt, cot, prediction, loss, uncertainty)
            diary.append(entry)
        diaries[clone_id] = diary

    # Save diaries
    DiaryManager.save_all(diaries)

    # Debate & Vet
    verifier = Verifier(guardrails=["unsafe", "bias"])
    debate = DebateSession(diaries, verifier)
    debate.run()
    top_clones = debate.top_k(TOP_K)
    annotations = debate.get_annotations()

    # Merge
    winning_adapters = [clones[cid] for cid in top_clones]
    new_weights = merge_adapters(base_weights, winning_adapters)
    trunk.load_weights(new_weights)

    print("Top Clones:", top_clones)
    print("\n--- B&MA Daily Cycle Complete ---")

if __name__ == '__main__':
    run_one_cycle()
