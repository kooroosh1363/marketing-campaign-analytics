from __future__ import annotations

import numpy as np
import pandas as pd


def clean_campaign_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the UCI campaign table without silently deleting valid contacts."""
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    out["converted"] = out["response"].astype(str).str.lower().eq("yes")
    out["contacted_before"] = out["previous"].fillna(0).gt(0)
    out["has_previous_success"] = out["poutcome"].astype(str).str.lower().eq("success")
    out["campaign_contacts"] = pd.to_numeric(out["campaign"], errors="coerce")
    out["contact_duration_seconds"] = pd.to_numeric(out["duration"], errors="coerce")
    return out


def overall_kpis(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{
        "contacts": len(df),
        "conversions": int(df["converted"].sum()),
        "conversion_rate_pct": round(100 * df["converted"].mean(), 2),
        "median_contacts_this_campaign": float(df["campaign_contacts"].median()),
        "previously_contacted_pct": round(100 * df["contacted_before"].mean(), 2),
    }])


def conversion_breakdown(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    g = df.groupby(dimension, dropna=False).agg(
        contacts=("converted", "size"),
        conversions=("converted", "sum"),
    ).reset_index()
    g["conversion_rate_pct"] = (100 * g["conversions"] / g["contacts"]).round(2)
    return g.sort_values(["conversion_rate_pct", "contacts"], ascending=[False, False])


def contact_frequency_effect(df: pd.DataFrame) -> pd.DataFrame:
    """Describe conversion by number of contacts in the current campaign."""
    bins = [0, 1, 2, 3, 5, 10, np.inf]
    labels = ["1", "2", "3", "4-5", "6-10", "11+"]
    x = df.copy()
    x["contact_frequency_band"] = pd.cut(
        x["campaign_contacts"], bins=bins, labels=labels, right=True, include_lowest=True
    )
    return conversion_breakdown(x, "contact_frequency_band")


def previous_campaign_effect(df: pd.DataFrame) -> pd.DataFrame:
    return conversion_breakdown(df, "poutcome")


def customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create interpretable descriptive segments, not a predictive model."""
    x = df.copy()
    x["age_band"] = pd.cut(
        x["age"], bins=[0, 29, 39, 49, 59, np.inf], labels=["<30", "30-39", "40-49", "50-59", "60+"]
    )
    g = x.groupby(["age_band", "job"], observed=True).agg(
        contacts=("converted", "size"),
        conversions=("converted", "sum"),
    ).reset_index()
    g["conversion_rate_pct"] = (100 * g["conversions"] / g["contacts"]).round(2)
    return g.sort_values(["conversions", "conversion_rate_pct"], ascending=False)


def duration_diagnostic(df: pd.DataFrame) -> pd.DataFrame:
    """Diagnostic only: duration is post-contact and must not be used for pre-call targeting."""
    x = df.copy()
    x["duration_band"] = pd.cut(
        x["contact_duration_seconds"],
        bins=[-1, 60, 180, 300, 600, np.inf],
        labels=["<=1m", "1-3m", "3-5m", "5-10m", "10m+"],
    )
    return conversion_breakdown(x, "duration_band")
