#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pycurl
import smtplib
import string
import sys
import time

URLS = ['http://www.vsochina.com', 'http://www.baidu.com',  'http://www.sina.com']
for URL in URLS:        
   print '当前URL :', URL

URL = "http://www.vsochina.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, URL)  # 定义请求的URL常量

# 连接超时时间,5秒
c.setopt(pycurl.CONNECTTIMEOUT, 5)  # 定义请求连接的等待时间

# 下载超时时间,5秒
c.setopt(pycurl.TIMEOUT, 5)  # 定义请求超时时间
c.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
c.setopt(pycurl.MAXREDIRS, 1)  # 制定http重定向的最大数为1
c.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条

# 判断文件是否存在，不存在则创建
codepath = "/root/pythondev/httpcode.log"
if not os.path.exists(codepath):
    os.system(r'touch %s' % codepath)

codefile = open('/root/pythondev/httpcode.log', 'a+')
httpfile = open('/root/pythondev/httpfile.log', 'a+')

c.setopt(pycurl.WRITEHEADER, httpfile)
c.setopt(pycurl.WRITEDATA, httpfile)

# 提交请求
try:
    c.perform()
except Exception, e:
    print "connecion error:" + str(e)
    codefile.close()
    c.close()
    sys.exit()

HTTP_CODE = c.getinfo(c.HTTP_CODE)  # 获取HTTP状态码
print >> codefile, "HTTP状态：状态码%s 网页%s" % (HTTP_CODE, URL)
# 打印出当前时间
print >> codefile, time.strftime("%Y-%m-%d %A %X %Z", time.localtime())
print >> codefile, "---------------------------------------------------------------------------------"

# 定义邮件报警
HOST = "smtp.landhightech.com"  # 定义smtp主机
SUBJECT = "PROBLEM:www.vsochina.com httpcode is %s %s" % (HTTP_CODE, URL)  # 定义邮件主题
TO = "fchen@landhightech.com"  # 定义邮件收件人
FROM = "fchen@landhightech.com"  # 定义邮件发件人
text = "PROBLEM:www.vsochina.com httpcode is %s %s" % (HTTP_CODE, URL)  # 定义邮件内容
BODY = string.join((  # 组装sendmail方法的邮件主题内容，各段以“\r\n”进行分割
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
), "\r\n")

if HTTP_CODE != 200:
    print "HTTP状态正常：状态码%s 网页%s" % (HTTP_CODE, URL)
else:
    server = smtplib.SMTP()  # 创建一个SMTP()对象
    server.connect(HOST, "25")  # 通过connect方法连接smtp主机
    server.starttls()  # 启动安全传输模式
    server.login("fchen@landhightech.com", "PA$$w0rd123")  # 邮件账号登陆校验
    server.sendmail(FROM, [TO], BODY)  # 邮件发送
    server.quit()  # 断开smtp连接
    print "HTTP状态异常：状态码%s 网页%s" % (HTTP_CODE, URL)

codefile.close()
c.close()
