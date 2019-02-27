# @Time 			: 2018/09/18
# @Author			: 王志鹏
# @File 			: GrabTicketLogin.py
# @Software			: PyCharm
# @Python Version	: 3.7
# @About 			: 程序入口 执行
import ssl
import city
import time
import re
import datetime
import GrabTicketOperation
from GrabTicketSmtp import GrabTicketSmtp
from GrabTicketLogin import GrabTicketLogin
from GrabTicketReserve import GrabTicketReservation
import requests

ss = requests.session()

cookies_print_code = "1" # 1:表示开启打印cookies功能  0：表示不使能

def city_station(sttype=1):

    Tips_text = ""

    #填充提示文字
    if sttype == 1:
        Tips_text = "出发地"
    elif sttype ==2:
        Tips_text = "目的地"

    while True:

        station_name = str(input("请输入%s："% Tips_text))
        station_names = city.get_city_code(station_name)
        if station_names == False:
            print("无法匹配到站点，请重新输入！")
        else:
            break
    return station_names

def checkTimeFormat(setOutTime):
    date_text = re.search("(\d{4}-\d{2}-\d{2})",setOutTime)
    try:
        if date_text == None:
            return False
        else:
            date_text = date_text.group(0)

        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            return False
        else:
            return True
    except ValueError:
        return False


def time_station():

    while True:
        setOutTime = input("请输入出发时间 （例：2018-04-04）:")
        print(type(setOutTime))
        if checkTimeFormat(setOutTime) == True:
            timeArray = time.strptime(setOutTime, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray))

            nowTime = time.time()

            nowTimeStamp = int(nowTime - nowTime % 86400 - 28800)
            if timeStamp < nowTimeStamp:
                print("出发时间不能小于当前时间")
            else:
                break
    return setOutTime


def danChengOrWangfan():
    while True:
        jc_save_wfdc_flag = input("选择单程往返（dc）or往返（wf）:")
        if jc_save_wfdc_flag == "dc" or "wf":
            ss.cookies.set("_jc_save_wfdc_flag",jc_save_wfdc_flag)
            break
        else:
            print("输入有误！请重新输入")

    return jc_save_wfdc_flag


if __name__ == "__main__":

    # # 定义一个参数字典
    input_param_dict = {}
    # # 实例化登录对象
    # print("****************【1】登录操作************************************************************************************")
    # Login = GrabTicketLogin()
    # Login.loginInit()
    # # 获取校验码
    # captChaCode = Login.getVerificationCode()
    # while True:
    #     if Login.checkVerifyCode(captChaCode):
    #         # print("校验通过！")
    #         break
    #     else:
    #         print("校验失败！请重新输入校验码！")
    #         captChaCode = Login.getVerificationCode()
    # Login.login()
    # print("****************【1】登录操作************************************************************************************")

    print("****************【2】查询操作************************************************************************************")
    input_param_dict["from_station"] = "EAY"
    input_param_dict["to_station"] = "HTV"
    input_param_dict["setOutTime"] = "2018-10-30"
    input_param_dict["dc_or_wf"] = "dc"
    # input_param_dict["from_station"] = city_station(1)
    # input_param_dict["to_station"] = city_station(1)
    # input_param_dict["setOutTime"] = time_station()
    # input_param_dict["dc_or_wf"] = danChengOrWangfan()
    print("正在爬取数据.....请稍等！")
    grabTicket = GrabTicketOperation.GrabTicketOperation(input_param_dict)
    trains_list = grabTicket.callQueryTrain()
    # print(trains_list)  # trains_list中包含着secretstr信息
    # standbyTrains_list = grabTicket.getStandbyTicketTrainsList(trains_list) # 处理trains_list的信息，在控制台输出“有余票的所有车次的信息”
    # grabTicket.sentEmail(trains_list) # 处理trains_list的信息，以html语言的形式，发送“有余票的所有车次的信息”邮件到指定的邮箱
    print("****************【2】查询操作************************************************************************************")

    # print("****************【3】预订操作************************************************************************************")
    # yuding = GrabTicketReservation()    # 实例化预订对象
    # yuding.checkUser()  # 检测登录条件
    # yuding.submitOrderRequest(standbyTrains_list)
    # print("****************【3】预订操作************************************************************************************")
    #













