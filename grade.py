#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests,time,os,json


def login(postUrl,postHeaders,postData):
    sessionRequests = requests.session()
    sessionRequests.post(url=postUrl, headers=postHeaders, data=postData)
    return sessionRequests


def getGrade(sessionRequests):
    source = sessionRequests.get(url='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?semesterIds')
    data=json.loads(source.text)
    return data



def calcGPA(data):
    semestersGPA=[]
    totalPoints,totalCredits=0,0
    for semester in data['semesters']:
        point,credit=0,0
        for subject in semester['scores']:
            if subject['gp'] is not None:
                credit+=subject['credits']
                point+=subject['gp']*subject['credits']
        if credit!=0:
            semestersGPA+=[{'semesterCh':semester['scores'][0]['semesterCh'],'gp':float(point)/credit}]
            totalPoints+=point
            totalCredits+=credit
    return {'gp':float(totalPoints)/totalCredits,'semesters': semestersGPA}
            

