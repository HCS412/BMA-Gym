# debate.py
import heapq

def verifier_score(entry):
    return 0.7 * (1 - entry['loss']) + 0.3 * (1 - entry['uncertainty'])

def select_top_clones(clones, top_k=25):
    scored = []
    for idx, clone in enumerate(clones):
        avg_score = sum(verifier_score(e) for e in clone['diary']) / len(clone['diary'])
        scored.append((avg_score, idx))
    top = heapq.nlargest(top_k, scored)
    return [clones[i] for _, i in top]
