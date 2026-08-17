from pathlib import Path

import pandas as pd

from .analytics import (
    clean_campaign_data,
    contact_frequency_effect,
    conversion_breakdown,
    customer_segments,
    duration_diagnostic,
    overall_kpis,
    previous_campaign_effect,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bank_marketing.csv"
OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = clean_campaign_data(pd.read_csv(RAW))

    outputs = {
        "executive_summary.csv": overall_kpis(df),
        "job_performance.csv": conversion_breakdown(df, "job"),
        "month_performance.csv": conversion_breakdown(df, "month"),
        "contact_method_performance.csv": conversion_breakdown(df, "contact"),
        "previous_outcome_performance.csv": previous_campaign_effect(df),
        "contact_frequency_effect.csv": contact_frequency_effect(df),
        "customer_segments.csv": customer_segments(df),
        "duration_diagnostic.csv": duration_diagnostic(df),
    }
    for filename, frame in outputs.items():
        frame.to_csv(OUT / filename, index=False)

    print(outputs["executive_summary.csv"].to_string(index=False))


if __name__ == "__main__":
    main()
