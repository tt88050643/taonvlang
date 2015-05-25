#coding=utf-8
#!/usr/bin/env python
import urllib2
import urllib
import re, os, commands
import simplejson as json
import chardet
import time
import FindToHomePage, mycookie
from bs4 import BeautifulSoup
class TAONVLANG:

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

    def getPic(self, page):
        pattern = re.compile('<img style.*?src="(.*?)"/>', re.S)
        items = re.findall(pattern, page)
        return items

#<img height="559" src="http://img01.taobaocdn.com/imgextra/i1/10490029241756805/T1zm_SFhFXXXXXXXXX_!!631300490-0-tstar.jpg" style="margin: 10.0px;width: 630.0px;height: 559.0px;float: none;" width="630"/>

    def getPic_BS(self, page):
        picList_temp = []
        soup = BeautifulSoup(page) 
        pattern = re.compile('<img.*?src="(.*?)"', re.S)

        for eachone in soup.find_all('div', class_='mm-aixiu-content')[0].find_all('img'):
            items = re.findall(pattern, str(eachone))
            if len(items)>1:
                print u'在items找到多个图片链接'
            elif len(items)==1:
                picList_temp.append(items[0])
        return picList_temp
        #for eachone in soup.find_all('img'):
         #   print eachone

    def saveImg(self, imgURL, fileName):
        u = urllib.urlopen(imgURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()     

    def mkDir(self, dirName):
        isExists = os.path.exists(dirName)
        if not isExists:
            os.makedirs(dirName)
            return dirName
        else:
            commands.getstatusoutput('rm -rf ' + dirName)[0]
            os.makedirs(dirName)
            if os.path.exists(dirName):
                return dirName
            else:
                return False

if __name__ == '__main__':
    tmmInfo_L = []
    #try:
    for i in range(1,2):
        tmm = FindToHomePage.TMMINDEX('http://mm.taobao.com/json/request_top_list.htm?type=0&page=' + str(i))
        tmmPage = tmm.getpage('utf-8')
        tmmSoup = BeautifulSoup(tmmPage)
        #find every mm's home page and infopage
        for eachdiv in tmmSoup.body.children:
            if eachdiv!=' ' and eachdiv!='\n' and eachdiv.name!='input':
                tempList = []
                for eacha in eachdiv.descendants:
                    if eacha.name=='a':
                        tempList.append(str(eacha))
                tmmInfo_L.append(tmm.getMMInfo(tempList[0]+tempList[1])[0])
        time.sleep(1)
    for eachone in tmmInfo_L:
        taonvlang = TAONVLANG(str(eachone['homeURL']))
        pageHome = taonvlang.getpage('gb2312')
        picURL_List = set(taonvlang.getPic_BS(pageHome))

        result = taonvlang.mkDir('/home/zm/pythonProject/spider/taonvlang/pic/' + eachone['mmName'])
        print result
        if result:
            fileNameNum = 1
            print 'Name=' + eachone['mmName']
            for eachone1 in picURL_List:
                houzhui = eachone1.split('.')[-1]
                taonvlang.saveImg(eachone1, result + '/' + str(fileNameNum) + '.' + houzhui)
                fileNameNum = fileNameNum + 1
                time.sleep(0.2)
    #except Exception, e:
        #print e
        #print 'This is ERROR!'

            
        