import csv
import copy
import os
import json
import calendar
from datetime import date, timedelta
import urllib.request
import locale
import time

locale.setlocale(locale.LC_ALL, 'de_DE')

apiToken = os.getenv('API_TOKEN')

transactions = []
transaction = {
    'Datum': '',
    'Typ': 'Kauf',
    'Wert': '',
    'Buchungswährung': 'EUR',
    'Bruttobetrag': '',
    'Währung Bruttobetrag': '',
    'Wechselkurs': '',
    'Gebühren': '',
    'Steuern': '',
    'Stück': '',
    'ISIN': '',
    'WKN': '',
    'Ticker-Symbol': '',
    'Wertpapiername': '',
}


def createTransaction(item, value, pointInTime):
    newTransaction = copy.copy(transaction)

    tresorAPIUrl = 'https://api.tresor.one/v1/quotes/' + \
        pointInTime.isoformat() + '?isin=' + \
        item['ISIN'] + '&exchange=' + item['Market']

    req = urllib.request.Request(tresorAPIUrl)
    req.add_header('authorization',
                   'Bearer ' + apiToken)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    newTransaction['Datum'] = pointInTime.isoformat() + 'T10:00'
    newTransaction['Wert'] = '{:n}'.format(float(value))
    newTransaction['Stück'] = '{:n}'.format(
        float(value) / float(data['price']))
    newTransaction['ISIN'] = item['ISIN']
    newTransaction['Ticker-Symbol'] = item['Ticker']
    newTransaction['Wertpapiername'] = item['Name']
    return newTransaction


with open('positions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        currentDate = date.fromisoformat(row['Start'])

        if (float(row['Initial']) > 0):
            transactions.append(createTransaction(
                item=row, value=row['Initial'], pointInTime=currentDate))

        if (float(row['Rate']) > 0):
            while (currentDate < date.today()):
                print(currentDate.isoformat(), row['ISIN'])
                transactions.append(createTransaction(
                    item=row, value=row['Rate'], pointInTime=currentDate))
                time.sleep(0.5)

                daysInMonth = calendar.monthrange(
                    currentDate.year, currentDate.month)[1]
                currentDate = currentDate + timedelta(days=daysInMonth)

with open('transactions.csv', 'w', encoding='utf-8', newline='\n') as transactionFile:
    fieldnames = [
        'Datum',
        'Typ',
        'Wert',
        'Buchungswährung',
        'Bruttobetrag',
        'Währung Bruttobetrag',
        'Wechselkurs',
        'Gebühren',
        'Steuern',
        'Stück',
        'ISIN',
        'WKN',
        'Ticker-Symbol',
        'Wertpapiername'
    ]

    writer = csv.DictWriter(
        transactionFile, fieldnames=fieldnames, delimiter=";", lineterminator='\n')
    writer.writeheader()
    writer.writerows(transactions)
