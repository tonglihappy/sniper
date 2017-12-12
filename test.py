from zipline.api import order, record, symbol
from zipline.finance import commission
from zipline import run_algorithm
from toolz import merge
from importlib import import_module
import pandas as pd
import os

from zipline.data.bundles import register

from zipline.data.bundles.viadb import viadb

from zipline.utils.calendars import register_calendar, get_calendar

def initialize(context):
    context.asset = symbol('HSDZ')

    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))

def handle_data(context, data):
    order(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))

def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('HSDZ price (USD)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()

equities1={}
register('sniper',  # name this whatever you like
    viadb(equities1)
)

register_calendar("HSDZ", get_calendar("SHSZ"), force=True)

run_algorithm( initialize=initialize, handle_data=handle_data, analyze=analyze,
        bundle='sniper', environ=os.environ,
         **merge({'capital_base': 1e7}, {
        'start': pd.Timestamp('2014-01-01', tz='utc'),
         'end': pd.Timestamp('2014-11-01', tz='utc'),
}))