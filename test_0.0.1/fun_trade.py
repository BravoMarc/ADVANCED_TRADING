import time as tm
import datetime 
import pandas as pd
import time as tm
import numpy as np
import json
import pickle
import traceback
import math
import pandas



def obtain_keys():
    f = open ('/home/bravomarc/Desktop/ADVANCED_TRADING/test_0.0.0/pass_Marc','r')
    for i in range(0,6):
        mensaje = f.readline()
        if i==3: api_key=mensaje[:-1]
        if i==5: secret_key=mensaje[:-1]
    f.close()
    
    return api_key , secret_key




def RSI_fly(vector):
    n=len(vector)
    vec_down=[]
    vec_up=[]
    for i in range(1,n):
        diff=vector[i]-vector[i-1]
        if diff<0:
            vec_down.append(abs(diff))
            vec_up.append(0)
        else:
            vec_up.append(diff)
            vec_down.append(abs(0))


    RS=np.mean(vec_up)/np.mean(vec_down)
    RSI=100-100/(1+RS)

    return RSI

    
def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


def sell_buy_f(df_pandas):
    action=[]
    price_action=[]
    action.append(np.nan)
    price_action.append(np.nan)
    num=len(df_pandas["macd_hist"])
    act=0
    for i in range(1,num):
        if df_pandas["macd_hist"][i-1]>=0 and df_pandas["macd_hist"][i]<0 and act==1:
            action.append('sell')
            act=0
            price_action.append(df_pandas["close"][i])
        elif df_pandas["macd"][i]<0 and df_pandas["macd_hist"][i-1]<=0 and df_pandas["macd_hist"][i]>0:
            action.append('buy')
            act=1
            price_action.append(df_pandas["close"][i])
        else:
            action.append(np.nan)
            price_action.append(np.nan)

    df_pandas["action"]=action
    df_pandas["price_action"]=price_action

def ganancias(df_pandas):

    ope=df_pandas[df_pandas['action'].isna()==False][['price_action','action']]
    if ope['action'][0]=='sell':
        ope=ope[1::]
    if ope['action'][-1]=='buy':
        ope=ope[:-1]

    num=len(ope["action"])
    gan=1
    for i in range(0,num,2):
        buy=ope['price_action'][i]
        sell=ope['price_action'][i+1]
        gan*=1+(sell-buy)/buy

    return gan
    