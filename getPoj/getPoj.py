#!/usr/bin/python
# coding=utf-8
import requests
import re
import HTMLParser


cookies  = dict(cookies_are='working')
html_parser = HTMLParser.HTMLParser()
vis = {}

def login(id,password):
    data = {
        'user_id1':id,
        'password1':password,
        'B1':'login',
        'url':'/'
    }
    s = requests.session()
    url = "http://poj.org/login"
    r = s.post(url,data=data,cookies=cookies)
    #print r.text
    if id in r.text:
        return [s,True]
    else :
        return [s,False]

def getCode(s,runId):
    url = 'http://poj.org/showsource?solution_id=' + runId
    r = s.get(url,cookies=cookies)
    r.encoding = 'utf8'
    txt = r.text
    pattern = re.compile('<pre class="sh_cpp" style="font-family:Courier New,Courier,monospace">(.+?)</pre>',re.S)
    ans = pattern.findall(txt)[0]
    return html_parser.unescape(ans)


def run(id,password,path):
    url = 'http://poj.org/status?problem_id=&user_id='+str(id)+'&result=0&language='
    islogin = False
    while not islogin:
        try:
            [s,islogin] = login(id,password)
        except Exception:
            continue
        if not islogin:
            return False
    nxtUrl = ""
    while nxtUrl != url:
        if nxtUrl == "":
            nxtUrl = url
        r = s.get(nxtUrl,cookies=cookies)
        txt = r.text
        pattern = re.compile('a href=problem\\?id=(.+?)>(.+?)</a></td><td><font color=blue>Accepted</font></td><td>(.+?)</td><td>(.+?)</td><td><a href=showsource\\?solution_id=(.+?) target=_blank',re.S)
        ans = pattern.findall(txt)
        for lines in ans:
            tihao = lines[0]
            if vis.has_key(tihao):
                continue
            else:
                vis[tihao] = True
            runId = lines[-1]
            code = getCode(s,runId).encode('utf8')
            code = code.replace('\r\n','\n')
            filepath = path + '/poj/%s.cpp' %(tihao)
            print '正在保存poj'+str(tihao)+'的代码到'+str(filepath)
            f = open(filepath,'w')
            print >>f,code
        url = nxtUrl
        pattern = re.compile('Previous Page</font></a>\\]&nbsp;&nbsp;\\[<a href=(.+?)><font color=blue>Next Page</font>',re.S)
        suf = pattern.findall(txt)
        if suf == []:
            break
        suf = suf[0]
        nxtUrl = 'http://poj.org/'+str(suf)
    return True



qt = False
while not qt: 
    id = raw_input('请输入你的id:')
    password = getpass.getpass('请输入你的密码:')
    path = raw_input('请输入你想要保存的目录:')
    qt = run(id,password,path)
