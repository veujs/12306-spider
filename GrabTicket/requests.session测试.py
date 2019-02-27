import requests



def setCookies():
    """
    session对象能够帮我们跨请求保持某些参数，也会在同一个session实例发出的所有请求之间保持cookies。
    设置cookies
    """
    s = requests.session() # 实例化
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789') #设置cookies
    r = s.get('http://httpbin.org/cookies') # 读取cookies
    print(r.text)

def setSessionAttribute():
    """
    提供请求方法的缺省数据，通过设置session对象的属性来实现
    """
    s = requests.session()
    # 设置session对象的auth(授权)属性，用来作为请求的默认参数
    s.auth = ('user', 'pass')

    # 设置session的headers属性，通过update方法，将其余请求方法中的headers属性合并起来作为最终的请求方法的headers
    s.headers.update({'x-text':'true'})
    s.headers.update({'x-text1': 'true'})
    s.headers.update({'x-text': ''})

    # 发送请求，这里没有设置auth会默认使用session对象的auth属性，这里的headers属性会与session对象的headers属性合并
    r = s.get('http://httpbin.org/headers',headers={'x-text2':'true'})
    print(r.text)

def test():
    """
    函数参数中的数据只会使用一次，并不会保存到session中
    """
    durl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=log'\
              'in&rand=sjrand&0.5744143427000492'
    headers = {"User-Agent":
                        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    # 创建一个网络请求session实现登录验证
    s = requests.Session()
    # s.auth = ('user', 'pass')
    # s.headers.update({'x-text': 'true'})
    # s.headers.update({'x-text1': 'true'})

    r = s.get(url=durl,headers=headers, verify=False)
    print(r)
    # r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    # print(r.text)
    # r = s.get('http://httpbin.org/headers')
    # print('第二次访问结果')
    # print(r.text)

# setSessionAttribute()
test()
