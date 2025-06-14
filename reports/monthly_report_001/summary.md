# B&MA Monthly Report — Cycle 001 (April 2025)

## 🌟 Highlights
- Symbol Swap accuracy: **+22.3pp** over best baseline
- Verifier recall stable across 4 debate rounds per day
- Quiet Epoch reduced forgetting by **28.4%**
- Total compute: 336 GPU-hours (~1.4kWh/day × 24 days)

## 🧠 Performance Metrics
- **Symbol Swap**: 68.4%
- **Logic Grid**: 64.2%
- **GSM-Hard**: 45.0%
- MMLU: 57.3%
- CodeParrot++: 62.9%

## 🔍 Debate + Merge Overview
- Debate rounds: 96 total
- Avg verifier agreement: 82%
- Merged adapters this month: 74
- Rollback events: 2 (due to >0.3pp drop)

## ⚙️ System Profile
- 8×A100, 40GB
- Avg GPU util: 71% Roam, 18% Debate
- Energy: 1.4kWh/day
- Adapter storage footprint: 2.1GB (LoRA, N=256)

## 🔐 Alignment + Replay
- Guardrail violations: 0.8%
- SHA digest match on 100% of diaries
- Merkle root archived: `12d4ac...9a1e6f`
