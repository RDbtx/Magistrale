# MLSECproject

## RobustBench Re-evaluation with AutoAttack across ε (CIFAR-10, ℓ∞)

This project consists of selecting **five CIFAR-10 (ℓ∞)** models from **RobustBench** and **re-evaluating** them with *
*AutoAttack** under multiple perturbation radii **ε**. We sweep ε from **1/255 to 16/255** at regular intervals and
include the standard reference point **8/255**, using a **subset of 100–200 CIFAR-10 test samples**.

The objective is to measure how robust accuracy changes as ε increases, and to study how model **rankings** change
across ε values. In particular, we evaluate the **stability of rankings**: whether the ordering observed at a single
baseline ε (as commonly shown in RobustBench leaderboards) remains consistent when ε is smaller or larger. We then
highlight cases where the ranking changes significantly and discuss what this implies about how reliable a single-ε
leaderboard is for describing overall robustness.

---

## Project Overview

The pipeline loads the chosen RobustBench models and a reproducible random subset of the CIFAR-10 test set, then runs
AutoAttack for a fixed ε grid (by default `1/255`, `4/255`, `8/255`, `12/255`, `16/255`). For each model and ε, the
program records robust accuracy together with basic runtime/configuration metadata, and saves the results both as a full
JSON file and as a CSV table (models × ε). From the CSV, the project generates plots showing robust accuracy curves,
rank-vs-ε trends, and an accuracy heatmap ordered by average rank. If provided, the plots can also overlay RobustBench
reference values at `8/255` to visually compare reported performance against our re-evaluation.

---

## Environment setup

Install dependencies with:

- `pip install torch torchvision torchaudio`
- `pip install robustbench`
- `pip install numpy pandas matplotlib scipy`
- `pip install git+https://github.com/fra31/auto-attack`

> Depending on your machine, you may need a platform-specific PyTorch install command to enable CUDA or Apple Silicon
> MPS support.
