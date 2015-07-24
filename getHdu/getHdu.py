#!/usr/bin/python
# coding=utf-8

import requests
import re
import HTMLParser
import getpass
html_parser = HTMLParser.HTMLParser()
s = requests.session()
cookies = dict(cookies_are='working')
vis = {}

def login(id,password):
    data = {
        'username':id,
        'userpass':password,
        'login':'Sign in'
    }
    url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    r = s.post(url,data=data,cookies=cookies)
    if id in r.text:
        return True
    else:
        return False


def getCode(runid):
    url = "http://acm.hdu.edu.cn/viewcode.php?rid=" + runid
    r = s.get(url,cookies=cookies)
    r.encoding = 'gb2312'
    txt = r.text
    pattern = re.compile('<textarea id=usercode style="display:none;text-align:left;">(.+?)</textarea>',re.S)
    ans = pattern.findall(txt)[0]
    return html_parser.unescape(ans)#.decode('utf8'))

    
def run(id,password,path):
    ok = False;
    while not ok:
        try:
            ok = login(id,password)
        except Exception:
            print 'Something error'
        if not ok:
            print 'Wrong id or Wrong password'
    url = 'http://acm.hdu.edu.cn/status.php?first=&pid=&user='+id+'&lang=0&status=5'
    flag = True
    while flag:
        try:
            r = s.get(url,cookies=cookies)
        except Exception:
            continue
        txt = r.text
        pattern = re.compile('/showproblem.php\\?pid=(.+?)">(.+?)</a></td><td>(.+?)</td><td>(.+?)</td><td><a href="/viewcode.php\\?rid=(.+?)"',re.S)
        ans = pattern.findall(txt)
        for line in ans:
            tihao = line[0]
            if vis.has_key(tihao):
                continue
            else :
                #print tihao
                filepath = path + '/hdu/%s.cpp' %(tihao)
                print '正在保存hdu'+str(tihao)+'的代码到'+str(filepath)
                vis[tihao] = True
                runid = line[-1]
                code = getCode(runid).encode('utf8')
                code = code.replace('\r\n','\n')
                #filepath = (r'/Users/huangchengbo/code/hdu/%s.cpp'%(tihao))
                f = open(filepath,'w')
                print >> f,code
        pattern = re.compile('Prev Page</a><a style="margin-right:20px" href="(.+?)">Next Page',re.S)
        #print txt
        ans = pattern.findall(txt)
        if ans == []:
            flag = False;
        else:
            url = 'http://acm.hdu.edu.cn' + ans[0]

id = raw_input('请输入你的id:')
password = getpass.getpass('请输入你的密码:')
path = raw_input('请输入你想要保存的目录:')
run(id,password,path)
