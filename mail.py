#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib,json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open('config.json','r') as conf:
    config=json.load(conf)
    

def send_email(subject, html):
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
