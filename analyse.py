'''
Author: ShAn_3003
Date: 2024-01-05 11:48:06
LastEditTime: 2024-01-05 12:12:52
LastEditors: ShAn_3003
Description: 
FilePath: \ForecastSecondHandHouse\analyse.py
'''

import pandas as pd

def read_data(data):
    xls=pd.read_excel(data,header=1)
    return xls

def preprocess(xls):
    selected_columns = ['单价','面积','户型']
    xls = xls[selected_columns]
    xls = xls.dropna()
    xls['房间数']=xls['户型'].str.extract('(\d+)').astype(int)
    xls['面积'] = xls['面积'].str.extract('(\d+).?\d*').astype(float)
    features = xls[['房间数','面积','单价']]
    return features
def analyse():
    xls = read_data("data.xlsx")
    features =  preprocess(xls)
    features.to_csv('features.csv',index=False)
    
    

