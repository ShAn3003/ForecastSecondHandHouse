# 导入要使用到的库
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import os
import re


def get_data(url, headers):
    """
    请求函数，向网页发起请求
    :param url: 网址
    :param headers: 请求头信息,里面有User-Agent内容
    :return:返回得到网页数据
    """
    proxies =  {
        "http":"http://localhost:7890",
        "https":"http://localhost:7890"
    }
    datas = requests.get(url, headers,proxies=proxies)
    return datas.text


def analyse_province(data):
    """
    解析主页面的省份信息
    :param data: 请求一级网页得到的数据
    :return: 返回一个序号对应省份的字典数据
    """
    bs_data = BeautifulSoup(data, 'lxml')
    provinces_data = bs_data.find_all('div', {'class': 'city_list_tit c_b'})  # 使用beautifulsoup库解析省份
    provinces = {}
    for i in range(len(provinces_data)):
        provinces[i] = (provinces_data[i].string)
    return provinces


def analyse_city(data, province):
    """
    根据所选的省份解析主页面的城市
    :param data:请求一级网页得到的数据
    :param province:所选省份的序号
    :return:返回一个序号对应该省份的城市的字典数据
    """
    bs_data = BeautifulSoup(data, 'lxml')
    # 根据所选省份得到源码中省份的整个div内容
    p_data = bs_data.find_all('div', {'class': 'city_province'})[province]
    x_data = etree.HTML(str(p_data))
    # 用xpath语法对得到的div进行解析，得到该省份下的城市和主页链接
    city_list = x_data.xpath('//div[@class="city_province"]/ul/li/a/text()')
    urls = x_data.xpath('//div[@class="city_province"]/ul/li/a/@href')
    citys = {}
    for i in range(len(city_list)):
        citys[i] = city_list[i]
        # 这里作这样的处理是为了二级页面直接是二手房板块
        urls[i] = urls[i] + 'ershoufang/pg{}/'
    return citys, urls


def get_page(data):
    """
    在二级页面的第一页解析出总页数
    :param data:请求二级页面的第一页得到的数据
    :return:返回一个表示页数的int数据
    """
    x_path = etree.HTML(data)
    total_page = x_path.xpath('//div[@class="page-box fr"]/div/@page-data')
    # 上面得到是一个字典形式的字符串数据，得到页数还要进一步解析
    page = re.match(r'.*?talPage":(.*?),"curPage', str(total_page))
    return int(str(page.group(1)))  # 以int类型返回，直接用在循环中


def get_model(infor):
    """
    从一次解析得到的文本中二次解析得到房屋户型信息
    :param infor: 一次解析得到的文本
    :return: 房屋户型信息的字符串类型
    """
    model = re.match('^(.*?)\s', infor)
    return model.group(1)


def get_area(infor):
    """
    从一次解析得到的文本中二次解析得到房屋面积信息
    :param infor: 一次解析得到的文本
    :return: 房屋面积信息的字符串类型
    """
    area = re.match('^(.*?)\s\|\s(.*?)\s\|\s', infor)
    return area.group(2)


def get_follow(atten):
    """
    从一次解析的关注度及发布时间文本中二次解析出房屋关注度信息
    :param atten: 一次解析的关注度及发布时间文本
    :return: 房屋关注度
    """
    follow = re.match('^(\d+)人关注', atten)
    return follow.group(1)


def get_day(atten):
    """
    一次解析的关注度及发布时间文本中二次解析出发布时间信息
    :param atten: 一次解析的关注度及发布时间文本
    :return: 发布时间字符串类型
    """
    day = re.match('.*?关注\s/\s(.*?)$', atten)
    return day.group(1)


def get_unitprice(up):
    """
    从一次解析的文本中解析出单价数据
    :param up: 一次解析的文本
    :return: int类型单价数据
    """
    p = re.match('^(\d+),(\d+)元/平$', up)
    return int(str(p.group(1))+str(p.group(2)))


def analyse_house(data):
    """
    解析所选城市的单页信息，调用前面已经定义的函数
    :param data: 请求单页返回的数据
    :return: 返回一个所有信息综合的二维列表
    """
    val = BeautifulSoup(data, 'lxml')
    # 解析出标题
    titles = val.find_all('a', {'target': '_blank', 'data-el': 'ershoufang'})[1::2]
    x_val = etree.HTML(data)
    # pngs = x_val.xpath('//img[@class="lj-lazy"]/@data-original')  # 解析出图片链接
    prices = val.find_all(class_='totalPrice totalPrice2')  # 解析出总价的板块
    infors = x_val.xpath('//div[@class="houseInfo"]/text()')  # 解析出户型等信息的文本
    attens = x_val.xpath('//div[@class="followInfo"]/text()')  # 解析出关注度等信息的文本
    ups = x_val.xpath('//div[@class="unitPrice"]/span/text()')  # 解析出单价的文本
    information = [[], [], [], [], [], [], [], []]  # 用来存所有一页信息的二维列表
    # 解析出真正想要的数据并保存到information列表中
    for title, p, infor, atten,up in zip(titles, prices, infors, attens, ups):
        information[0].append(title.string)  # 地址
        information[1].append(get_model(infor))  # 户型
        information[2].append(get_area(infor))  # 面积
        information[3].append(get_unitprice(up))  # 单价
        information[4].append(float(str(p.span.string)))  # 总价
        information[5].append(int(get_follow(atten)))  # 关注度
        information[6].append(get_day(atten))  # 发布时间
        information[7].append(title['href'])  # 链接
        # save_png(png, title)  # 保存图片
    return information


def merge_data(all_data, information):
    """
    将多页爬取到的信息汇总成一个二维列表
    :param all_data: 存每一页数据的二维列表
    :param information: 单页数据的二维列表
    :return: 汇总后的总数据列表
    """
    for i in range(8):
        all_data[i] += information[i]
    return all_data


def draw_picture(all_data, name):
    """
    画出分析单价与关注度、总价与关注度之间的散点图并保存
    :param all_data: 所有数据汇总的数据集
    :param name: 爬取的城市名
    :return: null
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.subplot(2, 1, 1)  # 绘制子图1
    plt.xlabel('单价（元/平）')
    plt.ylabel('关注度/人')
    plt.scatter(all_data[3], all_data[5])
    plt.subplot(2, 1, 2)  # 绘制子图2
    plt.xlabel('总价/万元')
    plt.ylabel('关注度/人')
    plt.scatter(all_data[4], all_data[5])
    # 保存图片
    plt.savefig('{}二手房可视化图像.jpg'.format(name))
    # 展示图片
    plt.show()


def get_max(all_data):
    """
    获取关注度最高的单价和总价信息
    :param all_data: 所有数据汇总的数据集
    :return: 返回关注度最高的单价和总价信息
    """
    max_follow = all_data[5].index(max(all_data[5]))
    return all_data[3][max_follow], all_data[4][max_follow]


def save_data(all_data):
    """
    保存所有数据到excel中
    :param all_data: 所有数据汇总的数据集
    :return: null
    """
    all_data = np.array(all_data)
    all_data = all_data.T
    # 增加表头
    name = ['地址', '户型', '面积', '单价', '总价', '关注度', '发布时间', '链接']
    all_data = np.insert(all_data, 0, name, axis=0)
    all_data = pd.DataFrame(all_data)
    all_data.to_excel('./data.xlsx', sheet_name='数据', index=False, engine='openpyxl')

def get_provinces():
    provinces = analyse_province(city_data)
    return provinces
# 一级页面
city_url = 'https://www.lianjia.com/city/'
headers = {  # 请求头
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
city_data = get_data(city_url, headers)
urls=None
def get_city(index):
    global urls
    citys, urls= analyse_city(city_data, index)
    return citys
def craw_data(city_idx):
    # 总数据集，保存的依次为地址、户型、面积、单价、总价、关注度、发布时间
    all_data = [[], [], [], [], [], [], [], []]
    page = get_page(get_data(urls[city_idx].format(1), headers))
    # 爬取多页
    print(f"正在从{city_url}爬取二手房信息：")
    for pn in tqdm(range(1, page)):
        href = urls[city_idx].format(pn)
        # 程序暂停2秒，避免爬取过快而被封IP
        time.sleep(1)
        # print('正在爬取第{}页'.format(pn))
        two_hand_data = get_data(href, headers)
        information = analyse_house(two_hand_data)
        all_data = merge_data(all_data, information)
    # max_follow_unitprice, max_follow_price = get_max(all_data)
    # print('关注度最高的单价：', max_follow_unitprice, '元/平')
    # print('关注度最高的房屋总价：', max_follow_price, '万元')
    print('数据量：', len(all_data[0]))
    save_data(all_data)
    # draw_picture(all_data, citys[city_ind])
