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
        tmmInfo_S = ''
        tmmInfo_L = []
        tmmSoup = BeautifulSoup(page)
        #find every mm's home page and infopage
        for eachone in tmmSoup.find_all('div', class_='list-item'):
            tmmInfo_S = str(eachone.find_all('a')[0]) + ' ' + str(eachone.find_all('a')[1])
            pattern = re.compile('<a class=.*?href="(.*?)".*?target.*?<a class="lady-name".*?href="(.*?)".*?target="_blank">(.*?)</a>', re.S)
            items = re.findall(pattern, tmmInfo_S)
            items = items[0]
            tmmInfo_L.append({'userID':items[1].split('user_id=')[-1], 'mmName':items[2], 'homeURL':items[0], 'mmInfo':items[1]})    
        #print len(tmmInfo_L)
        return tmmInfo_L
    
