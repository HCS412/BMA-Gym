# models.py
"""
Core model architecture definitions for B&MA (Branch & Merge Autodidacticism).

Includes:
- Trunk model loader
- LoRA-based explorer clones
- Optional verifier model stubs
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType


class TrunkModel:
    def __init__(self, base_model_name="EleutherAI/gpt-neo-1.3B", device="cuda"):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(base_model_name).to(device)
        self.device = device
        self.model.eval()

    def generate(self, prompt, max_tokens=64):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class ExplorerClone:
    def __init__(self, trunk_model, rank=16):
        config = LoraConfig(
            r=rank,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],  # adjust as needed per architecture
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        self.model = get_peft_model(trunk_model.model, config)
        self.tokenizer = trunk_model.tokenizer
        self.device = trunk_model.device
        self.model.train()  # enable gradient flow for Roam phase

    def forward(self, prompt, labels=None):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        if labels:
            labels = self.tokenizer(labels, return_tensors="pt").input_ids.to(self.device)
            outputs = self.model(**inputs, labels=labels)
        else:
            outputs = self.model(**inputs)
        return outputs


# Optional: Verifier placeholder (expand if centralizing scoring models)
class VerifierModel:
    def __init__(self):
        # Placeholder; could be a classifier or entailment model
        pass

    def score(self, prompt, prediction):
        # Return dummy values for now
        return {
            "novelty": 0.5,
            "coherence": 0.8,
            "guardrail": 1.0
        }

