# -*- coding: UTF-8 -*-
# @Time             : 2018/09/14 14:58
# @Author           : 王志鹏
# @File             : GrabTicketSmtp.py
# @Software         : PyCharm
# @Python Version   : 3.7
# @About            : 邮件类

import smtplib # 该模块负责发送邮件
from email.header import Header # 该模块负责构造邮件
from email.mime.text import MIMEText  #导入MIMEText库用来做纯文本的邮件模板


class GrabTicketSmtp(object):

    mail_host = "smtp.qq.com"  # QQ发件服务器
    mail_user = "624040034@qq.com"
    mail_pass = "etwpyzgnsclbbeji"  # 此密码为在邮箱设置开启smtp、pop3的时候反馈回来的户端授权密码"

    sender = "624040034@qq.com"
    title = "好消息！列车有余票啊！！"

    # 构造函数
    def __init__(self,receivers,content):

        # 邮件的内容
        self.content = content
        # 收件人
        self.receivers = [receivers]


    def getTitle(self):

        return self.title

    def sendEmail(self):
        # print('服务器为：\t\t%s' % self.mail_host)
        # print('登录名为：\t\t%s' % self.mail_user)
        # print('授权码：\t\t%s' % self.mail_pass)
        # print('发件人为：\t\t%s' % self.sender)
        # print('收件人为：\t\t%s' % self.receivers)

        message = MIMEText(self.content,"html","utf-8")
        message["from"] = "{}".format(self.sender)
        message["to"] = ",".join(self.receivers)
        message["subject"] = self.getTitle()

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            # smtpObj.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
            smtpObj.login(self.mail_user,self.mail_pass)
            smtpObj.sendmail(self.mail_user,self.receivers,message.as_string())
            print("邮件发送成功！")

        except smtplib.SMTPException as e:
            print(e)


# if __name__ == '__main__':
#     sendEmail()
#     pass
