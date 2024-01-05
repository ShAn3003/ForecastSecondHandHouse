'''
Author: ShAn_3003
Date: 2024-01-05 12:21:41
LastEditTime: 2024-01-05 12:52:27
LastEditors: ShAn_3003
Description: 
FilePath: \ForecastSecondHandHouse\linearmodel.py
'''
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

def train_model(rooms,data):
    data = pd.read_csv(data)
    selected_data = data[data['房间数']==rooms]
    X = selected_data[['面积']]
    y = selected_data['单价']

    # 建立线性回归模型
    model = LinearRegression()
    model.fit(X, y)

    plt.figure(figsize=(16,9))
    plt.scatter(X, y, color='black')
    plt.plot(X.values, model.predict(X), color='blue', linewidth=3)
    plt.xlabel('area')
    plt.ylabel('unitprice')
    plt.title(f'Room:{rooms}')
    plt.savefig("fit.png")

    return model

def predict(area,model):
    return model.predict(area)

if __name__ == "__main__":
    rooms = int(input("请输入房间数："))
    print("正在生成线性回归拟合结果......")
    model = train_model(rooms,"features.csv")
    areas = float(input("请输入面积："))
    areas = np.array([areas]).reshape(-1, 1)    
    price = predict(areas,model)
    print(f"{rooms}室-{areas[0][0]}平方米的预测单位面积价格是：{price[0]}")


