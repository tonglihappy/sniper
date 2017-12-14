import tushare as ts
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

start = "2015-06-12"
end = "2017-12-14"

engine = create_engine('sqlite:///astock.db', echo = False)

conn = sqlite3.connect('astock.db')
cur=conn.cursor()

alreadylist = []

query = "select name from sqlite_master where type='table' order by name"
alreadylist = pd.read_sql(query, conn)

stock = ts.get_stock_basics()
for i in stock.index:
    if i not in list(alreadylist.name):
        print i
        df = ts.get_h_data(i, start=start, end=end,retry_count = 5)
        df = df.sort_index(ascending=True)
        df.to_sql(i, engine, if_exists='append')






