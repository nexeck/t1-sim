# Tresore.one Sparplan Simulator

## Requirements

- pipenv
- Get T1 API Token from the `authorization` header

## Run

Add positions into positions.csv

```sh
API_TOKEN=<token> make run
```

Upload transactions.csv into a new tresore.one portfolio

## portfolio.csv

- Start: Beginning of recurring transactions and date of initial invest.
- Initial: Initial invest, can be 0 to omit it
- Rate: Rate of recurring transactions, can be 0 to omit it
