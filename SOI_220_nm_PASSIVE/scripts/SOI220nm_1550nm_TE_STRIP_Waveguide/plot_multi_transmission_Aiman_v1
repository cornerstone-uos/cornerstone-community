# Created by: Aiman Hazim Shafizam (CORNERSTONE)
# Date created: 2026-08-26
# Version: 1.2
# Changes:
#   v1.0 (2026-08-26) - Initial multi-transmission overlay.
#   v1.1 (2026-08-26) - Added separate chip panels, WG legends, and Loss (dB).
#   v1.2 (2026-08-26) - Inverted the Loss axis to match cs-testsuite and set
#                       the major Y-axis interval to 5 dB.

"""Plot one loss-spectrum panel per chip in a PDKMonitor slot folder.

Run with "Run script over folder". Each chip gets a separate panel and its
WG1, WG2, ... routes are identified in the legend.
"""

import json
import math
import re

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


LAUNCH_POWER_DBM = 10.0
MAX_POINTS_PER_TRACE = 3000


def _native(value):
    if hasattr(value, "to_py"):
        try:
            return value.to_py()
        except Exception:
            pass
    return value


def _folder_tests():
    encoded = globals().get("tests_json")
    if isinstance(encoded, str) and encoded:
        return json.loads(encoded)
    supplied = _native(globals().get("tests"))
    return list(supplied) if supplied is not None else []


def _identity(item):
    value = str(item.get("filename") or item.get("name") or "")
    match = re.search(r"Chip\s*(\d+).*?WG\s*(\d+)", value, re.IGNORECASE)
    return (int(match.group(1)), int(match.group(2))) if match else None


def _loss_pairs(item):
    parsed = _native(item.get("parsed"))
    if not isinstance(parsed, dict):
        return []
    sweep = _native(parsed.get("sweep")) or {}
    wavelengths = _native(sweep.get("values")) or []
    traces = _native(parsed.get("traces")) or []
    if not traces:
        return []
    powers = _native((_native(traces[0]) or {}).get("values")) or []
    pairs = []
    for wavelength, power in zip(wavelengths, powers):
        try:
            wavelength_value = float(wavelength)
            power_value = float(power)
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(wavelength_value) and math.isfinite(power_value)):
            continue
        if power_value <= 0:
            continue
        optical_power_dbm = 10.0 * math.log10(power_value * 1000.0)
        loss_db = abs(LAUNCH_POWER_DBM - optical_power_dbm)
        pairs.append((wavelength_value, loss_db))
    return pairs


def _downsample(pairs):
    if len(pairs) <= MAX_POINTS_PER_TRACE:
        return pairs
    stride = max(1, math.ceil(len(pairs) / MAX_POINTS_PER_TRACE))
    return pairs[::stride]


items = [_native(item) or {} for item in _folder_tests()]
folder_label = str(globals().get("folder_name") or "folder")
by_chip = {}
skipped = []

for item in items:
    identity = _identity(item)
    pairs = _loss_pairs(item)
    if identity is None or len(pairs) < 2:
        skipped.append(str(item.get("filename") or item.get("name") or "?"))
        continue
    chip_number, waveguide_number = identity
    by_chip.setdefault(chip_number, []).append((waveguide_number, _downsample(pairs)))

if not by_chip:
    print(f"No parseable Chip#_WG# transmission files in '{folder_label}'.")
else:
    column_count = min(4, len(by_chip))
    row_count = math.ceil(len(by_chip) / column_count)
    fig, axes = plt.subplots(
        row_count,
        column_count,
        figsize=(4.2 * column_count, 3.2 * row_count),
        squeeze=False,
    )
    trace_count = 0
    coverage = []
    for axis, chip_number in zip(axes.flat, sorted(by_chip)):
        for waveguide_number, pairs in sorted(by_chip[chip_number]):
            xs = [point[0] for point in pairs]
            ys = [point[1] for point in pairs]
            coverage.extend(xs)
            axis.plot(xs, ys, lw=0.8, alpha=0.85, label=f"WG{waveguide_number}")
            trace_count += 1
        axis.set_title(f"Chip{chip_number}", fontsize=10)
        axis.set_xlabel("Wavelength (nm)")
        axis.set_ylabel("Loss (dB)")
        axis.yaxis.set_major_locator(MultipleLocator(5.0))
        axis.invert_yaxis()
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=7, loc="best")

    for unused_axis in list(axes.flat)[len(by_chip):]:
        unused_axis.axis("off")

    fig.suptitle(f"Transmission spectra by chip — {folder_label}", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    print(f"Folder: {folder_label}")
    print(f"  chips plotted: {len(by_chip)}")
    print(f"  WG traces plotted: {trace_count}")
    if coverage:
        print(f"  wavelength coverage: {min(coverage):.3f}-{max(coverage):.3f} nm")
    print(f"  launch power reference: {LAUNCH_POWER_DBM:.3f} dBm")
    print(f"  non-plot files skipped: {len(skipped)}")
    if skipped:
        print(f"  skipped examples: {', '.join(skipped[:5])}")
    print(f"  display downsampling limit: {MAX_POINTS_PER_TRACE} points per WG")

    emit(fig)
