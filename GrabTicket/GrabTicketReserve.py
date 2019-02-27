# @Time 			: 2018/09/14
# @Author			: 王志鹏
# @File 			: GrabTicketReservation.py
# @Software			: PyCharm
# @Python Version	: 3.7
# @About 			: 12306预定接口操作类


import requests
import urllib.request
from json import loads
# import GrabTicketLogin
import GrabTicket
import re
import urllib.parse
from PIL import Image

from requests.cookies import RequestsCookieJar


requests.packages.urllib3.disable_warnings()
class GrabTicketReservation(object):


    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'kyfw.12306.cn',
            "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
            "User-Agent":
                        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
            # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

        }
        # 创建一个网络请求session
        self.session = GrabTicket.ss  # 实例化一个session对象

        # self.session = requests.session()  # 实例化一个session对象
    def checkUser(self):
        """
        检查用户是否保持登陆成功
        :return:
        """

        # 首先进入车票预订界面
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        if GrabTicket.cookies_print_code == "1":
            print("GetJS_start>>>",self.session.cookies.get_dict())

        response1 = self.session.get(url="https://kyfw.12306.cn/otn/HttpZF/GetJS", headers=self.headers) # 必须使用post请求来发送带数据的

        if GrabTicket.cookies_print_code == "1":
            print("GetJS_end:",self.session.cookies.get_dict())
            print("response.cookies>>>",response1.cookies.get_dict())
            # print("response.text>>>", loads(response.text))




        checkUserUrl = "https://kyfw.12306.cn/otn/login/checkUser"
        checkUserData = {"_json_att": ""}

        if GrabTicket.cookies_print_code == "1":
            print("checkUser_start>>>",self.session.cookies.get_dict())


        response = self.session.post(url=checkUserUrl, data=checkUserData, headers=self.headers) # 必须使用post请求来发送带数据的


        print("checkUser_request_headers>>>", response.request.headers)
        print("checkUser_response_headers>>>",response.headers)

        if GrabTicket.cookies_print_code == "1":
            print("checkUser_end:",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>", loads(response.text))

        response_dict = loads(response.text)  # 转化为字典形式的数据

        if response_dict["data"]["flag"] == True:

            print("已经成功登陆！")
            return True

        elif response_dict["data"]["flag"] == False:
            print("请重新登陆！")
            return False

    def submitOrderRequest(self,standyTrains_list):
        """
        点击预订,判断用户是否可以访问预订请求页面
        """
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        submitOrderRequestUrl = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        submitData = {
            "back_train_date":"2018-10-12", # 页面中有默认，非必须
            "purpose_codes":"ADULT", # 页面中有默认，非必须
            "query_from_station_name":"西安北", # 页面中有默认，非必须
            "query_to_station_name":"洪洞西", # 页面中有默认，非必须
            "secretStr":"", # 必选
            "tour_flag":"dc",   # 必选 不知为何！！！！！
            "train_date":"2018-10-12", # 页面中有默认，非必须
            "undefined":""
        }


        self.session.cookies.set("_jc_save_fromDate","2018-10-12")
        self.session.cookies.set("_jc_save_fromStation","%u897F%u5B89%u5317%2CEAY")
        self.session.cookies.set("_jc_save_toDate", "2018-10-12")
        self.session.cookies.set("_jc_save_showIns", "true")
        self.session.cookies.set("_jc_save_toStation","%u6D2A%u6D1E%u897F%2CHTV")
        self.session.cookies.set("_jc_save_wfdc_flag","dc")
        self.session.cookies.set("current_captcha_type", "Z")

        num = int(input("请输入选择的车次编号（例：0）："))

        # 注意需要对standyTrains_list[num]["secretStr"]进行urldecode解码
        print(standyTrains_list[num]["secretStr"])
        # submitData["secretStr"] = standyTrains_list[num]["secretStr"]
        submitData["secretStr"] = urllib.parse.unquote(standyTrains_list[num]["secretStr"])
        # submitData["secretStr"] = urllib.request.unquote(standyTrains_list[num]["secretStr"]).replace("\n","")
        print(submitData["secretStr"])

        if GrabTicket.cookies_print_code == "1":
            print("submitOrderRequest_start>>>",self.session.cookies.get_dict())



        response = self.session.post(url=submitOrderRequestUrl,data=submitData,headers=self.headers)
        print("submitOrderRequest_request_headers>>>", response.request.headers)
        print("submitOrderRequest_response_headers>>>",response.headers)

        if GrabTicket.cookies_print_code == "1":
            print("submitOrderRequest_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>", loads(response.text))
        print(response)
        print(response.cookies.get_dict())

        response_dict = loads(response.text)
        print(response_dict)
        if response_dict["status"] == False:
            print("用户不允许访问预订页面！")
            return False
        else:
            initDcResponseData = self.confirmPassenger_initDc_Or_Wc(submitData["tour_flag"]) # 跳转至预订页面
            card_List = self.getPassengerDTOs(initDcResponseData)  # 获取联系人
            self.checkOrderInfo(card_List,initDcResponseData)
            self.getQueueCount(initDcResponseData)
            pass


    # 通过单程、往返类型，跳转至车票预订确认页面
    def confirmPassenger_initDc_Or_Wc(self, dc_or_wf):

        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"

        confirmPassenger_initDcUrl = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        confirmPassenger_initWcUrl = "https://kyfw.12306.cn/otn/confirmPassenger/initWc"

        confirmPassengerData = {"_json_att":""}
        if dc_or_wf == "dc":
            durl = confirmPassenger_initDcUrl
            print("dddccc")
        elif dc_or_wf == "wf":
            print("wwwfff")
            durl = confirmPassenger_initWcUrl


        if GrabTicket.cookies_print_code == "1":
            print("confirmPassenger_initDc_Or_Wc_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=durl, data=confirmPassengerData,headers=self.headers)
        print("confirmPassenger_initDc_request_headers>>>", response.request.headers)
        print("confirmPassenger_initDc_response_headers>>>",response.headers)

        if GrabTicket.cookies_print_code == "1":
            print("confirmPassenger_initDc_Or_Wc_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            # print("response.text>>>", loads(response.text))
        # print(type(response))
        with open("confirmPassenger_initDc_Or_Wc.html","wb") as hh:
        # ff = open("verifycode_img.html","wb") # 新建一个jpg文件
            hh.write(response.content)

        return response.text



    def getPassengerDTOs(self, initDcResponseData):
        """
        获取联系人
        """
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        ticketToken = re.search("var globalRepeatSubmitToken = '(.*?)';", initDcResponseData).group(1)
        print("REPEAT_SUBMIT_TOKEN",ticketToken)
        getPassengerDTOsUrl = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        getPassengerDTOsData = {"_json_att": "",
                                "REPEAT_SUBMIT_TOKEN":ticketToken
        }

        # getPassengerDTOsData["REPEAT_SUBMIT_TOKEN"] = ticketToken


        if GrabTicket.cookies_print_code == "1":
            print("getPassengerDTOs_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=getPassengerDTOsUrl,data=getPassengerDTOsData,headers=self.headers)

        print("getPassengerDTOs_request_headers>>>", response.request.headers)
        print("getPassengerDTOs_response_headers>>>",response.headers)

        if GrabTicket.cookies_print_code == "1":
            print("getPassengerDTOs_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>", loads(response.text))


        response_dict = loads(response.text)
        # print(response_dict)
        card_List = response_dict["data"]["normal_passengers"]
        if response_dict["data"]["isExist"] == True:
            print("购票人信息列表如下：")
            card_index = 1
            for i in card_List:
                print("【%d】: %s"%(card_index,i["passenger_name"]))
                card_index += 1

            print(card_List)
            return card_List
        else:
            print("获取订票人信息出错！可能存在未完成的订单，请检查")
            return False


    def getPassCodeNew_(self):

        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        getPassCodeNew_Url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?" \
                             "module=passenger&rand=randp&0.10907346687656738"

        if GrabTicket.cookies_print_code == "1":
            print("getPassCodeNew__start>>>",self.session.cookies.get_dict())

        response = self.session.get(url=getPassCodeNew_Url,headers=self.headers)

        if GrabTicket.cookies_print_code == "1":
            print("getPassCodeNew__end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            # print("response.text>>>", loads(response.text))

        with open("getPassCode.jpg","wb") as gg:
            gg.write(response.content)
        # try:
            # imgg = Image.open("verifycode_img.jpg")

            # Image.Image.show(imgg)
            # Image.Image.close(imgg)

        # except Exception as e:
        #     print(e)


    def checkOrderInfo(self, card_List, initDcResponseData):
        """
        检查选票人的信息
        """
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        # self.getPassCodeNew_()
        # oldPassengerStr：name, 身份类型(身份证\军官证....), 身份证,乘客类型（1成人2孩子3学生4伤残军人）
        oldPassengerStr = "王志鹏,1,142625199110210433,1_"
        # 座位类型:M(一等座)，O（二等座），3（硬卧），1（硬座），4（软卧），9（商务座）
        # passengerTicketStr：座位类型(), 0, 票类型(成人\儿童), name, 身份类型(身份证\军官证....), 身份证, 电话号码, 保存状态
        passengerTicketStr = "O,0,1,王志鹏,1,142625199110210433,18710834869,N"

        # card_num = int(input("请选择所需购票人序号:"))
        # oldPassengerList = oldPassengerStr.split(",")
        # oldPassengerList[0] = card_List[card_num - 1]["passenger_name"]
        # oldPassengerList[1] = card_List[card_num - 1]["passenger_id_type_code"]
        # oldPassengerList[2] = card_List[card_num - 1]["passenger_id_no"]
        # oldPassengerList[3] = card_List[card_num - 1]["passenger_type"]
        # oldPassengerStr = ",".join(oldPassengerList)
        # oldPassengerStr +="_"
        print(oldPassengerStr)

        # passengerTicketList = passengerTicketStr.split(",")
        # passengerTicketList[0] = "O"
        # passengerTicketList[1] = "0"
        # passengerTicketList[2] = "1"
        # passengerTicketList[3] = card_List[card_num - 1]["passenger_name"]
        # passengerTicketList[4] = card_List[card_num - 1]["passenger_id_type_code"]
        # passengerTicketList[5] = card_List[card_num - 1]["passenger_id_no"]
        # passengerTicketList[6] = card_List[card_num - 1]["mobile_no"]
        # passengerTicketList[7] = "N"
        # passengerTicketStr = ",".join(passengerTicketList)
        print(passengerTicketStr)
        ticketToken = re.search("var globalRepeatSubmitToken = '(.*?)';", initDcResponseData).group(1)
        print("REPEAT_SUBMIT_TOKEN", ticketToken)
        checkOrderInfoUrl = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        checkOrderInfoData = {
            "_json_att":"",
            "bed_level_order_num":"000000000000000000000000000000",
            "cancel_flag":"2",
            "oldPassengerStr":oldPassengerStr,
            "passengerTicketStr":passengerTicketStr,
            "randCode":"",
            "REPEAT_SUBMIT_TOKEN":ticketToken,
            "tourflag":"dc",
            "whatsSelect":"1"
        }
        # self.session.cookies.set("_jc_save_fromDate","2018-09-29")
        #         # self.session.cookies.set("_jc_save_fromStation","%u897F%u5B89%u5317%2CEAY")
        #         # self.session.cookies.set("_jc_save_toDate", "2018-09-21")
        #         # self.session.cookies.set("_jc_save_showIns", "true")
        #         # self.session.cookies.set("_jc_save_toStation","%u6D2A%u6D1E%u897F%2CHTV")
        #         # self.session.cookies.set("_jc_save_wfdc_flag","dc")
        #         # self.session.cookies.set("current_captcha_type", "Z")
        if GrabTicket.cookies_print_code == "1":
            print("checkOrderInfo_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=checkOrderInfoUrl,data=checkOrderInfoData,headers=self.headers)

        if GrabTicket.cookies_print_code == "1":
            print("checkOrderInfo_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>", loads(response.text))


        response_dict = loads(response.text)
        print(response_dict)

        if response_dict["data"]["submitStatus"] == True:

            return True
        else:
            print(response_dict["data"]["errMsg"])
            # self.checkOrderInfo(self, card_List, ticketToken)
            return False



    def getQueueCount(self, initDcResponseData):
        """
        提交订单
        """
        ticketToken = re.search("var globalRepeatSubmitToken = '(.*?)';", initDcResponseData).group(1)
        fromStationTelecode = re.search("'from_station_telecode':'(.*?)'", initDcResponseData).group(1)
        leftTicket = re.search("'ypInfoDetail':'(.*?)'", initDcResponseData).group(1)
        purpose_codes = re.search("'purpose_codes':'(.*?)'", initDcResponseData).group(1)
        station_train_code = re.search("'station_train_code':'(.*?)'", initDcResponseData).group(1)
        to_station_telecode = re.search("'to_station_telecode':'(.*?)'", initDcResponseData).group(1)
        train_no = re.search("'train_no':'(.*?)'", initDcResponseData).group(1)
        train_date = re.search("'train_date':'(.*?)'", initDcResponseData).group(1)
        train_location = re.search("'train_location':'(.*?)'", initDcResponseData).group(1)
        # train_no = re.search("'train_no':'(.*?)'", initDcResponseData).group(1)

        print("正则查找得到：globalRepeatSubmitToken",ticketToken)
        print("正则查找得到：from_station_telecode", fromStationTelecode)
        print("正则查找得到：ypInfoDetail", leftTicket)
        print("正则查找得到：purpose_codes", purpose_codes)
        print("正则查找得到：station_train_code", station_train_code)
        print("正则查找得到：to_station_telecode", to_station_telecode)
        print("正则查找得到：train_no", train_no)
        print("正则查找得到：train_date", train_date)
        print("正则查找得到：train_location", train_location)

        getQueueCountUrl = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        getQueueCountData = {
            "_json_att":"",
            "fromStationTelecode":fromStationTelecode,    # 出站编号
            "leftTicket":leftTicket,    #
            "purpose_codes":purpose_codes, #默认取ADULT ,表成人
            "REPEAT_SUBMIT_TOKEN":ticketToken,
            "seatType":"O",  # 座位类型
            "stationTrainCode":station_train_code,  #
            "toStationTelecode":to_station_telecode, # 到站编号
            "train_date":train_date,    # 列车日期
            "train_location":"",
            "trian_no":train_no   # 列车编号，例如：# 27000D256702
        }

        if GrabTicket.cookies_print_code == "1":
            print("getQueueCount_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=getQueueCountUrl,data=getQueueCountData,headers=self.headers)

        if GrabTicket.cookies_print_code == "1":
            print("getQueueCount_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>", loads(response.text))

        response_dict = loads(response.text)

        if response_dict["status"] == True:
            return True
        else:
            return False



    def confirmSingleForQueue(self):
        """
        确认订单
        """
        confirmSingleForQueueUrl = ""
        pass


    def queryOrderWaitTime(self):
        """
        排队等待
        """
        queryOrderWaitTimeUrl = ""

        pass


    def resultOrderForDcQueue(self):
        """
        订单结果
        """
        resultOrderForDcQueueUrl = ""
        pass



# ticketReserve = GrabTicketReservation()
# ticketReserve.submitOrderRequest()