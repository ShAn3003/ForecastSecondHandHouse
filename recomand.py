'''
Author: ShAn_3003
Date: 2024-01-05 12:55:42
LastEditTime: 2024-01-05 21:39:39
LastEditors: ShAn_3003
Description: 
FilePath: \ForecastSecondHandHouse\recomand.py
'''
import pandas as pd


def recomand(rooms,areas,data='data.xlsx'):
    

    xls = pd.read_excel(data,header=1)

    xls['房间数']=xls['户型'].str.extract('(\d+)').astype(int)
    xls['面积'] = xls['面积'].str.extract('(\d+).?\d*').astype(float)
    # 选择相似的房间数和在给定面积范围内上下浮动20的数据
    selected_data = xls[
        (xls['房间数'] == rooms) &
        (xls['面积'] >= areas - 20) & 
        (xls['面积'] <= areas + 20)
    ]

    # 获取前十条数据
    result = selected_data.head(10).to_dict(orient='records')
    return result

if __name__ == "__main__":
    rooms = 3
    areas = 150
    result=recomand(rooms,areas,'data.xlsx')
    print(result)



