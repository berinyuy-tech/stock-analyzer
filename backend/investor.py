import pandas as pd

from backend.analyzer import Analyzer


class Investor:
    def __init__(self, amount, stocks_to_invest):
        self.amount = amount
        self.stocks_to_invest = stocks_to_invest

    def invest(self):
        results = Analyzer().analyze()
        changes = []
        for stock in self.stocks_to_invest:
            avg_change = int(float(results.loc[stock]['avg_1Y_change'][1:]) * 100)
            changes.append(avg_change)
            print(avg_change)
        columns = None
        output = []
        for i, stock in enumerate(self.stocks_to_invest):
            row = {
                'amount_to_invest': int(self.amount * (changes[i] / sum(changes)))
            }
            output.append(row)
        output = pd.DataFrame(output, index=self.stocks_to_invest, columns=['amount_to_invest'])
        return output