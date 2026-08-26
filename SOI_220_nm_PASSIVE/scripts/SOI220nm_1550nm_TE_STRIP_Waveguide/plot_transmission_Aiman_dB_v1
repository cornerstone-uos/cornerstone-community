# Created by: Aiman Hazim Shafizam (CORNERSTONE)
# Date created: 2026-08-26
# Version: 1.0
# Changes:
#   v1.0 (2026-08-26) - Initial peak-normalised dB transmission plot.

"""Plot one PDKMonitor transmission trace in dB, normalised to its peak.

Run this saved script from an individual TXT test card. Non-positive power
samples are ignored because they cannot be converted to logarithmic units.
"""

import math

import matplotlib.pyplot as plt


def _native(value):
    if hasattr(value, "to_py"):
        try:
            return value.to_py()
        except Exception:
            pass
    return value


def _positive_pairs(xs, ys):
    pairs = []
    for x, y in zip(xs or [], ys or []):
        try:
            x_value = float(x)
            y_value = float(y)
        except (TypeError, ValueError):
            continue
        if math.isfinite(x_value) and math.isfinite(y_value) and y_value > 0:
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
            pairs = _positive_pairs(wavelengths, _native(trace.get("values")) or [])
            if not pairs:
                continue
            xs = [point[0] for point in pairs]
            powers = [point[1] for point in pairs]
            peak_power = max(powers)
            values_db = [10.0 * math.log10(value / peak_power) for value in powers]
            label = trace.get("name") or active_test.get("name") or "transmission"
            ax.plot(xs, values_db, lw=1.0, label=label)
            peak_index = powers.index(peak_power)
            plotted.append((label, xs, values_db, peak_power, peak_index))

        if not plotted:
            plt.close(fig)
            print(f"No positive wavelength/power values on '{active_test.get('name', '?')}'.")
        else:
            metadata = _native(active_test.get("metadata")) or {}
            title = metadata.get("device_id") or active_test.get("name") or "Transmission"
            ax.set_xlabel(str(x_name).replace("_", " "))
            ax.set_ylabel("Transmission (dB, normalised to peak)")
            ax.set_title(f"Transmission (dB) — {title}")
            ax.grid(True, alpha=0.3)
            if len(plotted) > 1:
                ax.legend(fontsize=8, loc="best")
            fig.tight_layout()

            print(f"Test: {active_test.get('name', '?')}")
            for label, xs, values_db, peak_power, peak_index in plotted:
                in_3db_band = [
                    x for x, value_db in zip(xs, values_db) if value_db >= -3.0
                ]
                bandwidth_3db = (
                    max(in_3db_band) - min(in_3db_band) if in_3db_band else float("nan")
                )
                print(
                    f"  {label}: {len(values_db)} positive points | "
                    f"wavelength={min(xs):.3f}-{max(xs):.3f} nm | "
                    f"peak={peak_power:.6e} W @ {xs[peak_index]:.3f} nm | "
                    f"range={min(values_db):.3f} to {max(values_db):.3f} dB"
                )
                print(f"  3 dB bandwidth: {bandwidth_3db:.3f} nm")

            emit(fig)
