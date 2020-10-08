import glob
import pandas as pd
import os
import datetime
from backend.data_merge import DataMerge

rows_in_year = 251  # number of working days in a year


class Analyzer:
    def __init__(self):
        self.stocks = list(os.walk('stocks data'))[0][1]
        self.__data = {}
        for stock in self.stocks:
            data_URL = 'stocks data/' + stock
            stock_data = DataMerge(data_URL).get_data()
            self.__data[stock] = stock_data

    def price(self, price):
        if isinstance(price, str):
            return float(price.replace(',', ''))
        return price

    def average_change(self, stock, window):
        """
        calculates the average expected change in stock price in a window of days

        :param stock: string
        :param window: int
        :return: float
        """
        data = self.__data[stock]
        changes = []
        for i in range(len(data) - window):
            price_later = self.price(data.iloc[i]['Close'])
            price_earlier = self.price(data.iloc[i + window]['Close'])
            changes.append((price_later - price_earlier) / price_earlier)
        return f'%{round(100 * sum(changes) / len(changes), 2)}'

    def expected_current_price(self, stock, window):
        avg_change = float(self.average_change(stock, window)[1:]) / 100
        price_earlier = self.price(self.__data[stock].iloc[window]['Close'])
        expected_price = price_earlier + price_earlier * avg_change
        return round(expected_price, 2)

    def analyze(self):
        columns = None
        output = []
        for stock in self.stocks:
            row = {
                'current_price': self.__data[stock].iloc[0]['Close'],
                'avg_1Y_change': self.average_change(stock, rows_in_year),
                'expected_current_1Y_price': self.expected_current_price(stock, rows_in_year),
                'avg_6M_change': self.average_change(stock, rows_in_year // 2),
                'expected_current_6M_price': self.expected_current_price(stock, rows_in_year // 2),
                'avg_3M_change': self.average_change(stock, rows_in_year // 4),
                'expected_current_3M_price': self.expected_current_price(stock, rows_in_year // 4),
            }
            columns = row.keys()
            output.append(row)
        output = pd.DataFrame(output, columns=columns, index=self.stocks)
        output.to_csv('analysis.csv')
        print('CSV file with the analysis results is saved in analysis.csv')
        return output
