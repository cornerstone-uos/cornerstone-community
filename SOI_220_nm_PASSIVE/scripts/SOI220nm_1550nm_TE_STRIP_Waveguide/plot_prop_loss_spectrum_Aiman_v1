# Created by: Aiman Hazim Shafizam (CORNERSTONE)
# Date created: 2026-08-26
# Version: 1.0
# Changes:
#   v1.0 (2026-08-26) - Initial per-chip propagation-loss and MSE spectrum.

"""Plot propagation loss and fit MSE versus wavelength for every chip.

Run with "Run script over folder" on a slot folder containing the matching
Chip#_WG#.txt files and route-config.json.
"""

import json
import math
import re

import matplotlib.pyplot as plt


TARGET_WAVELENGTH_NM = 1550.0
WINDOW_NM = 5.0
SPECTRAL_STEP_NM = 10.0
MSE_THRESHOLD = 0.5
LAUNCH_POWER_DBM = 10.0
DEFAULT_ROUTE_LENGTHS_MM = {1: 0.0, 2: 5.0, 3: 10.0, 4: 15.0}


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


def _route_lengths(items):
    for item in items:
        name = str(item.get("filename") or item.get("name") or "").lower()
        if "route-config" not in name or not item.get("rawText"):
            continue
        try:
            config = json.loads(item["rawText"])
            found = {}
            for index, route in enumerate(config.get("routes") or [], start=1):
                match = re.search(r"(\d+)", str(route.get("route") or index))
                length = float(route.get("lengthMm"))
                if match and math.isfinite(length):
                    found[int(match.group(1))] = length
            if found:
                return found, "route-config.json"
        except Exception:
            pass
    return dict(DEFAULT_ROUTE_LENGTHS_MM), "built-in fallback"


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
        pairs.append((wavelength_value, abs(LAUNCH_POWER_DBM - optical_power_dbm)))
    return pairs


def _mean_in_window(pairs, center):
    values = [loss for wavelength, loss in pairs if abs(wavelength - center) <= WINDOW_NM]
    return sum(values) / len(values) if values else None


def _linear_fit(points):
    if len(points) < 2:
        return None
    count = len(points)
    sum_x = sum(x for x, _ in points)
    sum_y = sum(y for _, y in points)
    sum_xy = sum(x * y for x, y in points)
    sum_xx = sum(x * x for x, _ in points)
    denominator = count * sum_xx - sum_x * sum_x
    if denominator == 0:
        return None
    slope = (count * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / count
    residual_sum = sum((y - (slope * x + intercept)) ** 2 for x, y in points)
    return slope * 10.0, residual_sum / count


def _centers(minimum, maximum):
    start = math.ceil(minimum / SPECTRAL_STEP_NM) * SPECTRAL_STEP_NM
    values = []
    center = start
    while center <= maximum + 1e-9:
        values.append(center)
        center += SPECTRAL_STEP_NM
    return values


items = [_native(item) or {} for item in _folder_tests()]
folder_label = str(globals().get("folder_name") or "folder")
route_lengths, route_source = _route_lengths(items)
by_chip = {}

for item in items:
    identity = _identity(item)
    if identity is None:
        continue
    chip_number, waveguide_number = identity
    if waveguide_number not in route_lengths:
        continue
    pairs = _loss_pairs(item)
    if pairs:
        by_chip.setdefault(chip_number, {})[waveguide_number] = pairs

results = []
for chip_number in sorted(by_chip):
    routes = by_chip[chip_number]
    common_minimum = max(min(point[0] for point in pairs) for pairs in routes.values())
    common_maximum = min(max(point[0] for point in pairs) for pairs in routes.values())
    spectrum = []
    for center in _centers(common_minimum, common_maximum):
        regression_points = []
        for waveguide_number, pairs in sorted(routes.items()):
            mean_loss = _mean_in_window(pairs, center)
            if mean_loss is not None:
                regression_points.append((route_lengths[waveguide_number], mean_loss))
        fit = _linear_fit(regression_points)
        if fit is not None:
            spectrum.append((center, fit[0], fit[1], len(regression_points)))
    if spectrum:
        results.append((chip_number, spectrum))

if not results:
    print(
        f"No propagation-loss spectra were produced for '{folder_label}'. "
        "Check the Chip#_WG# files and route-config.json."
    )
else:
    column_count = min(3, len(results))
    row_count = math.ceil(len(results) / column_count)
    fig, axes = plt.subplots(
        row_count,
        column_count,
        figsize=(5.1 * column_count, 3.5 * row_count),
        squeeze=False,
    )

    for axis, (chip_number, spectrum) in zip(axes.flat, results):
        xs = [point[0] for point in spectrum]
        losses = [point[1] for point in spectrum]
        mses = [point[2] for point in spectrum]
        mse_axis = axis.twinx()
        loss_line = axis.plot(
            xs, losses, color="#2f81f7", marker="o", ms=3.5, lw=1.25,
            label="Propagation loss",
        )[0]
        mse_line = mse_axis.plot(
            xs, mses, color="#f0883e", marker="s", ms=3.0, lw=1.0,
            ls="--", label="MSE",
        )[0]
        axis.axvspan(
            TARGET_WAVELENGTH_NM - WINDOW_NM,
            TARGET_WAVELENGTH_NM + WINDOW_NM,
            color="#2f81f7",
            alpha=0.08,
        )
        nearest = min(spectrum, key=lambda point: abs(point[0] - TARGET_WAVELENGTH_NM))
        status = "PASS" if nearest[2] <= MSE_THRESHOLD else "FAIL"
        axis.set_title(
            f"Chip{chip_number}: {nearest[1]:.3f} dB/cm at {nearest[0]:.0f} nm\n"
            f"MSE={nearest[2]:.4f} — {status}",
            fontsize=9,
        )
        axis.set_xlabel("Wavelength (nm)")
        axis.set_ylabel("Propagation loss (dB/cm)", color="#2f81f7")
        mse_axis.set_ylabel("MSE", color="#f0883e")
        axis.tick_params(axis="y", colors="#2f81f7")
        mse_axis.tick_params(axis="y", colors="#f0883e")
        axis.grid(True, alpha=0.25)
        axis.legend([loss_line, mse_line], ["Propagation loss", "MSE"], fontsize=7)

    for unused_axis in list(axes.flat)[len(results):]:
        unused_axis.axis("off")

    fig.suptitle(
        f"Propagation-loss spectrum — {folder_label} | "
        f"window +/- {WINDOW_NM:.0f} nm, step {SPECTRAL_STEP_NM:.0f} nm",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    print(f"Folder: {folder_label}")
    print(f"  route lengths: {route_source} -> {route_lengths}")
    print(
        f"  wavelength window: +/- {WINDOW_NM:.1f} nm | "
        f"spectral step: {SPECTRAL_STEP_NM:.1f} nm | "
        f"MSE threshold: {MSE_THRESHOLD:.4f}"
    )
    for chip_number, spectrum in results:
        nearest = min(spectrum, key=lambda point: abs(point[0] - TARGET_WAVELENGTH_NM))
        status = "PASS" if nearest[2] <= MSE_THRESHOLD else "FAIL"
        print(
            f"  Chip{chip_number}: {len(spectrum)} intervals | "
            f"nearest target={nearest[0]:.1f} nm | "
            f"loss={nearest[1]:.6f} dB/cm | MSE={nearest[2]:.6f} | {status}"
        )

    emit(fig)
