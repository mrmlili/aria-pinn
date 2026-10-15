# ARIA-PINN

A Diagnostic Framework for Detecting False Fractionalization in Physics-Informed Neural Networks.

**Author:** Maryam Jalili (mrmjlili@iau.ac.ir)
**Affiliation:** Department of Mathematics, Neyshabur Branch, Islamic Azad University, Neyshabur, Iran

---

## Overview

This repository contains the code, data, and manuscript for a study on
fractional derivative discretizations in Physics-Informed Neural Networks
(PINNs).

We introduce a **three-test diagnostic protocol** (kernel-presence,
Δt-refinement, effective-time) to detect whether a PINN residual genuinely
preserves the non-local memory of the fractional operator, or silently
reduces to a local surrogate.

---

## Key results (α = 0.8, 3 seeds)

| Residual  | MSE (mean ± std)      | Time (s) |
|-----------|-----------------------|----------|
| Naive FD  | 3.04e-6 ± 1.42e-6     | 216      |
| Caputo-L1 | 6.19e-6 ± 0.72e-6     | 2327     |
| ABC-L1    | 4.19e-5 ± 9.17e-6     | 2968     |

At **α = 0.5**, the ranking changes: Caputo-L1 outperforms Naive FD.

See the manuscript (in `paper/`) for full analysis, limitations, and
discussion of the cross-PDE nature of the MSE ratios.

---

## Repository structure

- `paper/` — LaTeX source (`ARIA_PINN.tex`) and final PDF
- `code/` — Python scripts (training, reference solvers, figure generation)
- `data/` — Reference solutions and PINN results (`.npz` files)
- `figures/` — Figure PDFs

---

## IMPORTANT: Pre-computed data included

All training results and reference solutions are already included in
`data/`. You do **not** need to re-run training scripts unless reproducing
from scratch.

To regenerate figures, run the `fig*.py` scripts in `code/`.

---

## Requirements

- Python 3.10+
- PyTorch (CPU), NumPy, SciPy, Matplotlib

Install:


pip install torch numpy scipy matplotlib
