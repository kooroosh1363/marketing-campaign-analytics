# Data Source & Provenance

## Source

DA-06 uses the **Bank Marketing** dataset from the UCI Machine Learning Repository.

- Dataset ID: `222`
- DOI: `10.24432/C5K306`
- Creators: S. Moro, P. Rita, P. Cortez
- License: **CC BY 4.0**
- Subject area: Business
- Full older-version file used here: `bank-full.csv`
- Population: **45,211 campaign contact records**

The data describes direct-marketing campaigns of a Portuguese banking institution. Campaigns were conducted by phone, and the response variable `y` indicates whether the contacted client subscribed to a term deposit.

## Reproducible acquisition

The repository does not commit the raw dataset. Instead, the acquisition script uses the official UCI Python client:

```bash
python -m src.download_data
```

This writes the source data into `data/raw/`, which is ignored by Git.

## Analytical claim boundary

This is a real public research dataset from UCI, but the repository does not claim access to the bank's internal campaign spend, advertising platform data, CAC, ROAS, or true incremental lift. Therefore DA-06 focuses on **campaign response, contact effectiveness, client segments, prior-campaign context, and conversion patterns** rather than inventing unsupported ROI metrics.

## Citation

Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306
