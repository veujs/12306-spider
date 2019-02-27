# 测试urllib.request.urlopen进行网页请求
# import urllib.request
# response = urllib.request.urlopen("https://www.python.org")
# result = response.read()
# print("response的类型为--------------------%s"%(type(response)))
# print("result的类型为----------------------%s"%(type(result)))
# print("result为----------------------------%s"%result)
# print("result解码后为----------------------%s"%result.decode('utf-8'))
# print("response.status为-------------------%s"%response.status)
# print("response.getheaders()为-------------%s"%response.getheaders())
# print(response.read().decode('utf-8'))
# print(response.status())


# #测试urllib.request库中有关类关于   Cookies的相关操作
# import urllib.request
# import http.cookiejar

# cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
#
# print(type(cookie))
# print(cookie)
# for item in cookie:
#     print(item.name+"="+item.value)
# result = response.read()
# print("response的类型为--------------------%s"%(type(response)))
# print("result的类型为----------------------%s"%(type(result)))
# print("result为----------------------------%s"%result)
# print("result解码后为----------------------%s"%result.decode('utf-8'))

# filename = 'cookies.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
#
# response = opener.open('http://www.baidu.com')
# cookie.save(filename,ignore_discard=True,ignore_expires=True)
# print(type(cookie))
# print(cookie)
# for item in cookie:
#     print(item.name+"="+item.value)



import requests



r = requests.get('https://github.com/favicon.ico')
print(r.text)
print(r.content)
print(type(r))
# print(r.content.decode('utf-8'))

