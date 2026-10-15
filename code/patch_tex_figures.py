"""
ARIA-ICNABS
File: patch_tex_figures.py
Purpose: Insert 6 figure environments into ARIA_ICNABS_v3.tex at proper locations.
         Creates ARIA_ICNABS_v3_with_figures.tex (does not overwrite original).
"""
import os
import shutil

SRC = "ARIA_ICNABS_v3.tex"
DST = "ARIA_ICNABS_v3_with_figures.tex"

# ============================================================
# FIGURE BLOCKS
# ============================================================
FIG01 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{fig01_protocol_flowchart.pdf}
\caption{The three-test diagnostic protocol for detecting false fractionalization in PINN residuals. A residual that fails Test~1 (no kernel present), passes Test~2 (converges to the classical limit as $\Delta t \to 0$), and passes Test~3 (matches the effective-time prediction) is classified as a \emph{local surrogate}.}
\label{fig:protocol}
\end{figure}
"""

FIG02 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{fig02_reference_comparison.pdf}
\caption{Reference solutions at $t=T=1$ for the three discretizations of the same PDE: the classical limit (solid), Caputo-L1 with power-law kernel (dashed), and ABC-L1 with Mittag-Leffler kernel (dash-dot). The three profiles differ substantially, confirming that the three residuals are not interchangeable.}
\label{fig:references}
\end{figure}
"""

FIG03 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{fig03_training_loss.pdf}
\caption{Training loss histories for the three residuals (mean over 3 random seeds; shaded region indicates min--max range). All three curves decrease monotonically, but the ABC-L1 residual requires substantially more epochs to reach comparable loss values.}
\label{fig:loss}
\end{figure}
"""

FIG04 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig04_solution_comparison.pdf}
\caption{PINN prediction (black dashed) versus reference solution (colored solid) at $t=1$ for each of the three residuals. Left: naive FD (local). Middle: Caputo-L1 (power-law). Right: ABC-L1 (Mittag-Leffler). All three PINNs reproduce the qualitative shape of their respective reference, but the quantitative agreement degrades with operator complexity.}
\label{fig:solution}
\end{figure}
"""

FIG05 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig05_error_profiles.pdf}
\caption{Pointwise absolute error profiles $|C_{\mathrm{PINN}}(x,1) - C_{\mathrm{ref}}(x,1)|$ for the three residuals. The naive FD residual achieves the lowest maximum error ($5.7 \times 10^{-3}$), followed by Caputo-L1 ($7.6 \times 10^{-3}$) and ABC-L1 ($1.2 \times 10^{-2}$).}
\label{fig:errors}
\end{figure}
"""

FIG06 = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{fig06_mse_cost_bars.pdf}
\caption{Accuracy--cost trade-off across the three residuals. Left: MSE (mean $\pm$ std over 3 seeds, log scale). Right: training time. The price of genuine non-locality is quantified: Caputo-L1 is $2.0\times$ worse in MSE at $10.8\times$ the cost; ABC-L1 is $13.8\times$ worse at $13.8\times$ the cost.}
\label{fig:cost}
\end{figure}
"""

# ============================================================
# INSERTION PLAN
# ============================================================
# (anchor_text, figure_block, insert_after=True)
insertions = [
    # Fig 1: after classification algorithm paragraph in Section 4
    (
        r"We apply this classifier to the three residuals considered in this work in Section~\ref{sec:diagnostic_results}.",
        FIG01, True
    ),
    # Fig 2: after ABC reference subsection in Section 5
    (
        r"We use \(N_x=100\), \(N_t=200\) for the ABC reference, with weights precomputed once and cached.",
        FIG02, True
    ),
    # Fig 3: after Setup itemize in Section 6.1
    (
        r"For the two non-local residuals (Caputo-L1 and ABC-L1) we use \(N_t=50\) time steps for the residual and \(60\) spatial collocation points per step. For the naive FD residual, we use 1000 random collocation points and \(\Delta t = 10^{-2}\) as in the standard implementation.",
        FIG03, True
    ),
    # Fig 4 & 5: after Table tab:main explanation in Section 6.2
    (
        r"Training time increases by a factor of \(10.8\times\) (Caputo) to \(13.8\times\) (ABC) relative to the local baseline.",
        FIG04 + "\n" + FIG05, True
    ),
    # Fig 6: after cost table in Section 6.5
    (
        r"The ABC-L1 residual costs approximately \(13.8\times\) more than the naive FD residual for the same number of epochs and the same architecture.",
        FIG06, True
    ),
]

# ============================================================
# PATCH
# ============================================================
def main():
    if not os.path.exists(SRC):
        print(f"❌ {SRC} not found in {os.getcwd()}")
        return

    with open(SRC, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup
    shutil.copy(SRC, DST)
    print(f"Working on copy: {DST}")

    n_ok, n_fail = 0, 0
    for anchor, block, after in insertions:
        if anchor in content:
            if after:
                content = content.replace(anchor, anchor + "\n" + block, 1)
            else:
                content = content.replace(anchor, block + "\n" + anchor, 1)
            n_ok += 1
            print(f"  ✅ inserted ({anchor[:50]}...)")
        else:
            n_fail += 1
            print(f"  ❌ anchor not found: {anchor[:60]}...")

    with open(DST, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Done: {n_ok} figures inserted, {n_fail} failures.")
    print(f"Output: {DST}")
    print("\nNext: pdflatex ARIA_ICNABS_v3_with_figures.tex (twice)")

if __name__ == "__main__":
    main()