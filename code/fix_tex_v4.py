"""
ARIA-ICNABS
File: fix_tex_v4.py
Purpose: Diagnose and fix remaining issues in ARIA_ICNABS_v4.tex.
         Outputs ARIA_ICNABS_v5.tex
"""
import os
import re

SRC = "ARIA_ICNABS_v4.tex"
DST = "ARIA_ICNABS_v5.tex"

if not os.path.exists(SRC):
    raise SystemExit(f"❌ {SRC} not found")

with open(SRC, 'r', encoding='utf-8') as f:
    tex = f.read()

print("=" * 70)
print("DIAGNOSTIC REPORT")
print("=" * 70)

# ============================================================
# 1. DIAGNOSE: duplicate intro paragraph
# ============================================================
needle = "We focus on the Atangana"
positions = []
start = 0
while True:
    idx = tex.find(needle, start)
    if idx < 0:
        break
    positions.append(idx)
    start = idx + 1

print(f"\n[1] Occurrences of 'We focus on the Atangana...': {len(positions)}")
if len(positions) >= 2:
    print(f"    First at char {positions[0]}")
    print(f"    Second at char {positions[1]}")
    print(f"    Distance: {positions[1] - positions[0]} chars")
    snippet = tex[positions[0]:positions[0]+300]
    print(f"    First 300 chars of first occurrence:")
    print(f"    {repr(snippet[:300])}")

# ============================================================
# 2. DIAGNOSE: typos
# ============================================================
print(f"\n[2] Typo search:")
for pattern in ["substantial more", "substantially more",
                "operat or", "archit ecture", "checkpoint,",
                "and it is dimensionless"]:
    count = tex.count(pattern)
    print(f"    '{pattern}': {count} occurrences")

# ============================================================
# 3. DIAGNOSE: Figure 6 block
# ============================================================
print(f"\n[3] Figure 6 block:")
idx = tex.find("fig06_mse_cost_bars")
if idx > 0:
    # find enclosing \begin{figure}
    begin = tex.rfind(r"\begin{figure}", 0, idx)
    end = tex.find(r"\end{figure}", idx) + len(r"\end{figure}")
    print(tex[begin:end])

# ============================================================
# APPLY FIXES
# ============================================================
fixes = []

# --- FIX A: remove duplicate intro paragraph ---
# The paragraph starts with "We focus on the Atangana" and ends with "of the form"
if len(positions) >= 2:
    # Find full extent of first occurrence (from "We focus" to end of paragraph before "of the form")
    p1 = positions[0]
    # Find the "of the form" after p1
    end1 = tex.find("of the form", p1)
    if end1 > 0:
        # Extend to include up to and including the period before the equation
        end1 = tex.find("\n", end1)  # end of that line
        # Remove this block (including trailing newline)
        removed = tex[p1:end1+1]
        tex = tex[:p1] + tex[end1+1:]
        fixes.append(f"✅ Removed duplicate intro paragraph ({len(removed)} chars)")

# --- FIX B: typo "substantial more" -> "substantially more" ---
n_before = tex.count("substantial more")
tex = tex.replace("substantial more epochs", "substantially more epochs")
tex = tex.replace("requires substantial more", "requires substantially more")
n_after = tex.count("substantial more")
if n_before != n_after:
    fixes.append(f"✅ Fixed 'substantial more' -> 'substantially more'")

# --- FIX C: typo "operator and it is dimensionless" ---
if "operator and it is dimensionless" in tex:
    tex = tex.replace("operator and it is dimensionless",
                      "operator and its dimensionless")
    fixes.append("✅ Fixed 'it is dimensionless' -> 'its dimensionless'")

# --- FIX D: Figure 6 - ensure it's not cropped ---
# Strategy: put Figure 6 on its own page and use full width again
idx6 = tex.find("fig06_mse_cost_bars")
if idx6 > 0:
    begin = tex.rfind(r"\begin{figure}", 0, idx6)
    end = tex.find(r"\end{figure}", idx6) + len(r"\end{figure}")
    old_block = tex[begin:end]
    # New: use 0.95\textwidth + center + ensure not overfull
    new_block = old_block.replace(
        r"\includegraphics[width=0.85\textwidth]{fig06_mse_cost_bars.pdf}",
        r"\includegraphics[width=0.95\textwidth]{fig06_mse_cost_bars.pdf}"
    )
    tex = tex[:begin] + new_block + tex[end:]
    fixes.append("✅ Figure 6 widened back to 0.95\\textwidth")

# --- FIX E: remove duplicate "8 Conclusion" line if source has it ---
# Search for literal doubled header
pattern = re.compile(r"(\\section\{Conclusion\})\s*\1", re.MULTILINE)
if pattern.search(tex):
    tex = pattern.sub(r"\1", tex)
    fixes.append("✅ Removed duplicate \\section{Conclusion}")

# Search for "Test 1: Kernel presence" literal duplicate
dup_test = r"\subsection{Test 1: Kernel presence}"
count_t1 = tex.count(dup_test)
if count_t1 >= 2:
    # Remove one
    first = tex.find(dup_test)
    second = tex.find(dup_test, first + 1)
    tex = tex[:second] + tex[second + len(dup_test):]
    fixes.append(f"✅ Removed duplicate subsection: Test 1")

dup_test2 = r"\subsection{Test 2: \(\Delta t\)-refinement}"
count_t2 = tex.count(dup_test2)
if count_t2 >= 2:
    first = tex.find(dup_test2)
    second = tex.find(dup_test2, first + 1)
    tex = tex[:second] + tex[second + len(dup_test2):]
    fixes.append(f"✅ Removed duplicate subsection: Test 2")

# --- FIX F: Put Figure 6 on its own page to avoid cropping ---
# Add \clearpage before figure 6's block
idx6 = tex.find("fig06_mse_cost_bars")
if idx6 > 0:
    begin = tex.rfind(r"\begin{figure}", 0, idx6)
    # Insert \clearpage before, if not already there
    before = tex[max(0, begin-30):begin]
    if "clearpage" not in before and "newpage" not in before:
        tex = tex[:begin] + "\\clearpage\n" + tex[begin:]
        fixes.append("✅ Added \\clearpage before Figure 6")

# ============================================================
# WRITE
# ============================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(tex)

print("\n" + "=" * 70)
print("FIXES APPLIED")
print("=" * 70)
if fixes:
    for f_ in fixes:
        print(f"  {f_}")
else:
    print("  ⚠️  No fixes applied (all patterns already correct?)")

print(f"\n✅ Output: {DST}")
print(f"\nNext steps:")
print(f"  pdflatex {DST}")
print(f"  pdflatex {DST}")