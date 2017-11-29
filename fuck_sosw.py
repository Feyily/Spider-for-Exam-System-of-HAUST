#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- BeautifulSoup(必须)
- cookielib||cookiejar (任选其一)
Info
- author : "ShuhaoMa"
- email  : "630924780@qq.com"
- date   : "2017.6.1"
Update
- name   : "SpaderForSosw"
- date   : "2017.6.2"
'''
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
from bs4 import BeautifulSoup
import bs4
import types
import SelectFile as sf

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "210.43.5.241",
    "Referer": "http://210.43.5.241/wlkcroot/html5root/function/empty.asp",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def isLogin(baseurl):
    # 通过查看用户个人信息来判断是否已经登录
    url = baseurl+"/grxx/index.asp"
    index_page = session.get(url, headers=headers)
    html = index_page.text
    pattern = r'name="user_id"'
    if len(re.findall(pattern, html)) == 0:
        return True
    else:
        return False


def login(secret, account,baseurl):
    headers["X-Requested-With"] = "XMLHttpRequest"
    post_url = baseurl+'/function/login_do.asp'
    postdata = {
            'r1': '2',
            'u1': secret,
            'u2': account
        }
    # 不需要验证码直接登录成功
    login_page = session.post(post_url, data=postdata, headers=headers)
    session.cookies.save()
    print(login_page.text)

def doTest(filename,baseurl):
    post_url = baseurl+'/kczy/zjzc1.asp'
    postdata = {
        'ctl1':'&#160;&#160;0&#160;&#160',
        'kctl1':'&#160;&#160;0&#160;&#160',
        'ctl2':'&#160;&#160;0&#160;&#160',
        'kctl2':'&#160;&#160;0&#160;&#160',
        'ctl3':'&#160;&#160;0&#160;&#160',
        'kctl3':'&#160;&#160;0&#160;&#160',
        'ctl4': '&#160;&#160;0&#160;&#160',
        'kctl4': '&#160;&#160;5&#160;&#160',
        'ctl5': '&#160;&#160;0&#160;&#160',
        'kctl5': '&#160;&#160;0&#160;&#160',
        'ctl6': '&#160;&#160;0&#160;&#160',
        'kctl6': '&#160;&#160;0&#160;&#160',
        'ctl7': '&#160;&#160;0&#160;&#160',
        'kctl7': '&#160;&#160;0&#160;&#160',
        'ctl8': '&#160;&#160;0&#160;&#160',
        'kctl8': '&#160;&#160;0&#160;&#160',
        'ctl9': '&#160;&#160;0&#160;&#160',
        'kctl9': '&#160;&#160;0&#160;&#160',
        'ctl10': '&#160;&#160;0&#160;&#160',
        'kctl10': '&#160;&#160;0&#160;&#160',
        'ctl11': '&#160;&#160;0&#160;&#160',
        'kctl11': '&#160;&#160;0&#160;&#160',
        'ctl12': '&#160;&#160;0&#160;&#160',
        'kctl12': '&#160;&#160;0&#160;&#160',
        'ctl13': '&#160;&#160;0&#160;&#160',
        'kctl13': '&#160;&#160;0&#160;&#160',
        'ctl14': '&#160;&#160;0&#160;&#160',
        'kctl14': '&#160;&#160;0&#160;&#160',
        'ctl15': '&#160;&#160;0&#160;&#160',
        'kctl15': '&#160;&#160;0&#160;&#160',
        'SYSJ': '5',
        'zjzc': '11',
        'ztl': '5',
        'zjzs': '15'
    }
    test_page=session.post(post_url, data=postdata, headers=headers)
    getAnswer(filename,baseurl)

def getAnswer(filename,baseurl):
    #get_url = 'http://210.43.5.241/wlkcroot/html5root/kczy/zjzc1.asp?zcstda0=000000000&zcstda1='   #此为选择的请求参数,需根据需求更换二者之一
    get_url = baseurl+'/kczy/zjzc1.asp?zcstda0=&zcstda1=~~~~~~~~~~'   #此为填空请求参数,需根据需求更换二者之一
    answer_page = session.get(get_url)
    answer_page.encoding = 'gb2312'
    parseTest(answer_page.text,filename)

def parseTest(text,filename):
    soup = BeautifulSoup(text, 'lxml')
    attrs = {
        'width': '860',
        'bgcolor': '#FFFFFF',
        'valign':'top'
    }
    newslist = soup.find_all(name='td', attrs=attrs)
    file = open(filename, "a", encoding="utf-8")
    result = ""
    i = 1
    for question in newslist:
        title = appendquest(question.contents,filename)
        if title != "":
            result += str(i) + "、"
            result += title
            #sibl = "\n" + question.parent.nextSibling.nextSibling.text + "\n\n"  # 选择题节点处理,需根据需求更换二者之一,此处有空白也算是兄弟节点！！！
            sibl = "\n" + question.parent.nextSibling.nextSibling.nextSibling.nextSibling.text + "\n\n"    #填空题节点处理,获取填空题节点,需根据需求更换二者之一
            result += sibl
            file.writelines(result + "\n")
            i = i + 1
        result = ""

def appendquest(cont,name):
    str=""
    for tag in cont:
        if type(tag) == bs4.element.Tag:
            str += "\n"
        else:
            if sf.selectfile(tag,name):
                break
            else:
                str += tag
    return str

if __name__ == '__main__':
    baseurl = input("请输入基地址：")
    if isLogin(baseurl):
        print('您已经登录')
    else:
        #account = input('请输入你的用户名\n>  ')
        #secret = input("请输入你的密码\n>  ")
        login('151451080320', '151451080320',baseurl)
        if isLogin(baseurl):
            times=int(input("你想刷几次？\n"))
            filename=input("你想保存的文件名（含扩展名）：")
            for i in range(times):
                doTest(filename,baseurl)
