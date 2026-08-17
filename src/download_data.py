from pathlib import Path

from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    dataset = fetch_ucirepo(id=222)
    x = dataset.data.features.copy()
    y = dataset.data.targets.copy()
    target_name = y.columns[0]
    frame = x.copy()
    frame["response"] = y[target_name]
    out = RAW / "bank_marketing.csv"
    frame.to_csv(out, index=False)
    print(f"Saved {len(frame):,} rows to {out}")


if __name__ == "__main__":
    main()
