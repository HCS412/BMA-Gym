import json
import random

SYMBOLS = ['@', '#', '$', '%', '&', '*']
WORDS = ['apple', 'banana', 'carrot', 'date', 'fig', 'grape']

def generate_example():
    mapping = dict(zip(random.sample(SYMBOLS, 3), random.sample(WORDS, 3)))
    reverse_mapping = {v: k for k, v in mapping.items()}

    sentence = f"The {mapping['@']} is red, the {mapping['#']} is yellow, and the {mapping['$']} is orange."
    target_question = f"What symbol represents banana?"
    answer = reverse_mapping.get('banana', 'unknown')

    return {
        "input": sentence + " " + target_question,
        "label": answer,
        "mapping": mapping  # For debugging only
    }

def generate_dataset(n=10, out_file='symbol_swap_example.jsonl'):
    with open(out_file, 'w') as f:
        for _ in range(n):
            ex = generate_example()
            f.write(json.dumps(ex) + '\n')

if __name__ == "__main__":
    generate_dataset()
