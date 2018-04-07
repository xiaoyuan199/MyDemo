# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 12:22:19 2018

@author: Administrator
"""
from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plt

def get_html(url):
    '''
    爬取网页函数
    '''
    head={}
    #写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/                  18.0.1025.166  Safari/535.19'
    try:
        r = requests.get(url,headers=head)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print('get_html()失败')
        
def draw2(dates,temp_hight,temp_low):
    '''
    绘图函数，使用pygal
    '''
    import pygal
    line = pygal.Line(title='一周最高气温和最低气温曲线图',x_title='日期',y_title='温度值（℃）')
    line.x_labels=dates
    line.add('最高气温',temp_hight)
    line.add('最低气温',temp_low)
    line.render_to_file('wendu.svg')
        
def draw(dates,temp_hight,temp_low):
    '''
    绘图函数，使用pyplot
    '''
    #创建一个画布
    fig = plt.figure(dpi=128,figsize=(10,6))
    #导入要绘画的数据
    plt.plot(dates,temp_hight,c='red',alpha=0.5)
    plt.plot(dates,temp_low,c='blue',alpha=0.5)
    #给图表区加颜色
    #plt.fill_between(dates,temp_hight,temp_low,facecolor='blue',alpha=0.1)
    #设置标题
    plt.title('一周最高气温和最低气温曲线图',fontsize=20)
    #设置横坐标标签
    plt.xlabel('日期',fontsize=13)
    #设置纵坐标标签
    plt.ylabel('温度值（℃）',fontsize=13)
    #设置坐标轴参数的大小
    plt.tick_params(axis='both',which='major',labelsize=16)
    #调用fig.autofmt_xdate()来绘制斜 日期标签，以免他们彼此重复。
    #fig.autofmt_xdate()
    plt.show()
    
    
        
        
def get_content(url):
    '''
    解析天气数据
    '''
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    
    day7 = soup.find_all('div',class_='day7')[0]
    #获得日期列表
    date_list = day7.find('ul',class_='week')
    #获得气温列表
    temp_list = day7.find('div',class_='zxt_shuju')
    #准备储存获取到的数据列表
    dates=[]
    temp_hight=[]
    temp_low=[]

    #获取到具体日期值，存到日期列表
    for date in date_list.find_all('li'):
        dates.append(int(date.b.text[-3:-1]))
        
    #获取到具体温度值，存到温度列表
    for temp in temp_list.find_all('li'):
        temp_hight.append(int(temp.span.text))
        temp_low.append(int(temp.b.text))
        
    #调用绘画函数
    draw(dates,temp_hight,temp_low)
    
    #调用绘画函数2，使用pygal
    draw2(dates,temp_hight,temp_low)


if __name__ == '__main__':
    url =  "http://www.tianqi.com/zhuhai/"
    get_content(url)