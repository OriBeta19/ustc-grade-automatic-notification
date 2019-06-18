#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests,time,os,json
from mail import send_email


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

def login(postData):
    sessionRequests = requests.session()
    sessionRequests.post(url=postUrl, headers=postHeaders, data=postData)
    return sessionRequests


def parseGrade(grade):
    soup = BeautifulSoup(grade)
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        elems = row.find_all('td')
        if len(elems) == 6:
            subGrade = [td.get_text() for td in elems]
            data.append([subGrade[0]] + subGrade[3:6])
    return data


def getGrade(sessionRequests):
    sheet = sessionRequests.get(url='https://jw.ustc.edu.cn/for-std/grade/sheet')
    soupSheet = BeautifulSoup(sheet.text)
    realUrl = 'https://jw.ustc.edu.cn' + soupSheet.find('form').get('action')
    semesters = soupSheet.find_all('option')
    data = []
    for semester in semesters[1:len(semesters)]:
        grade = sessionRequests.get(realUrl + '?semester=' + semester.get('value'))
        semesterData = parseGrade(grade.text)
        semesterData.insert(0, semester.string)
        data.append(semesterData)
    return data


def writeMail(data, newGradeNumber):
    mailContent = '<div>您有' + str(newGradeNumber) + '门新成绩，分别为：</div>'
    for subject in data[0][1:newGradeNumber + 1]:
        mailContent += '<div>    ' + subject[0] + '(' + subject[1] + '学分):总评=' + subject[3]
        if subject[2] != ' ':
            mailContent += ',GPA=' + subject[2]
        mailContent += '</div>'

    def calcGPA(gradeData):
        point = 0
        credit = 0
        for subject in gradeData:
            if subject[2] == ' ':
                continue
            credit += float(subject[1])
            point += float(subject[2]) * float(subject[1])
        return [point, credit]

    GPA = []
    for semester in data:
        GPA.append(calcGPA(semester[1:len(semester)]))
    if GPA[0][1] != 0:
        mailContent += '<div>您本学期平均绩点为' + '%.2f' % (GPA[0][0] / GPA[0][1]) + '</div>'
    totalPoint = 0
    totalCredit = 0
    for semester in GPA:
        totalPoint += semester[0]
        totalCredit += semester[1]
    if totalCredit != 0:
        mailContent += '<div>您截至目前'+str(len(GPA))+'学期总平均绩点为' + '%.2f' % (totalPoint / totalCredit) + '</div>'
    return mailContent



