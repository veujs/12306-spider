
# -*- coding: utf-8 -*-

import urllib.request
from json import loads  # 导入json模块，用于将jon语言转换为相对应的python语言

# url为所要访问的网址
url = "https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2018-09-25&leftTicketDTO." \
      "from_station=EAY&leftTicketDTO.to_station=HTV&purpose_codes=ADULT"

# headers为
# 用来包装头部的数据：
# User-Agent ：这个头部可以携带如下几条信息：浏览器名和版本号、操作系统名和版本号、默认语言
# Referer：可以用来防止盗链，有一些网站图片显示来源http://***.com，就是检查Referer来鉴定的
# Connection：表示连接状态，记录Session的状态。
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit'
                 '/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
    'Connection':'keep-alive'
}

# Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
# 使用request（）来包装请求，再通过urlopen（）获取页面。
req = urllib.request.Request(url,headers=headers)


def get_list():
    """
    获取网页requests请求的的返回,
    :return: 返回result中的结果.list
    """
    html = urllib.request.urlopen(req).read()
    # html = html.decode('utf-8')  # 将返回的json语言中乱码部分转化打印
    html_dict = loads(html)  # 转化json为python语言重点的 字典
    # print(html)
    # print(type(html))
    # print(html_dict)
    # print(type(html_dict))
    # print(html_dict["data"])
    # print(html_dict["data"]["result"])  # 返回result的结果
    return html_dict["data"]["result"]  # 返回类型为list
    pass


# print(dict(get_list()))
# get_list()切片后的索引对应关系
# 1 ：预定
# 3 ：车次
# 4 ：始发站
# 5 ：终点站
# 6 ：出发站（已选择）
# 7 ：到达站（已选择）
# 8 ：出发时间
# 9 ：到达时间
# 10：历史时长
# 21：高级软卧
# 23：软卧
# 26：无座
# 28：硬卧
# 29：硬座
# 30：二等座
# 31：一等座
# 32：商务座、特等座
# 33：动卧


def get_trains_list():
    """
    将get_list()的返回的值，进行切片处理
    :return: 列车列表数组trains，列表中的每一项元素仍为列表（代表一趟车次的所有信息）
    """
    a = 0  # 初始化数组下标值
    index = 0    # 初始化列车列表数组的下标
    trains_list = []  # 初始化列车列表数组
    for i in get_list():
        trains_list.append([])

        for j in i.split("|"):
            # print("[%s]:%s" % (a, j))  # 循环打印切片后的字符串
            trains_list[index].append(j)
            a += 1

        index += 1  # 列车列表数组下标值+1
    return trains_list  # 返回列车列表


def print_trains_list(args=[]):
    """
    打印列车列表数组
    :param args: list
    """
    for i in args:
        # 打印我们所需要的数据
        print('火车：%s' % (i[3]))
        print('出发地：%s' % (i[6]))
        print('目的地：%s' % (i[7]))
        print('发车时间：%s' % (i[8]))
        print('到达时间：%s' % (i[9]))
        print('历时时间：%s' % (i[10]))
        print('商务座/特等座：%s' % (i[32]))
        print('一等座：%s' % (i[31]))
        print('二等座：%s' % (i[30]))
        print('高级软卧：%s' % (i[21]))
        print('软卧：%s' % (i[23]))
        print('硬卧：%s' % (i[28]))
        print('硬座：%s' % (i[29]))
        print('无座：%s' % (i[26]))
        print('\n\t')
    # pass


trains_list = get_trains_list()
print_trains_list(trains_list)




