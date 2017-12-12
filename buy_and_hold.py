from zipline.api import order, symbol
from zipline.finance import commission
from zipline.finance.trading import TradingEnvironment
from zipline import TradingAlgorithm
from zipline.utils.calendars import get_calendar
import datetime
import pandas as pd

stocks = ['AAPL', 'MSFT']

def initialize(context):
    context.has_ordered = False
    context.stocks = stocks

    # Explicitly set the commission to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))


def handle_data(context, data):
    if not context.has_ordered:
        for stock in context.stocks:
            order(symbol(stock), 100)
        context.has_ordered = True

def analyze():
    pass

#TradingEnvironment(initialize=initialize, handle_data=handle_data,trading_calendar=get_calendar('SHSZ'), analyze=analyze)
algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data, trading_calendar=get_calendar('SHSZ'), analyze=analyze)

parse = lambda x: datetime.date(datetime.strptime(x, '%Y/%m/%d'))

# data generator
data_s = pd.read_csv('JDGF.csv', parse_dates=['date'], index_col=0, date_parser=parse)
#print data_s
data_c = pd.Panel({'JDGF': data_s})

perf_manual = algo.run(data_c)