# roam.py
import random
import json

def sample_task(input_pool):
    return random.choice(input_pool)

def run_roam(clone, task_pool, steps=5):
    for _ in range(steps):
        task = sample_task(task_pool)
        # Simulate uncertainty score + fake prediction
        pred = "[PRED]"
        loss = random.uniform(0.1, 1.0)
        uncertainty = random.uniform(0.0, 1.0)
        diary_entry = {
            "input": task['input'],
            "label": task['label'],
            "pred": pred,
            "loss": loss,
            "uncertainty": uncertainty
        }
        clone["diary"].append(diary_entry)
