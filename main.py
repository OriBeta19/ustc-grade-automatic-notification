#!/usr/bin/env python
# -*- coding: utf-8 -*-

from grade import *
from mail import *
import itertools

if not os.path.exists('config.json'):
    print('配置文件不存在，请创建配置文件。')
    smtp_username = input('请输入邮箱：')
    smtp_password = input("请输入邮箱密码：")
    student_number = input("请输入学号：")
    studnet_password = input("请输入统一登陆系统密码：")
    config = {
        'enable_mail': True,
        'smtp_server': 'mail.ustc.edu.cn',
        'smtp_username': smtp_username,
        'smtp_password': smtp_password,
        'smtp_to': smtp_username,
        'smtp_ssl': False,
        'student_number': student_number,
        'student_password': studnet_password,
        'req_timeout': 10,
        'interval': 60
    }
    config = json.dumps(config, sort_keys=False, indent=4, separators=(',', ':'))
    with open('config.json', 'w') as conf:
        conf.write(config)

with open('config.json', 'r') as conf:
    config = json.load(conf)
    



postData = {
    "service": "https://jw.ustc.edu.cn/ucas-sso/login",
    "username": config['student_number'],
    "password": config['student_password']
}
postUrl = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin'
postHeaders = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.12 Safari/537.36 Edg/76.0.182.6',
    'Referer':
    'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin',
    'Connection': 'keep-alive'
}



sessionRequests = login(postUrl,postHeaders,postData)
oldData = getGrade(sessionRequests)


"""
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
win = MainWindow() #新建窗口
win.show()
sys.exit(app.exec_())
"""

test=True

while True:
    data = getGrade(sessionRequests)
    if test:
        diffData=data['semesters'][0]['scores']
    else:
        diffData = list(itertools.filterfalse(lambda x: x in oldData['semesters'][0]['scores'], data['semesters'][0]['scores']))  #TODO 刚入学的学生没有oldData
    if len(diffData) != 0:
        GPAData=calcGPA(data)
        mailContent = writeMail(diffData,GPAData)
        print(mailContent)
        if config['enable_mail']:
            sendMail("新成绩提醒", mailContent.encode('utf-8'))
    else:
        print('查询完成，没有新成绩！')
    oldData = data
    if test:
        break
    time.sleep(config['interval'])
