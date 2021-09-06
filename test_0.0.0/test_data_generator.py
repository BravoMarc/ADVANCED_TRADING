
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

api_key,secret_key = ft.obtain_keys()

client = Client(api_key, secret_key)
tickers=['LINKUSDT']
key=tickers[0]

actualtime=dt.today()
interval='5m'
t_end=int(actualtime.strftime('%s')) * 1000 
t_start =int(actualtime.strftime('%s')) * 1000 - 5*14*5*60*1000
bars = client.get_klines(symbol=key, interval=interval, startTime=t_start,endTime=t_end)
historical=pd.DataFrame(columns=['CLOSE','High','low','date'], index=tickers)
historical['CLOSE'][key]=[]
historical['High'][key]=[]
historical['low'][key]=[]
historical['date'][key]=[]
for line in bars:
    historical['High'][key].append(float(line[2]))
    historical['low'][key].append(float(line[3]))
    historical['CLOSE'][key].append(float(line[4]))
    historical['date'][key].append(time.strftime('%H:%M:%S', tm.localtime(line[6]/1000)))


high=np.asarray(historical['High'][key])
low =np.asarray(historical['low'][key])
close=np.asarray(historical['CLOSE'][key])

print(close[-1])
print(ta.RSI(close,timeperiod=14)[-1] )
print('')
df=pd.Series(historical['CLOSE'][key])
#print(pdt.rsi(df[0],length=14))

slowk, slowd = ta.STOCH(high, low, close, fastk_period=14,
 slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

print(slowk[-1])
print(slowd[-1])
print('')
dfhigh=pd.Series(historical['High'][key])
dflow=pd.Series(historical['low'][key])

stoch=pdt.stoch(dfhigh,dflow,df,k=14, d=3, smooth_k=3, mamode=None, offset=None,)
print(stoch.iloc[-1,:])

macd=pdt.macd(df)


macd, signal, hist=ta.MACD(close,fastperiod=12,slowperiod=26, signalperiod=9)

print(macd[-1])
print(signal[-1])
print(hist[-1])


