"""
fix_v8.py — Final cleanup to v9.
"""
import os

SRC = "ARIA_ICNABS_v8.tex"
DST = "ARIA_ICNABS_v9.tex"

if not os.path.exists(SRC):
    raise SystemExit(f"❌ {SRC} not found")

with open(SRC, 'r', encoding='utf-8') as f:
    tex = f.read()

fixes = []

# ============================================================
# FIX A: Duplicate sec:dt_refinement label
# ============================================================
# The 6.3 subsection should use a unique label
if r"\subsection{\(\Delta t\)-refinement study}" in tex:
    # Find this subsection and change its label
    idx = tex.find(r"\subsection{\(\Delta t\)-refinement study}")
    window_end = tex.find("\\subsection", idx + 50)
    if window_end > 0:
        chunk = tex[idx:window_end]
        if r"\label{sec:dt_refinement}" in chunk:
            new_chunk = chunk.replace(
                r"\label{sec:dt_refinement}",
                r"\label{sec:dt_refinement_study}"
            )
            tex = tex[:idx] + new_chunk + tex[window_end:]
            fixes.append("✅ FIX A: Duplicate label renamed (6.3 -> sec:dt_refinement_study)")

# ============================================================
# FIX B: Section 4.3 hard-coded "Table 5 and Figure 7"
# ============================================================
old_b = r"the results are summarized in Table 5 and Figure 7."
new_b = r"the results are summarized in Table~\ref{tab:effective_time} and Figure~\ref{fig:effective_time}."
if old_b in tex:
    tex = tex.replace(old_b, new_b)
    fixes.append("✅ FIX B: Section 4.3 references auto-resolved")

# Also fix any hard-coded "Table 4 and Figure 6" in 6.3
old_b2 = r"reported in Table 4 and visualized in Figure 6"
new_b2 = r"reported in Table~\ref{tab:dt_refinement} and visualized in Figure~\ref{fig:dt_refinement}"
if old_b2 in tex:
    tex = tex.replace(old_b2, new_b2)
    fixes.append("✅ FIX B2: Section 6.3 references auto-resolved")

# ============================================================
# FIX C: Abstract broken fPINN
# ============================================================
old_c = r"future \(\# \mathrm{PINN}\) work"
new_c = r"future fPINN work"
if old_c in tex:
    tex = tex.replace(old_c, new_c)
    fixes.append("✅ FIX C: Abstract fPINN typo fixed")
elif r"\# \mathrm{PINN}" in tex:
    tex = tex.replace(r"\# \mathrm{PINN}", "fPINN")
    fixes.append("✅ FIX C (variant): fPINN typo fixed")

# ============================================================
# FIX D: 'for the first time' in Section 1 after Contributions
# ============================================================
old_d = r"This quantifies, for the first time, the price of genuine non-locality in a neural-network solver."
new_d = r"This quantifies, to our knowledge for the first time, the price of genuine non-locality in a neural-network solver."
if old_d in tex:
    tex = tex.replace(old_d, new_d)
    fixes.append("✅ FIX D: 'for the first time' softened")

# ============================================================
# FIX E: 'quantitively' typo
# ============================================================
if "quantitively" in tex:
    tex = tex.replace("quantitively", "quantitatively")
    fixes.append("✅ FIX E: 'quantitively' -> 'quantitatively'")

# ============================================================
# FIX F: 'Finite-At regime' -> 'Finite-Delta-t regime'
# ============================================================
old_f = r"Remark 2 (Finite-At regime)"
new_f = r"Remark 2 (Finite-\(\Delta t\) regime)"
if old_f in tex:
    tex = tex.replace(old_f, new_f)
    fixes.append("✅ FIX F: 'Finite-At' -> 'Finite-Δt'")

# ============================================================
# FIX G: Figure 7 caption correction (effective-time)
# ============================================================
# The caption on page 13 was cut off as "igure 8"
old_g = r"igure 8: Accuracy- cost trade- off"
# This is likely PDF extraction artifact, no action needed

# ============================================================
# FIX H: check for broken table cells
# ============================================================
# Look for pattern of many "1" cells (indicating broken parsing)
# The actual .tex is fine; the PDF extraction was problematic

# ============================================================
# WRITE
# ============================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(tex)

print("=" * 70)
print("FIXES APPLIED")
print("=" * 70)
if fixes:
    for f_ in fixes:
        print(f"  {f_}")
else:
    print("  ⚠️  No fixes were applied")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)
checks = [
    (r"\label{sec:dt_refinement_study}", "Unique label for 6.3"),
    (r"Table~\ref{tab:effective_time}", "Section 4.3 auto-ref"),
    (r"future fPINN work", "Abstract fPINN fixed"),
    (r"to our knowledge for the first time", "Section 1 softened"),
    (r"quantitatively", "Typo fixed"),
    (r"Finite-\(\Delta t\) regime", "Remark 2 fixed"),
]
for pattern, label in checks:
    status = "✅" if pattern in tex else "❌"
    print(f"  {status} {label}")

# Check for duplicate labels
import re
labels = re.findall(r"\\label\{([^}]+)\}", tex)
from collections import Counter
dups = [k for k, v in Counter(labels).items() if v > 1]
if dups:
    print(f"\n  ⚠️  Duplicate labels remaining: {dups}")
else:
    print(f"\n  ✅ No duplicate labels")

print(f"\n✅ Output: {DST}")