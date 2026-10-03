"""ECON 611 Project: Does Okun's Law still hold in the U.S. (2005 Q1 - 2024 Q4)?

Requires a free FRED API key in the FRED_API_KEY environment variable.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf
from fredapi import Fred

# Fetch from 2004 so the 2005 Q1 changes can be calculated.
FETCH_START = "2004-01-01"
FETCH_END = "2024-12-31"

# Analysis window: 2005 Q1 through 2024 Q4 (quarter-start dates).
ANALYSIS_START = "2005-01-01"
ANALYSIS_END = "2024-10-01"

COVID_QUARTERS = pd.to_datetime(["2020-04-01", "2020-07-01"])  # 2020 Q2, Q3


# ---- Data source ----
fred = Fred(api_key=os.environ["FRED_API_KEY"])
unrate = fred.get_series("UNRATE", observation_start=FETCH_START, observation_end=FETCH_END)
gdp = fred.get_series("GDPC1", observation_start=FETCH_START, observation_end=FETCH_END)

# ---- Cleaning ----
# Monthly unemployment -> quarterly by averaging the three months in each quarter.
unrate_q = unrate.resample("QS").mean()

# Merge by quarter.
df = pd.concat({"unrate": unrate_q, "gdp": gdp}, axis=1)

# Quarter-over-quarter GDP growth (percent, not annualized)
# and change in the unemployment rate (percentage points).
df["gdp_growth"] = df["gdp"].pct_change() * 100
df["d_unrate"] = df["unrate"].diff()

# Keep the analysis window and drop missing values.
df = df.loc[ANALYSIS_START:ANALYSIS_END].dropna()
print(f"Observations: {len(df)} ({df.index[0].date()} to {df.index[-1].date()})")

# ---- Regression ----
model = smf.ols("d_unrate ~ gdp_growth", data=df).fit()
print("\n=== Full sample ===")
print(model.summary())

# Robustness check: drop the COVID quarters (2020 Q2 and Q3).
no_covid = df.drop(COVID_QUARTERS)
model_nc = smf.ols("d_unrate ~ gdp_growth", data=no_covid).fit()
print("\n=== Without 2020 Q2 and Q3 ===")
print(model_nc.summary())

print("\n=== Comparison ===")
for name, m in [("Full sample", model), ("Without COVID", model_nc)]:
    print(
        f"{name:14s} slope = {m.params['gdp_growth']:.3f}, "
        f"p-value = {m.pvalues['gdp_growth']:.4f}, "
        f"R-squared = {m.rsquared:.3f}, N = {int(m.nobs)}"
    )

# ---- Scatter plot ----
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df["gdp_growth"], df["d_unrate"], alpha=0.7, label="Quarters")
x = df["gdp_growth"].sort_values()
ax.plot(x, model.params["Intercept"] + model.params["gdp_growth"] * x,
        color="red", label=f"OLS fit (slope = {model.params['gdp_growth']:.3f})")
ax.axhline(0, color="gray", linewidth=0.8)
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel("Real GDP growth (% change from previous quarter)")
ax.set_ylabel("Change in unemployment rate (percentage points)")
ax.set_title("Okun's Law in the U.S., 2005 Q1 - 2024 Q4")
ax.legend()
fig.tight_layout()
fig.savefig("okun_scatter.png", dpi=150)
print("\nSaved scatter plot to okun_scatter.png")
