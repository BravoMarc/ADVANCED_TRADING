# %%
from os import lchown
import matplotlib
import fun_trade as ft


from binance.client import Client
from binance import ThreadedWebsocketManager

import time as tm
import numpy as np
import threading
import traceback
import pandas as pd
from datetime import datetime as dt
import time
import matplotlib.pyplot as plt
import talib as ta
import pandas_ta as pdt
import mplfinance as mpf

api_key,secret_key = ft.obtain_keys()

client = Client(api_key, secret_key)
tickers=['LINKUSDT']
key=tickers[0]

actualtime=dt.today()
interval='1d'
t_end=int(actualtime.strftime('%s')) * 1000 
t_start =int(actualtime.strftime('%s')) * 1000 - 5*26*(24*60)*60*1000
bars = client.get_klines(symbol=key, interval=interval, startTime=t_start,endTime=t_end)
close=[]
high=[]
open=[]
low=[]
date=[]
volume=[]
for line in bars:
    open.append(float(line[1]))
    high.append(float(line[2]))
    low.append(float(line[3]))
    close.append(float(line[4]))
    volume.append(float(line[5]))
    date.append(time.strftime('%m/%d/%Y %H:%M:%S', tm.localtime(line[6]/1000)))



df_pandas=pd.DataFrame({'open':open,'high': high,'low': low, 'close': close, 'volume': volume})
df_pandas.index=pd.to_datetime(date)
mpf.plot(
            df_pandas,
            type='candle',
            title='LINKUSDT, March - 2020',
            ylabel='Price ($)', style="binance"
        )
mpf.show()

macd, signal, hist=ta.MACD(np.asarray(close),fastperiod=12,slowperiod=26, signalperiod=9)

df_pandas["macd"]=macd
df_pandas["macd_signal"]=signal
df_pandas["macd_hist"]=hist
ft.sell_buy_f(df_pandas)
print(ft.ganancias(df_pandas))

# macd panel
colors = ['g' if v >= 0 else 'r' for v in df_pandas["macd_hist"]]
macd_plot = mpf.make_addplot(df_pandas["macd"], panel=1, color='fuchsia', title="MACD")
macd_hist_plot = mpf.make_addplot(df_pandas["macd_hist"], type='bar', panel=1, color=colors) # color='dimgray'
macd_signal_plot = mpf.make_addplot(df_pandas["macd_signal"], panel=1, color='b')
colors = ['g' if v == 'buy' else 'r' for v in df_pandas["action"]]
buy_sell_plot = mpf.make_addplot(df_pandas["price_action"],type='scatter' ,color=colors)

plots = [macd_plot, macd_signal_plot, macd_hist_plot,buy_sell_plot]
mpf.plot(df_pandas, type='candle', style='binance', addplot=plots, title="LINKUSDT", volume=False, volume_panel=2, ylabel='', ylabel_lower='',savefig='testsave.png')

print(ft.ganancias(df_pandas))


# %%
