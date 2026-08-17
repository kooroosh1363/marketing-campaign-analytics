# Data Dictionary

DA-06 analyzes one row per direct-marketing contact/client record from the UCI Bank Marketing dataset.

## Client attributes

- `age` — client age
- `job` — occupation category
- `marital` — marital status
- `education` — education category
- `default` — credit default indicator
- `balance` — average yearly account balance (older/full dataset variant)
- `housing` — housing loan indicator
- `loan` — personal loan indicator

## Current campaign context

- `contact` — contact communication type
- `day` — last contact day of month
- `month` — last contact month
- `duration` — last contact duration in seconds
- `campaign` — number of contacts performed during the current campaign for this client

## Previous campaign context

- `pdays` — days since the client was previously contacted; special values indicate no previous contact
- `previous` — number of contacts before the current campaign
- `poutcome` — outcome of the previous marketing campaign

## Target

- `response` — derived repository name for UCI target `y`; `yes` means the client subscribed to a term deposit
- `converted` — Boolean analytical version of `response`

## Important leakage warning

`duration` is known only after a phone call has occurred. It is useful for **post-campaign diagnostics**, but it must not be presented as a valid pre-contact targeting feature. Using it to claim prospective targeting performance would leak future information.

## Analytical grain

The repository treats each row as a campaign-contact/client observation. Metrics are aggregated from this grain by job, month, contact method, prior outcome, contact-frequency band, and descriptive customer segment.
