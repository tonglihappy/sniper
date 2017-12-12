#-*- coding: utf-8 -*-
from datetime import datetime
from zipline.algorithm import TradingAlgorithm
from zipline.finance.trading import TradingEnvironment
from zipline.api import order, record, symbol, history, get_datetime
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.utils.calendars import get_calendar
from zipline.data.loader import load_market_data
from numpy.random import randn
import pandas as pd
import numpy as np

#input_data = load_market_data(trading_day="2017-12-06")
# Define algorithm
def initialize(context):
    context.asset = symbol('JDGF')
    print "initialization"
    print context.asset
    pass

def handle_data(context, data):
    #print "handle", n
    close_data = data.history(context.asset, 'close', 5, '1d')#close price

    print close_data

    ma5 =  close_data[-6:-2].mean()
    ma10 = close_data[-11:-2].mean()
    print ma5, ma10

    #取得目前的现金
    cash = context.portfolio.cash
    print cash

    #交易日期
    print get_datetime()
    record(JDGF=data.current(symbol('JDGF'), 'price'),ma5=ma5,ma10=ma10, date=get_datetime())
    #order(symbol('JDGF'), 10)
    #record(JDGF=data.current(symbol('JDGF'), 'price'))

def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    #plt.figure()

    ax1 = plt.subplot(211)#2行一列，选中第一个
    #plt.plot(randn(50), 'k-')
    #print len(results.ma5)

    ax1.plot(results.date,results.ma5)
    #ax1.hist(results.ma5, bins=20,color='red',alpha=0.3)
   # results.portfolio_value.plot(ax=ax1, color='red',legend=u'策略收益')
    #ax1.set_ylabel('Portfolio value (USD)')
    #ax2 = plt.subplot(212, sharex=ax1)
    #results.JDGF.plot(ax=ax2)
    #ax2.set_ylabel('JDGF price (USD)')

    # Show the plot.
    #plt.gcf().set_size_inches(18, 8)
    plt.show()

# 本地化工作开始
def load_t(trading_day, trading_days, bm_symbol):
    # dates = pd.date_range('2001-01-01 00:00:00', periods=365, tz="Asia/Shanghai")

    bm = pd.Series(data=np.random.random_sample(len(trading_days)), index=trading_days)
    tr = pd.DataFrame(data=np.random.random_sample((len(trading_days), 7)), index=trading_days,
                      columns=['1month', '3month', '6month', '1year', '2year', '3year', '10year'])
    return bm, tr

sim_params = create_simulation_parameters(year=2017,
    start=pd.to_datetime("2017-10-18 00:00:00").tz_localize("Asia/Shanghai"),
    end=pd.to_datetime("2017-12-06 00:00:00").tz_localize("Asia/Shanghai"))

trading.environment = TradingEnvironment(load=load_t, bm_symbol='^HSI', exchange_tz='Asia/Shanghai', trading_calendar=get_calendar('SHSZ'))

# setting the algo parameters
algor_obj = TradingAlgorithm(sim_params=sim_params,
            initialize=initialize, handle_data=handle_data,trading_calendar=get_calendar('SHSZ'),
                            env=trading.environment, analyze=analyze)
# data format definition
parse = lambda x: datetime.date(datetime.strptime(x, '%Y/%m/%d'))

# data generator
data_s = pd.read_csv('JDGF.csv', parse_dates=['date'], index_col=0, date_parser=parse)

#print data_s
data_c = pd.Panel({'JDGF': data_s})

perf_manual = algor_obj.run(data_c, False)
# PrintFV
perf_manual.to_csv('myoutput.csv')