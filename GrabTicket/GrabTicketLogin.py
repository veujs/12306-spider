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
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'kyfw.12306.cn',
            # "Referer": "https://kyfw.12306.cn/otn/login/init",
            "User-Agent":
                        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
            # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        # 创建一个网络请求session实现登录验证
        self.session = GrabTicket.ss  # 实例化一个session对象



    # 跳转12306登录页面
    def loginInit(self):
        if GrabTicket.cookies_print_code == "1":
            print("loginInit_start>>>",self.session.cookies.get_dict())

        loginInitUrl = "https://kyfw.12306.cn/otn/login/init"
        response = self.session.get(url=loginInitUrl,headers=self.headers)

        print("loginInit_request_headers>>>", response.request.headers)
        print("loginInit_response_headers>>>",response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("loginInit_end>>>", self.session.cookies.get_dict())
            print("response.cookies>>>", response.cookies.get_dict())



    def getVerificationCode(self):
        verificationCodeUrl = "https://kyfw.12306.cn/passport/captcha/captcha-image?" \
                              "login_site=E&module=login&rand=sjrand&0.5744143427000492"
        # requests库的session会为我们保存cookie信息，只要我们继续使用session请求即可requests库的session会为我们保存cookie信息，只要我们继续使用session请求即可

        if GrabTicket.cookies_print_code == "1":
            print("getVerificationCode_start>>>",self.session.cookies.get_dict())
        response = self.session.get(url=verificationCodeUrl, headers=self.headers, verify=False)
        print("getVerificationCode_request_headers>>>", response.request.headers)
        print("getVerificationCode_response_headers>>>",response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("getVerificationCode_end>>>", self.session.cookies.get_dict())
            print("response.cookies>>>", response.cookies.get_dict())



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

        if GrabTicket.cookies_print_code == "1":
            print("checkVerifyCode_start>>>",self.session.cookies.get_dict())

        response = self.session.post(url=captChaUrl, data=form_Data,headers=self.headers, verify=False)
        print("checkVerifyCode_request_headers>>>", response.request.headers)
        print("checkVerifyCode_response_headers>>>",response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("checkVerifyCode_end>>>", self.session.cookies.get_dict())
            print("response.cookies>>>", response.cookies.get_dict())
            print("response.text>>>", loads(response.text))

        # print(response.text)   #  返回的位json数据

        response_dict = loads(response.text)
        print(response_dict)

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
        # print(form_Data)

        if GrabTicket.cookies_print_code == "1":
            print("login_start>>>",self.session.cookies.get_dict())
        response = self.session.post(url=loginUrl, data=form_Data, headers=self.headers, verify=False) # 必须使用post请求来发送带数据的
        print("login_request_headers>>>", response.request.headers)
        print("login_response_headers>>>", response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("login_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())
            print("response.text>>>",loads(response.text))

        response_dict = loads(response.text)
        # print(response_dict)
        if response_dict["result_message"] == "登录成功":
            # print("恭喜！登录成功")
            pass
        else:
            print("密码输入错误！")
        # self.uamtk_post()

        userLoginUrl = "https://kyfw.12306.cn/otn/login/userLogin"
        userLoginData = {
            "_json_att":""

        }
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/login/init"
        response = self.session.post(url=userLoginUrl,data=userLoginData,headers=self.headers)



        userLoginUUrl = "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin"
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/login/init"

        if GrabTicket.cookies_print_code == "1":
            print("userLogin_start>>>",self.session.cookies.get_dict())
        response = self.session.get(url=userLoginUUrl, headers=self.headers)
        print("userLogin_request_headers>>>", response.request.headers)
        print("userLogin_response_headers>>>", response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("userLogin_end>>>",self.session.cookies.get_dict())
            print("response.cookies>>>",response.cookies.get_dict())


        self.uamauthclient_post()

    # 很关键，不然后边预订会出现登录验证不成功
    def uamtk_post(self):
        uamtk_Url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        appid_Data = {"appid":"otn"}

        self.headers["Referer"] = "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin"

        if GrabTicket.cookies_print_code == "1":
            print("uamtk_start>>>>",self.session.cookies.get_dict())
        response = self.session.post(url=uamtk_Url, data=appid_Data,headers=self.headers, verify=False)
        print("uamtk_request_headers>>>", response.request.headers)
        print("uamtk_response_headers>>>", response.headers)
        if GrabTicket.cookies_print_code == "1":
            print("uamtk_end>>>>", self.session.cookies.get_dict())
            print("response.cookies>>>", response.cookies.get_dict())
            print("response.text>>>", loads(response.text))

        response_dict = loads(response.text)
        return response_dict["newapptk"]

    # 很关键，不然后边预订会出现登录验证不成功
    def uamauthclient_post(self):
        uamauthclientUrl = "https://kyfw.12306.cn/otn/uamauthclient"
        tk_Data = {"tk":""}  # 这个tk对应的值必须通过请求放入到COOKIES中切记
        tk_Data["tk"] = self.uamtk_post()

        self.headers["Referer"] = "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin"

        if GrabTicket.cookies_print_code == "1":
            print("uamauthclient_start>>>>", self.session.cookies.get_dict())
        response1 = self.session.post(url=uamauthclientUrl,data=tk_Data,headers=self.headers)
        print("uamauthclient_request_headers>>>", response1.request.headers)
        print("uamauthclient_response_headers>>>", response1.headers)
        if GrabTicket.cookies_print_code == "1":
            print("uamauthclient_end>>>>", self.session.cookies.get_dict())
            print("response1.cookies>>>", response1.cookies.get_dict())
            print("response.text>>>", loads(response1.text))

        durl = "https://kyfw.12306.cn/otn/login/userLogin"
        response2 = self.session.get(url=durl)

# if __name__ == "__main__":
#     # 实例化登录对象
#     Login = GrabTicketLogin()
#     # 获取校验码
#     captChaCode = Login.getVerificationCode()
#     while True:
#         if Login.checkVerifyCode(captChaCode):
#             print("校验通过！")
#             break
#         else:
#             print("校验失败！请重新输入校验码！")
#             captChaCode = Login.getVerificationCode()
#     Login.login()

    # Login.checkUser()