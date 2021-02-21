import csv
import json
import copy
import os
import calendar
from datetime import date, timedelta
import urllib.request
import locale
import time
import math

import sys
import getopt

locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')

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


def generateTransactions(positionsFileName, transactionsFileName, initialInvest, monthlyInvest):
    with open(positionsFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            currentDate = date.fromisoformat(row['Start'])

            initialQuote = float(row['InitialQuota'])
            if (initialInvest != None and initialInvest > 0 and initialQuote > 0):
                initialValue = math.ceil(initialInvest / 100 * initialQuote)
                print(currentDate.isoformat(), "Initial",
                      row['ISIN'], initialValue)
                transactions.append(createTransaction(
                    item=row, value=initialValue, pointInTime=currentDate))

            monthlyQuote = float(row['MonthlyQuote'])
            if (monthlyInvest != None and monthlyInvest > 0 and monthlyQuote > 0):
                monthlyValue = math.ceil(monthlyInvest / 100 * monthlyQuote)
                while (currentDate < date.today()):
                    print(currentDate.isoformat(), "Monthly",
                          row['ISIN'], monthlyValue)
                    transactions.append(createTransaction(
                        item=row, value=monthlyValue, pointInTime=currentDate))
                    time.sleep(0.5)

                    daysInMonth = calendar.monthrange(
                        currentDate.year, currentDate.month)[1]
                    currentDate = currentDate + timedelta(days=daysInMonth)

    with open(transactionsFileName, 'w', encoding='utf-8', newline='\n') as transactionFile:
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


def main(argv):
    positionsFileName = ''
    transactionsFileName = 'transactions.csv'
    initialInvest = None
    monthlyInvest = None
    try:
        opts, args = getopt.getopt(
            argv, "p:t:i:m:", ["pfile=", "tfile=", "initial=", "monthly="])
    except getopt.GetoptError:
        print('Wrong params')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--pfile"):
            positionsFileName = arg
        elif opt in ("-t", "--tfile"):
            transactionsFileName = arg
        elif opt in ("-i", "--initial"):
            initialInvest = float(arg)
        elif opt in ("-m", "--monthly"):
            monthlyInvest = float(arg)

    generateTransactions(
        positionsFileName, transactionsFileName, initialInvest, monthlyInvest)


if __name__ == "__main__":
    main(sys.argv[1:])
