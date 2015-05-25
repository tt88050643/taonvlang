#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import os, sys, time, re
import simplejson as json
import chardet
import mycookie
from bs4 import BeautifulSoup

reload(sys) 
sys.setdefaultencoding('utf-8') 

class TMMINDEX:

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def getpage(self, encodeInfo):
        try:
            #url = self.baseurl + str(self.userID)
            #print url
            headers = mycookie.headers
            requset = urllib2.Request(self.baseurl, headers=headers)
            response = urllib2.urlopen(requset)
            if encodeInfo == 'gb2312':
                return response.read().decode('gb2312', 'ignore')
            elif encodeInfo == 'utf-8':
                #print chardet.detect(response.read().decode('gb2312', 'ignore'))
                return response.read().decode('gb2312', 'ignore').encode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接失败，错误原因' + e.reason
                return None

    def getMMInfo(self, page):

        tmmSoup = BeautifulSoup(page)
        #find every mm's home page and infopage
        print tmmSoup.find_all('div', class_='list-item').find_all('a')
        """    
        for eachdiv in tmmSoup.body.children:
            if eachdiv!=' ' and eachdiv!='\n' and eachdiv.name!='input':
                tempList = []
                for eacha in eachdiv.descendants:
                    if eacha.name=='a':
                        tempList.append(str(eacha))
                tmmInfo_L.append(tmm.getMMInfo(tempList[0]+tempList[1])[0])



        pattern = re.compile('<a class=.*?href="(.*?)".*?target.*?<a class=.*?href="(.*?)".*?target="_blank">(.*?)</a>', re.S)
        items = re.findall(pattern, page)
        tmmInfo_L = []
        for eachone in items:
            tmmInfo_L.append({'userID':eachone[0].split('/')[-1].split('.')[0], 'mmName':eachone[2], 'homeURL':eachone[0], 'mmInfo':eachone[1]})       
        return tmmInfo_L
        """
