"""
ARIA-ICNABS
File: fix_tex_v3.py
Purpose: Fix the 6 issues found in ARIA_ICNABS_v3_with_figures.tex
         Creates ARIA_ICNABS_v4.tex (final version)
"""
import os
import re

SRC = "ARIA_ICNABS_v3_with_figures.tex"
DST = "ARIA_ICNABS_v4.tex"

if not os.path.exists(SRC):
    print(f"❌ {SRC} not found")
    raise SystemExit(1)

with open(SRC, 'r', encoding='utf-8') as f:
    tex = f.read()

fixes_log = []

# ============================================================
# FIX 1: Remove duplicate intro paragraph
# ============================================================
dup = r"""We focus on the Atangana--Baleanu--Caputo (ABC) derivative \cite{Atangana2016}, which is characterized by a non-singular, non-local Mittag-Leffler kernel. The ABC operator and its modified variant (MABC) have been applied to advection-dispersion models \cite{AzZobi2025, Chawla2022} and to PINN frameworks \cite{AzZobi2025}. In several of these works, the time-fractional derivative is discretized with a two-point finite difference of the form"""
if tex.count(dup) >= 2:
    # Remove first occurrence; keep second
    first_idx = tex.find(dup)
    second_idx = tex.find(dup, first_idx + len(dup))
    tex = tex[:first_idx] + tex[second_idx:]
    fixes_log.append("✅ FIX 1: Removed duplicate intro paragraph")

# ============================================================
# FIX 2: Figure 6 -> use 0.85\textwidth instead of \textwidth
# ============================================================
old_fig6 = r"\includegraphics[width=\textwidth]{fig06_mse_cost_bars.pdf}"
new_fig6 = r"\includegraphics[width=0.85\textwidth]{fig06_mse_cost_bars.pdf}"
if old_fig6 in tex:
    tex = tex.replace(old_fig6, new_fig6)
    fixes_log.append("✅ FIX 2: Figure 6 width reduced")

# ============================================================
# FIX 3: Figure 5 caption — note seed 42 explicitly
# ============================================================
old_cap5 = r"The naive FD residual achieves the lowest maximum error ($5.7 \times 10^{-3}$), followed by Caputo-L1 ($7.6 \times 10^{-3}$) and ABC-L1 ($1.2 \times 10^{-2}$)."
new_cap5 = r"Shown for a single representative seed (42). Across all three seeds, the mean maximum errors are $5.7 \times 10^{-3}$ (naive FD), $7.6 \times 10^{-3}$ (Caputo-L1), and $1.2 \times 10^{-2}$ (ABC-L1)."
if old_cap5 in tex:
    tex = tex.replace(old_cap5, new_cap5)
    fixes_log.append("✅ FIX 3: Figure 5 caption clarified")

# ============================================================
# FIX 4: Duplicate subsection headers (if present as literal text)
# ============================================================
# Look for duplicated \subsection lines
pattern = r"(\\subsection\{Test 1: Kernel presence\}\s*\n)(\s*\\subsection\{Test 1: Kernel presence\}\s*\n)"
if re.search(pattern, tex):
    tex = re.sub(pattern, r"\1", tex, count=1)
    fixes_log.append("✅ FIX 4: Removed duplicate Test 1 subsection header")

pattern = r"(\\subsection\{Test 2: \$\\Delta t\$-refinement\}\s*\n)(\s*\\subsection\{Test 2: \$\\Delta t\$-refinement\}\s*\n)"
if re.search(pattern, tex):
    tex = re.sub(pattern, r"\1", tex, count=1)
    fixes_log.append("✅ FIX 4b: Removed duplicate Test 2 subsection header")

# ============================================================
# FIX 5: Typo fixes
# ============================================================
typo_fixes = [
    ("requires substantial more epochs", "requires substantially more epochs"),
    ("operator and it is dimensionless transport ratio", "operator and its dimensionless transport ratio"),
    ("The three test s together", "The three tests together"),
]
for old, new in typo_fixes:
    if old in tex:
        tex = tex.replace(old, new)
        fixes_log.append(f"✅ FIX 5: Typo fixed: '{old[:40]}...'")

# ============================================================
# FIX 6: Code availability placeholder
# ============================================================
old_code = r"All code, reference solutions, PINN checkpoints, and figure-generation scripts are available at \url{https://github.com/[USERNAME]/ARIA-ICNABS} (to be deposited on Zenodo upon acceptance)."
new_code = r"All code, reference solutions, PINN checkpoints, and figure-generation scripts, together with the exact parameter values used in all experiments, are available from the corresponding author upon reasonable request, and will be deposited on Zenodo upon acceptance."
if old_code in tex:
    tex = tex.replace(old_code, new_code)
    fixes_log.append("✅ FIX 6: Code availability reworded")

# ============================================================
# WRITE
# ============================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(tex)

print("=" * 60)
print("FIXES APPLIED")
print("=" * 60)
for log in fixes_log:
    print(f"  {log}")

print(f"\n✅ Output: {DST}")
print(f"\nNext step:")
print(f"  pdflatex {DST}")
print(f"  pdflatex {DST}   # for references")