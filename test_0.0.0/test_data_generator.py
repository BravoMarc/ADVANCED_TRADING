import fun_trade as ft


from binance.client import Client
from binance import ThreadedWebsocketManager

import time as tm
import numpy as np
import threading
import traceback
import pandas as pd


api_key,secret_key = ft.obtain_keys()

client = Client(api_key, secret_key)
tickers=['LINKUSDT']
