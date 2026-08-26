# Working starter — plots column 0 (x) vs column 1 (y) of the
# first parseable test on this BB. Edit freely.
#
# Globals exposed by the dashboard:
#   tests    : list of every test on this BB (parsed dict + metadata)
#   data     : dict of S-matrix datasets keyed by name
#
# To emit a matplotlib figure, use the helper at the top.

import io, base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def emit(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    print("DASH_PLOT_PNG:" + base64.b64encode(buf.getvalue()).decode())
    plt.close(fig)

# Pick the first test that has parsed numeric data
candidate = None
for t in tests:
    if t.get("parsed") and t["parsed"].get("sweep") and t["parsed"].get("traces"):
        candidate = t
        break

if candidate is None:
    print("No tests with parsed numeric data on this BB yet.")
    print("Drop a CSV / TXT into the Test results tab and re-run.")
else:
    sweep  = candidate["parsed"]["sweep"]
    traces = candidate["parsed"]["traces"]
    fname  = candidate.get("name") or candidate.get("filename") or "data"
    fig, ax = plt.subplots(figsize=(9, 4.6))
    for tr in traces:
        # Prefix every legend entry with the source filename so the legend
        # in the plot window tells you exactly which file each trace came
        # from (matches the "Plot raw" behaviour on the dashboard side).
        tr_name = tr.get("name") or "y"
        legend  = f"{fname}:{tr_name}" if len(traces) > 1 else fname
        ax.plot(sweep["values"], tr["values"], lw=1.0, label=legend)
    ax.set_xlabel(sweep.get("name") or "x")
    ax.set_ylabel("value")
    ax.set_title(fname)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="best")
    fig.tight_layout()
    emit(fig)
    print(f"Plotted {len(traces)} trace(s) from '{fname}'.")
