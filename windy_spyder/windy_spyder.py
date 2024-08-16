from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
# pipreqs ./ --encoding=utf-8
'''
windy天气获取，这是一个漫长的过程，这里只提供示例性爬虫的程序，实际项目使用可以的在此基础上修改。
'''

#打开网址获取经过JAVA渲染的页面HTML文件，不是源码
def get_elements():
    co = ChromiumOptions().headless()
    page = ChromiumPage(co)
    # url中包含地区的经纬度。自定义爬取地址的经纬度。便可实现全国天气数据的获取
    page.get('https://www.windy.com/multimodel/37.856/112.556?37.366,112.558,8,i:pressure')
    ele = page.ele('@class =models')
    html = BeautifulSoup(ele.html, 'lxml')
    htmls = html.findAll('div', 'model-box')
    return htmls


'''
这个地方有问题，后期需要改正，这是为了保证每次请求都请求到完整颜页面内容，
若有人看到这个代码，有自己更好的想法可以留言提出，非常感谢
'''
while True:
    htmls = get_elements()
    if len(htmls) == 4:
        break

for html in htmls:
    label = html.find('div', 'legend-days height-days').find('span', 'legend-both').text
    table = html.find('div', 'forecast-table')
    time_list = [i.text for i in table.find('tr', 'td-hour height-hour d-display-table').find_all('td')]
    temp_list = [i.text for i in table.find('tr', 'td-temp height-temp d-display-table').find_all('td')]
    temp_list = [re.findall(r'\d+', temp)[0] for temp in temp_list]
    data = pd.DataFrame({'time': time_list, 'temp': temp_list})
    data.to_csv('{}.csv'.format(label), index=False)
