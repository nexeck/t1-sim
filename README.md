# Tresore.one Sparplan Simulator

### **Never hand out your API Token**

It has the same power then your username/password

## Requirements

- pipenv
- Get T1 API Token from the `authorization` header

## Run

Add positions into positions.csv (use positions_template.csv)

```sh
API_TOKEN=<token> make run TRANSACTIONS_FILE="<path to generated transactions.csv>" POSITIONS_FILE="<path to input portfolio.csv>" INITIAL_INVEST=<invest in euro> MONTHLY_INVEST=<invest in euro>
```

Upload transactions.csv into a new tresore.one portfolio

## portfolio.csv

- Start: Beginning of recurring transactions and date of initial invest.
- Initial: Initial invest, can be 0 to omit it
- Rate: Rate of recurring transactions, can be 0 to omit it
