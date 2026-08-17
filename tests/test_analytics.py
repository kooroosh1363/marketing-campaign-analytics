import pandas as pd

from src.analytics import clean_campaign_data, conversion_breakdown, overall_kpis


def sample_data():
    return pd.DataFrame({
        "age": [30, 45, 62],
        "job": ["admin.", "technician", "retired"],
        "previous": [0, 2, 1],
        "poutcome": ["unknown", "failure", "success"],
        "campaign": [1, 3, 1],
        "duration": [50, 200, 500],
        "response": ["no", "no", "yes"],
    })


def test_conversion_flag_and_population_are_preserved():
    x = clean_campaign_data(sample_data())
    assert len(x) == 3
    assert int(x["converted"].sum()) == 1


def test_overall_conversion_rate():
    x = clean_campaign_data(sample_data())
    k = overall_kpis(x).iloc[0]
    assert k["contacts"] == 3
    assert k["conversions"] == 1
    assert k["conversion_rate_pct"] == 33.33


def test_breakdown_reconciles_to_overall_population():
    x = clean_campaign_data(sample_data())
    b = conversion_breakdown(x, "job")
    assert int(b["contacts"].sum()) == len(x)
    assert int(b["conversions"].sum()) == int(x["converted"].sum())
