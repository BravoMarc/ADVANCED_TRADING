import time as tm
import datetime 
import pandas as pd
import time as tm
import numpy as np
import json
import pickle
import traceback
import math



def obtain_keys():
    f = open ('/home/bravomarc/Desktop/ADVANCED_TRADING/test_0.0.0/pass_Marc','r')
    for i in range(0,6):
        mensaje = f.readline()
        if i==3: api_key=mensaje[:-1]
        if i==5: secret_key=mensaje[:-1]
    f.close()
    
    return api_key , secret_key