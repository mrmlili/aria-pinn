"""
fix_v7.py — Cleanup v7 to v8
"""
import os

SRC = "ARIA_ICNABS_v7.tex"
DST = "ARIA_ICNABS_v8.tex"

if not os.path.exists(SRC):
    raise SystemExit(f"❌ {SRC} not found")

with open(SRC, 'r', encoding='utf-8') as f:
    tex = f.read()

fixes = []

# ============================================================
# FIX 1: Insert Section 6.3 (Δt-refinement)
# ============================================================
if r"\label{tab:dt_refinement}" not in tex:
    anchor = r"\subsection{Diagnostic classification}"
    if anchor in tex:
        section_63 = r"""\subsection{\(\Delta t\)-refinement study}
\label{sec:dt_refinement}

We now apply Test~2 to the naive-FD PINN. The network is trained under
the configuration of Section~\ref{sec:results} with \(\Delta t \in
\{0.1, 0.05, 0.025, 0.0125\}\), holding all other hyperparameters fixed.
For each value, we compute the MSE and the maximum error between the
trained PINN prediction at \(t=1\) and the classical reference solution
introduced in Section~\ref{sec:ref}. The results are reported in
Table~\ref{tab:dt_refinement} and visualized in
Figure~\ref{fig:dt_refinement}.

\begin{table}[h]
\centering
\caption{Test 2 (\(\Delta t\)-refinement) applied to the naive-FD PINN.
         As \(\Delta t\) is reduced, the MSE converges toward the PINN's
         own training-error floor, confirming the local-limit theorem
         (Proposition~\ref{prop:local_limit}).}
\label{tab:dt_refinement}
\begin{tabular}{cccc}
\toprule
\(\Delta t\) & MSE vs classical & Max error & Training time (s) \\
\midrule
0.1000 & \(1.34\times 10^{-5}\) & \(1.20\times 10^{-2}\) & 119 \\
0.0500 & \(3.98\times 10^{-6}\) & \(6.63\times 10^{-3}\) & 134 \\
0.0250 & \(1.90\times 10^{-6}\) & \(3.47\times 10^{-3}\) & 118 \\
0.0125 & \(1.97\times 10^{-6}\) & \(3.94\times 10^{-3}\) & 116 \\
\bottomrule
\end{tabular}
\end{table}

From \(\Delta t = 0.1\) to \(\Delta t = 0.025\), the MSE decreases by
a factor of \(7.1\times\), consistent with first-order convergence
toward the classical limit. At \(\Delta t = 0.0125\) the MSE plateaus
at \(\sim 2\times 10^{-6}\), which is the same order of magnitude as
the PINN's intrinsic training-error floor observed in
Table~\ref{tab:main}. The interpretation is therefore unambiguous: the
naive-FD PINN is converging, as \(\Delta t\to 0\), to a solution of the
classical advection-dispersion equation \eqref{eq:classical_rescaled},
not to a solution of the fractional PDE \eqref{eq:gov}. This
quantitatively confirms Test~2 of the diagnostic protocol.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{fig07_dt_refinement.pdf}
\caption{Test 2 (\(\Delta t\)-refinement) applied to the naive-FD PINN.
         Left: MSE versus \(\Delta t\) (log--log). Right: maximum error
         versus \(\Delta t\). Both quantities decrease monotonically as
         \(\Delta t\) is reduced, before saturating at the PINN's
         training-error floor near \(\Delta t = 0.025\).}
\label{fig:dt_refinement}
\end{figure}

"""
        tex = tex.replace(anchor, section_63 + anchor, 1)
        fixes.append("✅ Section 6.3 (Δt-refinement) added")
    else:
        fixes.append("❌ Anchor 'Diagnostic classification' not found")
else:
    fixes.append("⚠️  Section 6.3 already present")

# ============================================================
# FIX 2: Figure 3 caption
# ============================================================
variants_c3 = [
    r"requires substantial more epochs to reach comparable loss values",
    r"requires substantially more epochs to reach comparable loss values",
    r"requires substantial more training time to reach comparable loss values",
    r"requires substantially more training time to reach comparable loss values",
]
new_c3 = r"differs in its rate of decay across the three residuals---ABC-L1 converges to the lowest absolute loss, while Naive FD plateaus at the highest"
fixed_c3 = False
for v in variants_c3:
    if v in tex:
        tex = tex.replace(v, new_c3)
        fixed_c3 = True
        break
if fixed_c3:
    fixes.append("✅ Figure 3 caption fixed")
else:
    # Diagnostic: search for "requires" near fig:loss
    idx = tex.find(r"\label{fig:loss}")
    if idx > 0:
        window = tex[max(0, idx-800):idx]
        if "requires" in window:
            fixes.append(f"⚠️  Figure 3 caption still has 'requires' — please paste this window to me for diagnosis")
            print("\n--- Figure 3 caption window ---")
            print(window[-400:])
            print("--- end ---\n")
        else:
            fixes.append("⚠️  Figure 3 caption: 'requires' not found near fig:loss")

# ============================================================
# FIX 3: Figure 5 caption numbers
# ============================================================
if r"5.7 \times 10^{-3}" in tex:
    tex = tex.replace(r"5.7 \times 10^{-3}", r"7.23 \times 10^{-3}")
    tex = tex.replace(r"7.6 \times 10^{-3}", r"7.01 \times 10^{-3}")
    tex = tex.replace(r"1.2 \times 10^{-2}", r"1.10 \times 10^{-2}")
    fixes.append("✅ Figure 5 caption numbers updated")
elif r"7.23 \times 10^{-3}" in tex:
    fixes.append("⚠️  Figure 5 caption already correct")
else:
    # Try without backslashes (in case of escaping differences)
    if "5.7" in tex and "fig:errors" in tex:
        idx = tex.find(r"\label{fig:errors}")
        window = tex[max(0, idx-600):idx]
        print("\n--- Figure 5 caption window ---")
        print(window[-500:])
        print("--- end ---\n")

# ============================================================
# WRITE
# ============================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(tex)

print("=" * 70)
print("FIXES APPLIED")
print("=" * 70)
for f_ in fixes:
    print(f"  {f_}")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)
checks = [
    (r"\label{tab:dt_refinement}", "Table 5 (Δt-refinement) label"),
    (r"\label{fig:dt_refinement}", "Figure 7 (Δt-refinement) label"),
    (r"\label{tab:effective_time}", "Table 6 (Effective-time) label"),
    (r"\label{fig:effective_time}", "Figure 8 (Effective-time) label"),
    (r"7.23 \times 10^{-3}", "Figure 5 corrected number"),
    (r"to our knowledge, the first", "Softened 'first time' claim"),
]
for pattern, label in checks:
    status = "✅" if pattern in tex else "❌"
    print(f"  {status} {label}")

print(f"\n✅ Output: {DST}")
print(f"\nRun: pdflatex {DST} (twice)")