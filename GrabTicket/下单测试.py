# @Time 			: 2018/09/18
# @Author			: 王志鹏
# @File 			: GrabTicketLogin.py
# @Software			: PyCharm
# @Python Version	: 3.7
# @About 			: 12306抢票账户登录类
# 参考资料：https://blog.csdn.net/sinat_36772813/article/details/76804799
import requests
from PIL import Image
from json import loads


# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()

# ss = requests.session()
#
# cook = {
#     "_jc_save_fromDate": "2018-09-28",
#     "_jc_save_fromStation": "北京,BJP",
#     "_jc_save_toDate": "2018-09-20",
#     "_jc_save_toStation": "西安,XAY",
#     "_jc_save_wfdc_flag": "dc",
#     "BIGipServerotn": "351273482.38945.0000",
#     "BIGipServerpool_passport": "334299658.50215.0000",
#     "current_captcha_type": "Z",
#     "JSESSIONID": "2ACCBC669B21F29DC43BE3060F2EFF4E",
#     "RAIL_DEVICEID": "mxMSJSgNV7Bjg0TFx4Dw_SHXo3Opo0X0r74E2eG7vkihQA7qbuFnQrdDa_3g2DNpuHurPADVb88QJLKV2hnhfAUWtrmUQs6WgY_gM_rTrfVL4_m148XMl6pBXReBHPA2CIlrPgk3"
#                      "\MlCskyO9W1khuuSFeqovlPBi",
#     "RAIL_EXPIRATION": "1537605526560",
#     "route": "c5c62a339e7744272a54643b3be5bf64",
#     "tk": "18h1kW5AeV9Pvywmq7ak3rNRu6La09saQrqpBbVtWYL3A82G92w2w0"
# }
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"}
# # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3"
# #                         "6 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}




# @Time 			: 2018/09/18
# @Author			: 王志鹏
# @File 			: GrabTicketLogin.py
# @Software			: PyCharm
# @Python Version	: 3.7
# @About 			: 12306抢票账户登录类
# 参考资料：https://blog.csdn.net/sinat_36772813/article/details/76804799
import requests
from PIL import Image
from json import loads
import GrabTicket
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()

# session = requests.session()
class GrabTicketLogin(object):

    def __init__(self):
        self.headers = {
            # "Accept":"	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            # "Accept-Encoding":"gzip, deflate, br",
            # "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            # "Connection":"keep-alive",
            # "Host":"kyfw.12306.cn",
            # "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"


        }
        # self.headers = {"User-Agent":
        #                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        # 创建一个网络请求session实现登录验证
        self.session = requests.session()  # 实例化一个session对象


    def getVerificationCode(self):
        verificationCodeUrl = "https://kyfw.12306.cn/passport/captcha/captcha-image?" \
                              "login_site=E&module=login&rand=sjrand&0.5744143427000492"
        # requests库的session会为我们保存cookie信息，只要我们继续使用session请求即可requests库的session会为我们保存cookie信息，只要我们继续使用session请求即可
        print("getVerificationCode---start:")
        print(self.session.cookies.get_dict())
        response = self.session.get(url=verificationCodeUrl, headers=self.headers, verify=False)
        print("getVerificationCode---end:")
        print(self.session.cookies.get_dict())
        print("response.cookies:")
        print(response.cookies.get_dict())
        # print(verificationCodeUrl)
        # print(response.text.encode()) # 注意response.text和response.content的区别，都是返回内容不过表现形式不一样
        # print(response.content)
        with open("verifycode_img.jpg","wb") as ff:
        # ff = open("verifycode_img.jpg","wb") # 新建一个jpg文件
            ff.write(response.content)  # 验证码图片数据写入到verifycode_img.jpg文件中
        try:
            im = Image.open("verifycode_img.jpg")

            Image.Image.show(im)
            Image.Image.close(im)

        except Exception as e:
            print(e)
            print("请输入验证码：")

        captChaCode = input("请输入验证码序号/位置（例如：2,4）:")
        return captChaCode

    def checkVerifyCode(self, captChaCode=""):
        # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
        yanSol = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']

        # 请求接口
        captChaUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        form_Data = {
            "answer": "",
            "login_site": "E",
            "rand": "sjrand"
        }

        yanList = []
        for i in captChaCode.split(","):
            # print(i)
            yanList.append(yanSol[int(i)])

        yanStr = ",".join(yanList)
        form_Data["answer"] = yanStr
        # print(form_Data)


        print("checkVerifyCode---start:")
        print(self.session.cookies.get_dict())
        response = self.session.post(url=captChaUrl, data=form_Data,headers=self.headers, verify=False)
        # print(response.text)   #  返回的位json数据
        print("checkVerifyCode---end:")
        print(self.session.cookies.get_dict())
        print("response.cookies:")
        print(response.cookies.get_dict())
        response_dict = loads(response.text)


        # print(response_dict)

        if response_dict["result_code"] == "4":

            # print("验证码校验成功！")
            return True
        elif response_dict["result_code"] == "5":
            # print("校验失败！")
            return False
        else:
            # print("校验失败！")
            return False

    def login(self):

        # 请求接口
        loginUrl = "https://kyfw.12306.cn/passport/web/login"
        form_Data = {
            "username": "",
            "password": "",
            "appid": "otn"
        }
        form_Data["username"] = input("用户名：")
        form_Data["password"] = input("密码  ：")
        print(form_Data)


        print("login---start:")
        print(self.session.cookies.get_dict())
        response = self.session.post(url=loginUrl, data=form_Data, headers=self.headers, verify=False) # 必须使用post请求来发送带数据的
        print("login---end:")
        print(self.session.cookies.get_dict())
        print("response.cookies:")
        print(response.cookies.get_dict())



        response_dict = loads(response.text)
        print(response_dict)
        if response_dict["result_message"] == "登录成功":
            print("恭喜！登录成功")
        else:
            print("密码输入错误！")


    def checkUser(self):
        checkUserUrl = "https://kyfw.12306.cn/otn/login/checkUser"
        checkUserData = {"_json_att": ""}
        # requests.utils.add_dict_to_cookiejar(ss.cookies, cook)
        # response = self.session.post(url=checkUserUrl, data=checkUserData, headers=self.headers, verify=False)
        # cookies_temp = {"123":"456"}

        # # self.session.cookies.set("_jc_save_fromDate","2018-09-28")
        # # self.session.cookies.set("_jc_save_fromStation","%u5317%u4EAC%2CBJP")
        # # self.session.cookies.set("_jc_save_toDate", "2018-09-21")
        # # self.session.cookies.set("_jc_save_toStation","%u897F%u5B89%2CXAY")
        # # self.session.cookies.set("_jc_save_wfdc_flag","dc")
        # self.session.cookies.set("BIGipServerotn", "837812746.64545.0000")#很重要
        # # self.session.cookies.set("BIGipServerpool_passport", "283968010.50215.0000")
        # # self.session.cookies.set("current_captcha_type","Z")
        # self.session.cookies.set("JSESSIONID", "2B957AB33111081B6470A131FB84C541")#很重要
        # # self.session.cookies.set("RAIL_DEVICEID", "mxMSJSgNV7Bjg0TFx4Dw_SHXo3Opo0X0r74E2eG7vkihQA7qbuFnQrdDa_3g2DNpuHurPADVb88QJLKV2hnhfAUWtrmUQs6WgY_gM_rTrfVL4_m148XMl6pBXReBHPA2CIlrPgk3MlCskyO9W1khuuSFeqovlPBi")
        # # self.session.cookies.set("RAIL_EXPIRATION", "1537605526560")
        # self.session.cookies.set("route", "9036359bb8a8a461c164a04f8f50b252")#很重要
        # self.session.cookies.set("tk", "nOHU7iNhYCG6BY3KxmfafHsLXbOhPYNXZexz_AliJvPhpDEKtyw2w0")#很重要

        print("shezhihou>>>>>>>>>>>>>")
        print(self.session.cookies.get_dict())
        self.headers.get(self.session)
        print(self.headers)
        response = self.session.post(url=checkUserUrl, data=checkUserData, headers=self.headers)
        # print(requests.Request.headers)
        print(self.session.cookies)
        print(self.session.cookies.get("BIGipServerotn"))
        print(self.session.cookies.get_dict())

        print(response.cookies.get_dict())
        # response = Login.session.post(url=checkUserUrl)
        response_dict = loads(response.text) # 转化为字典形式的数据
        print(response_dict)
        print(response_dict["data"]["flag"])
        if response_dict["data"]["flag"] == True:

            print("已经成功登陆！")
            # return True
        elif response_dict["data"]["flag"] == False:
            print("请重新登陆！")
                # return False

    def checkOrderInfo(self):
        """
        检查选票人的信息
        """
        # self.getPassCodeNew_()
        # oldPassengerStr：name, 身份类型(身份证\军官证....), 身份证,乘客类型（1成人2孩子3学生4伤残军人）
        oldPassengerStr = "王志鹏,1,142625199110210433,1_"
        # 座位类型:M(一等座)，O（二等座），3（硬卧），1（硬座），4（软卧），9（商务座）
        # passengerTicketStr：座位类型(), 0, 票类型(成人\儿童), name, 身份类型(身份证\军官证....), 身份证, 电话号码, 保存状态
        passengerTicketStr = "O,0,1,王志鹏,1,142625199110210433,18710834869,N"
        print(oldPassengerStr)
        print(passengerTicketStr)
        # print("REPEAT_SUBMIT_TOKEN", ticketToken)
        checkOrderInfoUrl = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        checkOrderInfoData = {
            "_json_att":"",
            "bed_level_order_num":"000000000000000000000000000000",
            "cancel_flag":"2",
            "oldPassengerStr":oldPassengerStr,
            "passengerTicketStr":passengerTicketStr,
            "randCode":"",
            "REPEAT_SUBMIT_TOKEN":"c73d6da3149754f7266b0408f065cecf",
            "tourflag":"dc",
            "whatsSelect":"1"
        }

        self.session.cookies.set("_jc_save_fromDate","2018-09-29")
        self.session.cookies.set("_jc_save_fromStation","%u6D2A%u6D1E%u897F%2CHTV")
        self.session.cookies.set("_jc_save_toDate", "2018-09-21")
        self.session.cookies.set("_jc_save_toStation","%u897F%u5B89%u5317%2CEAY")
        self.session.cookies.set("_jc_save_wfdc_flag","dc")
        self.session.cookies.set("BIGipServerotn", "737149450.24610.0000")#很重要
        self.session.cookies.set("BIGipServerpool_passport", "367854090.50215.0000")
        self.session.cookies.set("current_captcha_type","Z")
        self.session.cookies.set("JSESSIONID", "EC940DAAD1BCFC48C26635556A66F736")#很重要
        self.session.cookies.set("RAIL_DEVICEID", "VLbl9zPKArF4ljn709p_19M4jfqhf6Du1kuGEm7fx1j1vv7Rh6Achh1jM0Kd-v_f0B8ZEk7qfX_MML3N3hwspQ_np6CM9Nw5nJFusaJAYc6EyO7OlO8LuyqzFDFHdm04_6SijMmfGl3QWB5ekP-cKue_SwikuEqo")
        self.session.cookies.set("RAIL_EXPIRATION", "1538264515981")
        self.session.cookies.set("route", "6f50b51faa11b987e576cdb301e545c4")#很重要
        self.session.cookies.set("tk", "qFwBwdrZlz7DfGYq_wG4XtLs7e8ATyFDakpNbTX0VJ5IpxbJ45w2w0")#很重要
        # self.session.cookies.set("_jc_save_fromDate","2018-09-29")
        # self.session.cookies.set("_jc_save_fromStation","%u897F%u5B89%u5317%2CEAY")
        # self.session.cookies.set("_jc_save_toDate", "2018-09-21")
        # self.session.cookies.set("_jc_save_toStation","%u6D2A%u6D1E%u897F%2CHTV")
        # self.session.cookies.set("_jc_save_wfdc_flag","dc")
        # self.session.cookies.set("current_captcha_type", "Z")
        print("checkOrderInfo_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=checkOrderInfoUrl,data=checkOrderInfoData,headers=self.headers)

        print("checkOrderInfo_end>>>",self.session.cookies.get_dict())
        print("response.cookies>>>",response.cookies.get_dict())
            # print("response.text>>>", loads(response.text))


        response_dict = loads(response.text)
        # print(response_dict)

        if response_dict["data"]["submitStatus"] == True:

            return True
        else:
            print(response_dict["data"]["errMsg"])
            # self.checkOrderInfo(self, card_List, ticketToken)
            return False






if __name__ == "__main__":
    # 实例化登录对象
    Login = GrabTicketLogin()
    # # 获取校验码
    # captChaCode = Login.getVerificationCode()
    # while True:
    #     if Login.checkVerifyCode(captChaCode):
    #         print("校验通过！")
    #         break
    #     else:
    #         print("校验失败！请重新输入校验码！")
    #         captChaCode = Login.getVerificationCode()
    # Login.login()

    # Login.checkUser()
    Login.checkOrderInfo()














































