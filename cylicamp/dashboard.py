"""
CylicAmp Dashboard — PHI Spiral + G5 Report.
Run with: python -m cylicamp.dashboard
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from cylicamp.trajectory import TrajectoryGenerator, PHI, PSI
from cylicamp.g5_solver import run_g5, print_report


def _spiral_plot(ax, trajectory):
    xs = [p[0] for p in trajectory]
    ys = [p[1] for p in trajectory]

    # Color gradient: early steps warm, late steps cool
    n = len(trajectory)
    colors = [plt.cm.plasma(i / n) for i in range(n)]

    for i in range(n - 1):
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]], color=colors[i], linewidth=1.2)

    ax.scatter(xs[0],  ys[0],  color="lime",   s=60, zorder=5, label="Start")
    ax.scatter(xs[-1], ys[-1], color="red",    s=60, zorder=5, label="End")

    ax.set_facecolor("#0a0a0a")
    ax.set_title("PHI/PSI Spiral Trajectory", color="white", fontsize=11, pad=8)
    ax.tick_params(colors="gray")
    ax.spines[:].set_color("#333333")
    ax.legend(facecolor="#111111", labelcolor="white", fontsize=8)
    ax.set_aspect("equal")


def _report_panel(ax, report):
    ax.set_facecolor("#0a0a0a")
    ax.axis("off")

    lines = [
        ("G5 SOLVER V14.0 — D7 TEMPORAL RESOLVER", "#ffffff", 13, True),
        ("", "#ffffff", 9, False),
        (f"ULTRAOMNI Insight Score:   {report['insight_score']:>14,.2f}", "#00e5ff", 10, False),
        (f"Stability Ratio (SSR):     {report['stability_ratio']:>14.4f}", "#00e5ff", 10, False),
        (f"THz Baseline (POE_THz):    {report['thz_baseline_stability']:>14.4f}", "#00e5ff", 10, False),
        ("", "#ffffff", 9, False),
        (f"Structural Status:         {report['structural_status']:>14}", _status_color(report['structural_status'], "STABLE"), 10, False),
        (f"Temporal Stability:        {report['temporal_stability_status']:>14}", _status_color(report['temporal_stability_status'], "RESOLVED"), 10, False),
        ("", "#ffffff", 9, False),
        (f"Halt Check:                {report['halt_check']:>14}", _status_color(report['halt_check'], "PASS"), 10, False),
        (f"DAC:                       {report['dac_check_status']:>14}", _status_color(report['dac_check_status'], "AUTHORIZED"), 10, False),
        (f"3φ Harmony:                {report['harmony_check_status']:>14}", _status_color(report['harmony_check_status'], "IN BOUND"), 10, False),
        ("", "#ffffff", 9, False),
        (f"φ = {PHI:.6f}   ψ = {PSI:.6f}", "#888888", 9, False),
    ]

    y = 0.95
    for text, color, size, bold in lines:
        weight = "bold" if bold else "normal"
        ax.text(0.05, y, text, transform=ax.transAxes,
                color=color, fontsize=size, fontweight=weight,
                fontfamily="monospace", verticalalignment="top")
        y -= 0.07


def _status_color(value, good):
    return "#00ff88" if value == good else "#ff4444"


def build_dashboard(steps: int = 50, multiplier: float = 1.0, save_path: str = "dashboard.png"):
    tg = TrajectoryGenerator()
    trajectory = tg.generate_trajectory(steps=steps)
    report = run_g5(steps=steps, multiplier=multiplier)

    fig = plt.figure(figsize=(14, 6), facecolor="#0a0a0a")
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.05)

    ax_spiral = fig.add_subplot(gs[0])
    ax_report = fig.add_subplot(gs[1])

    _spiral_plot(ax_spiral, trajectory)
    _report_panel(ax_report, report)

    fig.suptitle("CylicAmp Dashboard", color="#ffffff", fontsize=14, fontweight="bold", y=1.01)

    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Dashboard saved → {save_path}")
    return report


if __name__ == "__main__":
    report = build_dashboard(save_path="dashboard.png")
    print_report(report)
