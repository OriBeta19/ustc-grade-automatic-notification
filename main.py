#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grade import *

if not os.path.exists('config.json'):
    print('配置文件不存在，请创建配置文件。')
    smtp_username=input('请输入邮箱：')
    smtp_password=input("请输入邮箱密码：")
    student_number=input("请输入学号：")
    studnet_password=input("请输入统一登陆系统密码：")
    config={'enable_mail':True, 'smtp_server': 'mail.ustc.edu.cn', 'smtp_username':smtp_username, 'smtp_password':smtp_password, 'smtp_to':smtp_username, 
    'smtp_ssl':False, 'student_number':student_number, 'student_password':studnet_password, 'req_timeout':10, 'interval':60}
    config=json.dumps(config)
    with open('config.json','w') as conf:
        conf.write(config)
        
with open('config.json','r') as conf:
    config=json.load(conf)
    

postData = {
    "service": "https://jw.ustc.edu.cn/ucas-sso/login",
    "username": config['student_number'],
    "password": config['student_password']
}



sessionRequests = login(postData)
oldData = getGrade(sessionRequests)
while True:
    data = getGrade(sessionRequests)
    newGradeNumber = len(data[0])-len(oldData[0])
    if newGradeNumber!=0:
        mailContent=writeMail(data,newGradeNumber)
        print(mailContent)
        if config['enable_mail']:
            send_email("新成绩提醒", mailContent.encode('utf-8'))
    else:
        print('查询完成，没有新成绩！')
    oldData=data
    time.sleep(config['interval'])