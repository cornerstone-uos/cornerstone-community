# Created by: Aiman Hazim Shafizam (CORNERSTONE)
# Date created: 2026-08-26
# Version: 1.1
# Changes:
#   v1.0 (2026-08-26) - Initial per-chip propagation-loss fitting plot.
#   v1.1 (2026-08-26) - Added 95% confidence bounds and slope confidence
#                       intervals, renamed the Y-axis to Loss (dB), removed
#                       WG labels, and aligned loss conversion with cs-testsuite.

"""Fit propagation loss for every chip in one PDKMonitor slot folder.

Run with "Run script over folder". The script reads ``route-config.json``
from that folder, groups ``Chip#_WG#.txt`` files by chip, averages optical
loss in the 1550 +/- 5 nm window, and fits loss versus route length.
"""

import json
import math
import re

import matplotlib.pyplot as plt


TARGET_WAVELENGTH_NM = 1550.0
WINDOW_NM = 5.0
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
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _route_lengths(items):
    for item in items:
        name = str(item.get("filename") or item.get("name") or "").lower()
        if "route-config" not in name:
            continue
        raw_text = item.get("rawText")
        if not raw_text:
            continue
        try:
            config = json.loads(raw_text)
            routes = config.get("routes") or []
            found = {}
            for index, route in enumerate(routes, start=1):
                route_name = str(route.get("route") or index)
                route_match = re.search(r"(\d+)", route_name)
                length = float(route.get("lengthMm"))
                if route_match and math.isfinite(length):
                    found[int(route_match.group(1))] = length
            if found:
                return found, "route-config.json"
        except Exception:
            pass
    return dict(DEFAULT_ROUTE_LENGTHS_MM), "built-in fallback"


def _window_loss_db(item):
    parsed = _native(item.get("parsed"))
    if not isinstance(parsed, dict):
        return None, 0
    sweep = _native(parsed.get("sweep")) or {}
    wavelengths = _native(sweep.get("values")) or []
    traces = _native(parsed.get("traces")) or []
    if not traces:
        return None, 0
    trace = _native(traces[0]) or {}
    powers = _native(trace.get("values")) or []
    losses = []
    for wavelength, power in zip(wavelengths, powers):
        try:
            wavelength_value = float(wavelength)
            power_value = float(power)
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(wavelength_value) and math.isfinite(power_value)):
            continue
        if power_value <= 0 or abs(wavelength_value - TARGET_WAVELENGTH_NM) > WINDOW_NM:
            continue
        optical_power_dbm = 10.0 * math.log10(power_value * 1000.0)
        losses.append(abs(LAUNCH_POWER_DBM - optical_power_dbm))
    if not losses:
        return None, 0
    return sum(losses) / len(losses), len(losses)


def _linear_fit(points):
    if len(points) < 2:
        return None
    count = len(points)
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)
    sum_xy = sum(point[0] * point[1] for point in points)
    sum_xx = sum(point[0] * point[0] for point in points)
    denominator = count * sum_xx - sum_x * sum_x
    if denominator == 0:
        return None
    slope = (count * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / count
    residual_sum = sum((y - (slope * x + intercept)) ** 2 for x, y, _ in points)
    mse = residual_sum / count
    mean_y = sum_y / count
    total_sum = sum((y - mean_y) ** 2 for _, y, _ in points)
    r_squared = 1.0 - residual_sum / total_sum if total_sum > 0 else 1.0
    x_mean = sum_x / count
    sxx = sum((x - x_mean) ** 2 for x, _, _ in points)
    degrees_freedom = count - 2
    residual_standard_error = (
        math.sqrt(residual_sum / degrees_freedom) if degrees_freedom > 0 else 0.0
    )
    t_critical = _t_critical_95(degrees_freedom)
    slope_standard_error = (
        residual_standard_error / math.sqrt(sxx) if sxx > 0 else 0.0
    )
    slope_margin = t_critical * slope_standard_error
    return {
        "slope_db_per_mm": slope,
        "loss_db_per_cm": slope * 10.0,
        "intercept_db": intercept,
        "mse": mse,
        "r_squared": r_squared,
        "count": count,
        "x_mean": x_mean,
        "sxx": sxx,
        "residual_standard_error": residual_standard_error,
        "t_critical": t_critical,
        "slope_ci_db_per_cm": (
            (slope - slope_margin) * 10.0,
            (slope + slope_margin) * 10.0,
        ),
    }


def _t_critical_95(degrees_freedom):
    """Two-sided 95% Student-t critical value without SciPy."""
    values = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
        6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
        25: 2.060, 30: 2.042, 40: 2.021, 60: 2.000, 120: 1.980,
    }
    if degrees_freedom <= 0:
        return 0.0
    for available in sorted(values):
        if degrees_freedom <= available:
            return values[available]
    return 1.960


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
    mean_loss_db, sample_count = _window_loss_db(item)
    if mean_loss_db is None:
        continue
    by_chip.setdefault(chip_number, []).append(
        (route_lengths[waveguide_number], mean_loss_db, waveguide_number, sample_count)
    )

results = []
for chip_number in sorted(by_chip):
    samples = sorted(by_chip[chip_number], key=lambda sample: sample[0])
    fit_points = [(length, loss, waveguide) for length, loss, waveguide, _ in samples]
    fit = _linear_fit(fit_points)
    if fit is not None:
        results.append((chip_number, samples, fit))

if not results:
    print(
        f"No propagation fits were produced for '{folder_label}'. "
        "Check that the folder contains matching Chip#_WG#.txt files and route-config.json."
    )
else:
    column_count = min(4, len(results))
    row_count = math.ceil(len(results) / column_count)
    fig, axes = plt.subplots(
        row_count,
        column_count,
        figsize=(4.1 * column_count, 3.25 * row_count),
        squeeze=False,
    )

    passing_losses = []
    for axis, (chip_number, samples, fit) in zip(axes.flat, results):
        xs = [sample[0] for sample in samples]
        ys = [sample[1] for sample in samples]
        fit_xs = [
            min(xs) + index * (max(xs) - min(xs)) / 99.0 for index in range(100)
        ]
        fit_ys = [
            fit["slope_db_per_mm"] * x + fit["intercept_db"] for x in fit_xs
        ]
        confidence_margin = [
            fit["t_critical"]
            * fit["residual_standard_error"]
            * math.sqrt(
                1.0 / fit["count"]
                + ((x - fit["x_mean"]) ** 2 / fit["sxx"] if fit["sxx"] > 0 else 0.0)
            )
            for x in fit_xs
        ]
        confidence_lower = [y - margin for y, margin in zip(fit_ys, confidence_margin)]
        confidence_upper = [y + margin for y, margin in zip(fit_ys, confidence_margin)]
        passed = fit["mse"] <= MSE_THRESHOLD
        if passed:
            passing_losses.append(fit["loss_db_per_cm"])

        axis.scatter(xs, ys, s=34, color="#2f81f7", zorder=3, label="Measured")
        axis.plot(fit_xs, fit_ys, color="#f0883e", lw=1.4, label="Linear fit")
        axis.fill_between(
            fit_xs,
            confidence_lower,
            confidence_upper,
            color="#f0883e",
            alpha=0.18,
            label="95% confidence",
        )
        axis.plot(fit_xs, confidence_lower, color="#f0883e", lw=0.7, ls="--")
        axis.plot(fit_xs, confidence_upper, color="#f0883e", lw=0.7, ls="--")
        axis.set_title(
            f"Chip{chip_number}: {fit['loss_db_per_cm']:.3f} dB/cm\n"
            f"MSE={fit['mse']:.4f}, R2={fit['r_squared']:.4f} — "
            f"{'PASS' if passed else 'FAIL'}",
            fontsize=9,
        )
        axis.set_xlabel("Relative length (mm)")
        axis.set_ylabel("Loss (dB)")
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=7, loc="best")

    for unused_axis in list(axes.flat)[len(results):]:
        unused_axis.axis("off")

    fig.suptitle(
        f"Propagation-loss fits — {folder_label} | "
        f"{TARGET_WAVELENGTH_NM:.0f} +/- {WINDOW_NM:.0f} nm",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    print(f"Folder: {folder_label}")
    print(f"  route lengths: {route_source} -> {route_lengths}")
    print(
        f"  fit window: {TARGET_WAVELENGTH_NM:.1f} +/- {WINDOW_NM:.1f} nm | "
        f"MSE threshold={MSE_THRESHOLD:.4f}"
    )
    for chip_number, samples, fit in results:
        status = "PASS" if fit["mse"] <= MSE_THRESHOLD else "FAIL"
        print(
            f"  Chip{chip_number}: {fit['loss_db_per_cm']:.6f} dB/cm | "
            f"95% CI=[{fit['slope_ci_db_per_cm'][0]:.6f}, "
            f"{fit['slope_ci_db_per_cm'][1]:.6f}] dB/cm | "
            f"MSE={fit['mse']:.6f} | R2={fit['r_squared']:.6f} | "
            f"intercept={fit['intercept_db']:.6f} dB | {status} | "
            f"routes={len(samples)}"
        )
    yield_percent = 100.0 * len(passing_losses) / len(results)
    average_loss = (
        sum(passing_losses) / len(passing_losses) if passing_losses else float("nan")
    )
    print(
        f"  wafer result: {len(passing_losses)}/{len(results)} passing | "
        f"yield={yield_percent:.2f}% | average={average_loss:.6f} dB/cm"
    )

    emit(fig)
