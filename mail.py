#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib,json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open('config.json','r') as conf:
    config=json.load(conf)
    
def writeMail(diffData,GPAData):
    mailContent = '<div>您有' + str(len(diffData)) + '门新成绩，分别为：</div>'
    for subject in diffData:
        mailContent += '<div>    ' + subject['courseNameCh'] + '(' + str(subject['credits']) + '学分):总评=' + subject['score']
        if subject['gp'] is not None:
            mailContent += ',GPA=' + str(subject['gp'])
        mailContent += '</div>'
    mailContent +='</div>截至目前，您当前学期绩点为%.2f，%d学期总绩点为%.2f<div>'%(GPAData['semesters'][0]['gp'],len(GPAData['semesters']),GPAData['gp'])
    return mailContent


def sendMail(subject, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = config['smtp_username']
    msg['To'] = config['smtp_to']
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    if config['smtp_ssl']:
        s = smtplib.SMTP_SSL(config['smtp_server'])
    else:
        s = smtplib.SMTP(config['smtp_server'])
    s.login(config['smtp_username'], config['smtp_password'])
    s.sendmail(config['smtp_username'], config['smtp_to'], msg.as_string())
    s.quit()
