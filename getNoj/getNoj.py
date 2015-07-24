#!/usr/bin/python
# coding=utf-8
import requests
import re
import HTMLParser
import getpass



html_parser = HTMLParser.HTMLParser()
cookies = dict(cookies_are='working')

def login(id,password):
    data = {
        'userName':id,
        'password':password
    }
    url = 'http://acm.njupt.edu.cn/acmhome/login.do'
    s = requests.session()
    r = s.post(url,data=data,cookies=cookies)
    r = s.get('http://acm.njupt.edu.cn/acmhome/problemList.do?method=show',cookies=cookies)
    if id in r.text:
        return [s,True]
    else:
        return [s,False]


def getCode(s,runId):
    url = 'http://acm.njupt.edu.cn/acmhome/solutionCode.do?id=' + runId
    r = s.get(url,cookies=cookies)
    #print r.encoding
    txt = r.text
    pattern = re.compile('<font size="3" face="Times New Roman">(.+?)</font>',re.S)
    code = pattern.findall(txt)[1]
    return html_parser.unescape(code.decode('gb2312'))
    



def run(id,password,path):
    while True:
        try:
            [s,t] = login(id,password)
        except Exception:
            #print '1'
            continue
        if t == False:
            return False
        break
    pagenum = 1;
    #print 1
    url = 'http://acm.njupt.edu.cn/acmhome/showstatus.do?problemId=&contestId=null&userName='+str(id)+'&result=1&language=&page='
    while True:
        turl = url + str(pagenum)
        print turl
        r = s.get(turl,cookies=cookies)
        txt = r.text
        #print txt
        st=r'a href="/acmhome/problemdetail\.do\?&method=showdetail&amp;id=(.+?)">(.+?)</a></DIV></td>\r\n<td><div align="center"><input id="problemID" type="hidden" value="(.+?)"/>'
        #print st
        pattern = re.compile(st,re.S)
        ans = pattern.findall(txt)
        if ans == []:
            break
        for line in ans:
            tihao = line[0]
            runId = line[-1]
            code = getCode(s,runId)
            code = code.encode('utf8')
            code = code.replace('<BR>','')
            filepath = path + '/noj/%s.cpp' %(tihao)
            print '正在保存noj'+str(tihao)+'的代码到'+str(filepath)
            f = open(filepath,'w')
            print >>f,code
        pagenum = pagenum + 1

qt = False
while not qt: 
    id = raw_input('请输入你的id:')
    password = getpass.getpass('请输入你的密码:')
    path = raw_input('请输入你想要保存的目录:')
    qt = run(id,password,path)
