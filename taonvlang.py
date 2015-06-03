#!/usr/bin/python
#coding=utf-8
import urllib2, urllib
import re, os, commands, signal, chardet
import simplejson as json
import time, mycookie
from bs4 import BeautifulSoup
from os.path import getsize
from multiprocessing import Process, Queue

class TAONVLANG:

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def getpage(self, encodeInfo):
        try:
            headers = mycookie.headers
            requset = urllib2.Request(self.baseurl, headers=headers)
            response = urllib2.urlopen(requset, timeout=3)
            if encodeInfo == 'gb2312':
                return response.read().decode('gb2312', 'ignore')
            elif encodeInfo == 'utf-8':
                #print chardet.detect(response.read().decode('gb2312', 'ignore'))
                return response.read().decode('gb2312', 'ignore').encode('utf-8')
        except Exception, e:
            print e
        """
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接失败，错误原因' + e.reason
                return None
        """        
    def getPic_BS(self, page):
        picList_temp = []
        try:
            soup = BeautifulSoup(page) 
            pattern = re.compile('<img.*?src="(.*?)"', re.S)

            for eachone in soup.find_all('div', class_='mm-aixiu-content')[0].find_all('img'):
                items = re.findall(pattern, str(eachone))
                if len(items)>1:
                    print u'在items找到多个图片链接'
                elif len(items)==1:
                    if items[0].split('.')[-1]=='jpg':
                        picList_temp.append(items[0])
                    else:
                        pass
            return picList_temp
        except Exception, e:
            print e

    def saveImg(self, imgURL, fileName):
        u = urllib2.urlopen(imgURL)
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

    def isImage(self, filename):
        try:
            imageSize = os.path.getsize(filename)
            if imageSize<1000:      # <1k bytes
                return False
            else:
                return True
        except Exception, e:
            print e

    def rmImage(self, filename):
        try:
            os.remove(filename)
            print 'remove ' + filename
        except Exception, e:
            print e
            pass

if __name__ == '__main__':
    tmmInfo_L = []
    def noName():
        for x in xrange(1, 1000):     #if there are 1000 no name mm
            yield x

    #try:
    def mmStart(pageNum, curmmNum=1):
        curmmNum_now = curmmNum-1
        noNameIter = noName()
        #q.put(os.getpid())  #1st
        for i in range(pageNum, 999):
            #q.put(i)    #2st
            tmm = TAONVLANG('http://mm.taobao.com/json/request_top_list.htm?type=0&page=' + str(i))
            tmmPage = tmm.getpage('utf-8')
            tmmInfo_L = tmm.getMMInfo(tmmPage)
            
            for eachone in tmmInfo_L[curmmNum-1:]:
                curmmNum_now = curmmNum_now+1 if curmmNum_now!=10 else 1
                #if curmmNum_now==11:
                 #   curmmNum_now = 1
                #q.put(curmmNum_now)   #3st
                q.put({'tmmpid':os.getpid(), 'tmmPageNum':i, 'tmmCurmmNum':curmmNum_now})

                taonvlang = TAONVLANG(str(eachone['homeURL']))
                pageHome = taonvlang.getpage('gb2312')
                
                picURL_List = taonvlang.getPic_BS(pageHome)
                try:
                    result = taonvlang.mkDir('/home/zm/pythonProject/spider/taonvlang/pic/' + eachone['mmName']) if eachone['mmName']!='' else taonvlang.mkDir('/home/zm/pythonProject/spider/taonvlang/pic/' + 'NO NAME-' + str(noNameIter.next()))    
                    print str(len(picURL_List))
                    print result
                    if result and len(picURL_List)>=1:
                        fileNameNum = 1
                        print 'Name=' + eachone['mmName']
                        for eachone1 in picURL_List:
                            houzhui = eachone1.split('.')[-1]
                            imageName = result + '/' + str(fileNameNum) + '.' + houzhui
                            try:
                                taonvlang.saveImg(eachone1, imageName)
                            except Exception, e:
                                print 'get page error'
                                continue
                            if taonvlang.isImage(imageName):
                                fileNameNum = fileNameNum+1
                            else:
                                taonvlang.rmImage(imageName)
                            time.sleep(0.2)
                except Exception, e:
                    print e
                #q.put('status_OK!')    #4st
            curmmNum = 1

    def wdProc():

        #tmmpid = q.get(timeout=10)
        #pageNum_wd = q.get(timeout=10)
        #curmmNum_wd = q.get(timeout=10)
        #print 'before:   ' + str(curmmNum_wd)
        while True:
            try:
                tmmMessage = q.get(timeout=120)
                tmmpid = tmmMessage['tmmpid']
                pageNum_wd = tmmMessage['tmmPageNum']
                curmmNum_wd = tmmMessage['tmmCurmmNum']
                print '---------------------------------------------------------------------------------------------------------------------------------------------\n'
                print tmmMessage
            except Exception, e:
                print '\nno food! and restart the tmmTask!'
                print pageNum_wd
                print curmmNum_wd
                os.kill(tmmpid, signal.SIGKILL)
                if curmmNum_wd==10:
                    pageNum_wd = pageNum_wd+1
                    curmmNum_wd = 0
                Process(target=mmStart,args=(pageNum_wd, curmmNum_wd+1)).start()
                print 'after:   ' + str(curmmNum_wd)

    q = Queue()
    watchDogProc = Process(target=wdProc,args=())
    watchDogProc.start()
    tmmProc = Process(target=mmStart,args=(100, 6))
    tmmProc.start()

    