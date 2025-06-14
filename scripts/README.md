# BMA-Gym Scripts

This folder contains runnable prototypes of the Branch & Merge Autodidacticism (B&MA) pipeline.

Each component is modular and corresponds to a step in the B&MA cycle:
- `fork.py`: Generates LoRA adapters ("explorer clones")
- `roam.py`: Performs curiosity-driven task sampling and diary logging
- `debate.py`: Runs clone debates and scoring
- `merge.py`: Integrates top-performing updates into the trunk

See `run_daily_cycle.py` for a stitched-together example of one full day.
