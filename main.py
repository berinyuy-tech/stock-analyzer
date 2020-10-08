from backend.analyzer import Analyzer
from backend.investor import Investor
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)
stocks_to_invest = ['Apple', 'Google', 'Microsoft', 'AMD', 'Nvidia', 'Paypal']


def analyze():
    results = Analyzer().analyze()
    print(results)


def invest():
    amount = int(input('Please enter the amount of money you want to invest:\n'))
    investments = Investor(amount, stocks_to_invest).invest()
    print(investments)


def main():
    analyze()
    invest()


if __name__ == '__main__':
    main()