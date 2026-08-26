# Created by: Aiman Hazim Shafizam (CORNERSTONE)
# Date created: 2026-08-26
# Version: 1.0
# Changes:
#   v1.0 (2026-08-26) - Initial raw optical-power transmission plot.

"""Plot one PDKMonitor transmission trace as optical power in watts.

Run this saved script from an individual TXT test card. PDKMonitor supplies
``test`` and provides ``emit(fig)`` through its Python bootstrap.
"""

import math

import matplotlib.pyplot as plt


TARGET_WAVELENGTH_NM = 1550.0
WINDOW_NM = 5.0


def _native(value):
    if hasattr(value, "to_py"):
        try:
            return value.to_py()
        except Exception:
            pass
    return value


def _finite_pairs(xs, ys):
    pairs = []
    for x, y in zip(xs or [], ys or []):
        try:
            x_value = float(x)
            y_value = float(y)
        except (TypeError, ValueError):
            continue
        if math.isfinite(x_value) and math.isfinite(y_value):
            pairs.append((x_value, y_value))
    return pairs


active_test = _native(globals().get("test"))
if not isinstance(active_test, dict):
    print("Run this script from an individual parsed TXT test file.")
else:
    parsed = _native(active_test.get("parsed"))
    if not isinstance(parsed, dict):
        print(f"No parsed data on '{active_test.get('name', '?')}'.")
    else:
        sweep = _native(parsed.get("sweep")) or {}
        traces = _native(parsed.get("traces")) or []
        wavelengths = _native(sweep.get("values")) or []
        x_name = sweep.get("name") or "wavelength_nm"

        fig, ax = plt.subplots(figsize=(9.2, 4.8))
        plotted = []
        for trace in traces:
            trace = _native(trace) or {}
            pairs = _finite_pairs(wavelengths, _native(trace.get("values")) or [])
            if not pairs:
                continue
            xs = [point[0] for point in pairs]
            ys = [point[1] for point in pairs]
            label = trace.get("name") or active_test.get("name") or "transmission"
            ax.plot(xs, ys, lw=1.0, label=label)
            peak_index = max(range(len(ys)), key=ys.__getitem__)
            plotted.append((label, xs, ys, peak_index))

        if not plotted:
            plt.close(fig)
            print(f"No finite wavelength/power values on '{active_test.get('name', '?')}'.")
        else:
            metadata = _native(active_test.get("metadata")) or {}
            title = metadata.get("device_id") or active_test.get("name") or "Transmission"
            ax.set_xlabel(str(x_name).replace("_", " "))
            ax.set_ylabel("Optical power (W)")
            ax.set_title(f"Transmission (W) — {title}")
            ax.grid(True, alpha=0.3)
            if len(plotted) > 1:
                ax.legend(fontsize=8, loc="best")
            fig.tight_layout()

            print(f"Test: {active_test.get('name', '?')}")
            for label, xs, ys, peak_index in plotted:
                window_values = [
                    y for x, y in zip(xs, ys)
                    if abs(x - TARGET_WAVELENGTH_NM) <= WINDOW_NM
                ]
                window_average = (
                    sum(window_values) / len(window_values) if window_values else float("nan")
                )
                print(
                    f"  {label}: {len(ys)} points | "
                    f"wavelength={min(xs):.3f}-{max(xs):.3f} nm | "
                    f"min={min(ys):.6e} W | max={max(ys):.6e} W | "
                    f"peak wavelength={xs[peak_index]:.3f} nm"
                )
                print(
                    f"  target-window average: {window_average:.6e} W "
                    f"@ {TARGET_WAVELENGTH_NM:.1f} +/- {WINDOW_NM:.1f} nm "
                    f"({len(window_values)} points)"
                )

            # Keep emit as the final stdout-producing operation. PDKMonitor's
            # current stdout collector can corrupt a PNG if text follows it.
            emit(fig)
