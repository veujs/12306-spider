# @Time 			: 2018/09/14
# @Author			: 王志鹏
# @File 			: GrabTicketOperation.py
# @Software			: PyCharm
# @Python Version	: 3.7
# @About 			: 12306抢票操作类

# import splinter.browser import Browser
import urllib
import urllib.request
import requests
import ssl
import city
from json import loads
from GrabTicketSmtp import GrabTicketSmtp
import GrabTicket
# import urllib.parse


class GrabTicketOperation(object):  # 创建****类

    from_station = ""
    to_station = ""
    setOutTime = ""

    _jc_save_wfdc_flag = ""

    durl = "https://kyfw.12306.cn/otn/leftTicket/query?"

    # 构造函数
    def __init__(self, query_param_dict):
        self.session = GrabTicket.ss
        self.from_station = query_param_dict["from_station"]
        self.to_station = query_param_dict["to_station"]
        self.setOutTime = query_param_dict["setOutTime"]

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'kyfw.12306.cn',
            # "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
            "User-Agent":
                        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
            # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

        }


    # 拼接URL地址
    def getSplicingUrl(self):
        url = self.durl + 'leftTicketDTO.train_date='\
              + urllib.request.quote(self.setOutTime) \
              + '&leftTicketDTO.from_station=' \
              + urllib.request.quote(self.from_station) \
              +'&leftTicketDTO.to_station=' \
              + urllib.request.quote(self.to_station) \
              + '&purpose_codes=ADULT'
        return url


    def leftTicketInit(self):

        durl = "https://kyfw.12306.cn/otn/leftTicket/init"

        # self.headers["Referer"] = "https://kyfw.12306.cn/otn/index/initMy12306"
        if GrabTicket.cookies_print_code == "1":
            print("leftTicketInit_start>>>",self.session.cookies.get_dict())

        response = self.session.get(url=durl,headers=self.headers)

        if GrabTicket.cookies_print_code == "1":
            print("leftTicketInit_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            # print("response.text>>>",loads(response.text))

        # self.headers["Referer"] = "https://kyfw.12306.cn/otn/index/initMy12306"
        # durl2 = "https://ad.12306.cn/res/0004.html"
        # # durl2 = "https://ad.12306.cn/sdk/webservice/rest/appService/getAdAppInfo.json?placementNo" \
        #        # "=0004&clientType=2&billMaterialsId=84704f7fcb4345a2a1b88639dc1bd689"
        #
        # response = self.session.get(url=durl2,headers=self.headers)


        pass


    def curlTrainInfo(self):
        """
        查询车票信息
        :return:返回get请求返回的 response_dict["data"]["result"]  # 返回类型为list
        """
        # 获取链接
        url = self.getSplicingUrl()
        print(url)
        # TODO 测试使用
        # print(url)
        # 请求头

        self.leftTicketInit()
        # durl2 = "https://ad.12306.cn/res/0004.html"
        # # durl2 = "https://ad.12306.cn/sdk/webservice/rest/appService/getAdAppInfo.json?placementNo" \
        #        # "=0004&clientType=2&billMaterialsId=84704f7fcb4345a2a1b88639dc1bd689"
        #
        # response = self.session.get(url=durl2,headers=self.headers)

        # self.session.cookies.set("_jc_save_fromDate","2018-10-12")
        # self.session.cookies.set("_jc_save_fromStation","%u897F%u5B89%u5317%2CEAY")
        # self.session.cookies.set("_jc_save_toDate", "2018-10-12")
        # self.session.cookies.set("_jc_save_toStation","%u6D2A%u6D1E%u897F%2CHTV")
        # self.session.cookies.set("_jc_save_wfdc_flag","dc")
        # self.session.cookies.set("current_captcha_type","Z")
        # self.session.cookies.set("RAIL_DEVICEID", "VLbl9zPKArF4ljn709p_19M4jfqhf6Du1kuGEm7fx1j1vv7Rh6Achh1jM0Kd-v_f0B8ZEk7qfX_MML3N3hwspQ_np6CM9Nw5nJFusaJAYc6EyO7OlO8LuyqzFDFHdm04_6SijMmfGl3QWB5ekP-cKue_SwikuEqo")
        # self.session.cookies.set("RAIL_EXPIRATION", "1538264515981")


        if GrabTicket.cookies_print_code == "1":
            print("curlTrainInfo_start>>>",self.session.cookies.get_dict())

        response = self.session.get(url=url,headers=self.headers, verify=False) # 必须使用post请求来发送带数据的

        if GrabTicket.cookies_print_code == "1":
            print("curlTrainInfo_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>",loads(response.text))

        # 格式化json数据
        response_dict = loads(response.text)  # 转化json为python语言重点的字典
        print(response_dict)
        # 获取想要的数据
        result = response_dict["data"]["result"]  # 返回类型为list
        print(result)
        return result


    def handleResultDatas(self,data):
        """
        处理curlTrainInfo返回的列车信息，
        :param data:
        :return:
        """
        a = 0
        index = 0
        trains_list = []
        for i in data:
            trains_list.append([])

            for j in i.split("|"):
                # print("[%s]:%s"% (a, j))  # 打印“|”切片后的字符串
                trains_list[index].append(j)
                a += 1
            print(trains_list[index])
            index += 1 # 列表索引递增


        return trains_list


    def getStandbyTicketTrainsList(self, trains_list):
        """
        在控制台输出有票的所有车次的信息
        :param trains_list:
        """
        standbyTicketTrainsList = []
        titleTrainInfo = []
        index = 0
        for train_list in trains_list:
            self.isIntTrain = self.stringToInt(train_list)  # 获取该趟车中是否有“数字形式”的余票信息

            if train_list[32] == "有" or train_list[31] == "有" or train_list[30] == "有" or train_list[21] == "有" \
                or train_list[23] == "有" or train_list[28] == "有" or train_list[29] == "有"or train_list[26] == "有" \
                or self.isIntTrain == True: # 确定该趟车次中是否有有余票，包含“有”or“数字形式”

                standbyTicketTrainsList.append({})
                standbyTicketTrainsList[index]["序号"] = str(index)
                standbyTicketTrainsList[index]["车次"] = train_list[3]
                standbyTicketTrainsList[index]["出发站"] = city.get_city(train_list[6])
                standbyTicketTrainsList[index]["到达站"] = city.get_city(train_list[7])
                standbyTicketTrainsList[index]["出发时间"] =train_list[8]
                standbyTicketTrainsList[index]["到达时间"] = train_list[9]
                standbyTicketTrainsList[index]["历时"] = train_list[10]
                standbyTicketTrainsList[index]["商务座"] = train_list[32]
                standbyTicketTrainsList[index]["一等座"] = train_list[31]
                standbyTicketTrainsList[index]["二等座"] = train_list[30]
                standbyTicketTrainsList[index]["软卧"] = train_list[23]
                # standbyTicketTrainsList[index]["动卧"] = i[33]
                standbyTicketTrainsList[index]["硬卧"] = train_list[28]
                # allTrainInfo[index1]["软座"] = i[3]
                standbyTicketTrainsList[index]["硬座"] = train_list[29]
                standbyTicketTrainsList[index]["无座"] = train_list[26]
                standbyTicketTrainsList[index]["secretStr"] = train_list[0]
                index += 1

        titleTrainInfo = ["序号","车次","出发站","到达站", "出发时间","到达时间","历时时间",
            "商务座","一等座","二等座","软卧",
            # "动卧",
            "硬卧",
            # "软座",
            "硬座","无座","secretStr"
        ]
        print("---------------------------------------有票的车次如下------------------------------------------------------------------------------------------")
        for i in titleTrainInfo:
            # print("{:^}".format(self.myAlign(i,10)), end="")
            print(self.myAlign(i, 10), end="")
        print("")
        # 打印列车信息
        for i in standbyTicketTrainsList:
            for j in i.values():
                print(self.myAlign(j,10),end="")
                # print("{:^}".format(self.myAlign(j,10)), end="")
            print("")
        print("---------------------------------------有票的车次如上------------------------------------------------------------------------------------------")
        return standbyTicketTrainsList




    def isCheckValueInt(self,value):
        value = int(value)

        if value > 0:
            self.intTrain = True
            return True
        else:
            return False


    def stringToInt(self,train_list):

        # rr = "adfas"
        # rr.isdigit()

        # 商务座、特等座
        if train_list[32].isdigit():  # 判断商务座对应的字符串是否全为数字组成
            if self.isCheckValueInt(train_list[32]):
                return True

        # 一等座
        if train_list[31].isdigit():
            if self.isCheckValueInt(train_list[31]):
                return True

        # 二等座
        if train_list[30].isdigit():
            if self.isCheckValueInt(train_list[30]):
                return True

        # 高级软卧
        if train_list[21].isdigit():
            if self.isCheckValueInt(train_list[21]):
                return True

        # 软卧
        if train_list[23].isdigit():
            if self.isCheckValueInt(train_list[23]):
                return True

        # 硬卧
        if train_list[28].isdigit():
            if self.isCheckValueInt(train_list[28]):
                return True

        # 硬座
        if train_list[29].isdigit():
            if self.isCheckValueInt(train_list[29]):
                return True

        # 无座
        if train_list[26].isdigit():
            if self.isCheckValueInt(train_list[26]):
                return True


    def outputResult(self,trains_list):
        """
        整理数据转化为html语言，供邮件发送
        :param trains_list:
        :return:
        """
        content = ""
        # self.traincontents = []
        num = 1
        for train_list in trains_list:
            self.isIntTrain = self.stringToInt(train_list)

            if train_list[32] == "有" or train_list[31] == "有" or train_list[30] == "有" or train_list[21] == "有" \
                or train_list[23] == "有" or train_list[28] == "有" or train_list[29] == "有"or train_list[26] == "有" \
                or self.isIntTrain == True:

                # 定义一个列表 存放 某车次的【票的信息--例：有 or 无 or 数字】
                self.traincontents = []

                # 填充html文件中，车次表格的 前缀
                traincontent_prefixs = [
                    '<tr>',                           # html中应该指的是一行的开始标志
                    '<td>' + str(num) + '</td>',    # 序号
                    '<td>' + train_list[3] + '</td>',   # 车次
                    '<td>' + city.get_city(train_list[6]) + '</td>',   # 出发地
                    '<td>' + city.get_city(train_list[7]) + '</td>',   # 目的地
                    '<td>' + train_list[8] + '</td>',   # 出发时间
                    '<td>' + train_list[9] + '</td>',   # 到达时间
                    '<td>' + train_list[10] + '</td>'   # 历时时间
               ]
                # 链接字符串 -- traincontent_prefixs中的html合并
                traincontent_prefix = ''.join(traincontent_prefixs)

                traincontent_suffix = '</tr>'   # 一行结束标志

                num += 1

                # 下面为获取座位类别下 是否有余票，填充到
                self.getIsStandbyTicket(train_list[32])
                self.getIsStandbyTicket(train_list[31])
                self.getIsStandbyTicket(train_list[30])
                self.getIsStandbyTicket(train_list[21])
                self.getIsStandbyTicket(train_list[23])
                self.getIsStandbyTicket(train_list[28])
                self.getIsStandbyTicket(train_list[29])
                self.getIsStandbyTicket(train_list[26])

                traincontent = ''.join(self.traincontents)

                content = content + traincontent_prefix + traincontent + traincontent_suffix

        if content == '':
            return False
        else:
            return content

    # 获取是否有无余票----
    def getIsStandbyTicket(self,value=""):

        if value.isdigit():
            self.traincontents.append('<td style="color:#26a306;font-weight:400;">'+ value + '</td>')

        elif value == "有":
            self.traincontents.append('<td style="color: #26a306;font-weight: 400;">有</td>')

        else:
            self.traincontents.append('<td>无</td>')

    def getEmailContentTitle(self):

        emailTitle = '<tr><th colspan="30">12306余票监控</th></tr>'
        return emailTitle

    def getEmailContentListTitle(self):

        emaillistTitles = [
            '<tr>',
            '<td>序号</td>',
            '<td>列车</td>',
            '<td>出发地</td>',
            '<td>目的地</td>',
            '<td>发车时间</td>',
            '<td>到达时间</td>',
            '<td>历时时间</td>',
            '<td>商务座/特等座</td>',
            '<td>一等座</td>',
            '<td>二等座</td>',
            '<td>高级软卧</td>',
            '<td>软卧</td>',
            '<td>硬卧</td>',
            '<td>硬座</td>',
            '<td>无座</td>',
            '</tr>'
        ]
        return ''.join(emaillistTitles)

    def sentEmail(self,trains_list):

        # print("************************************email中的内容（start）****************************************************")
        emailTitle = self.getEmailContentTitle()
        # TODO 测试使用 print
        # print("emailTitle:")
        # print(emailTitle)

        emaillistTitle = self.getEmailContentListTitle()
        # TODO 测试使用 print
        # print("emaillistTitle:")
        # print(emaillistTitle)
        #
        emailListContent = self.outputResult(trains_list)   # 获取所有车次的票相关信息，返回html 表格
        # TODO 测试使用 print
        # print("emailListContent:")
        # print(emailListContent)
        # print("************************************email中的内容（end）****************************************************")

        if emailListContent ==  False:
            return False


        # 封装email中的内容，形成*****html格式
        emailContents = [
            '<table>',
            '<thead>',
            emailTitle,
            emaillistTitle,
            '</thead>',
            '<tbody>',
            emailListContent,
            '</tbody>',
            '</table>'
        ]
        emailContent = ''.join(emailContents)

        # 发送邮件
        grabTicket = GrabTicketSmtp("979959980@qq.com", emailContent)
        grabTicket.sendEmail()

        return True


    def callQueryTrain(self):
        """
        查询该天的所有车次信息，包括所有的车次（有票或者无票）
        :return: 返回列表数组，里面包含所有车次的信息，此信息经过切片处理，包含从网页上获取的所有信息，与网页对应
        """
        result = self.curlTrainInfo()
        # print(result[0])
        # print(result[1])
        # print(result[2])
        # print(result[3])
        # print(result[4])
        trains_list = self.handleResultDatas(result)
        return trains_list

    def myAlign(self, string, length=0):
        if length == 0:
            return string
        slen = len(string.encode("GBK"))
        re = string
        while slen < length:
            re += " "
            slen += 1
        return re