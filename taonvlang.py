#coding=utf-8
#!/usr/bin/python
import urllib2
import urllib
import re
import os
import simplejson as json
import chardet
import time

class TAONVLANG:

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def getpage(self, encodeInfo):
        try:
            #url = self.baseurl + str(self.userID)
            #print url
            headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',  
            'Referer' : 'http://www.taobao.com/',
            'Cookie' : 'mt=ci%3D-1_0; swfstore=11752; thw=cn; cna=P4DGDUWar2oCAW/FA7ZQvkVB; isg=55830F387A8DC0C65155A01CBAEBB86A; l=Acw/L3MgzLTMtJns7Iqrccy07LvMtMy0; t=1bf47062fdf4c6884d655ecf02da7167; mt=ci=5_1&cyk=0_1; CNZZDATA30064598=cnzz_eid%3D2046030241-1431753429-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1431786008; CNZZDATA30063600=cnzz_eid%3D1682120793-1431752062-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1431784532; JSESSIONID=D63D7A030918D47AB9BEEED4873ABE74; v=0; cookie2=11557083fc9c4bd47dc4c22b24766f20; _tb_token_=f754348d5ede6; existShop=MTQzMTgzODc3MA%3D%3D; unt=tt88050643%26center; tracknick=tt88050643; _cc_=UIHiLt3xSw%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%260; uc3=nk2=F4ItT%2BRNzT1W6A%3D%3D&id2=VWhZ6XpmGeVT&vt3=F8dAT%2BLDvr9JYmaXjJw%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=tt88050643; CNZZDATA30063598=cnzz_eid%3D272153817-1431782106-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1431782106; CNZZDATA30064595=cnzz_eid%3D848796480-1431785877-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1431785877; uc1=lltime=1431781249&cookie14=UoW0EwwKX8hmhQ%3D%3D&existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=UIHiLt3xTIkz&tag=3&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; sg=32e; cookie1=B0as0VkCphZkhxs8xnE%2FUyLcJKEFAHoZTL2vsqgxCaE%3D; unb=672903372; _l_g_=Ug%3D%3D; _nk_=tt88050643; cookie17=VWhZ6XpmGeVT',
            }
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

    def saveImg(self, imgURL, fileName):
        u = urllib.urlopen(imgURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    def getModelName(self, page):
        pattern = re.compile('<li class="mm-p-noborder">.*?<dd><a href.*? target="_blank">(.*?)</a></dd>', re.S)
        modelName = '.'.join(re.findall(pattern, page))
        return modelName        

    def mkDir(self, dirName):
        isExists = os.path.exists(dirName)
        if not isExists:
            os.makedirs(dirName)
            return dirName
        else:
            return False

    def getModelInfo(self, page):
        modelInfo_Dict = json.JSONDecoder().decode(page)
        modelInfo_List = modelInfo_Dict['data']['searchDOList']
        return modelInfo_List

taonvlangModelInFo = TAONVLANG('http://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
pageModelInfo = taonvlangModelInFo.getpage('utf-8')

modelInfo_ID_List = taonvlangModelInFo.getModelInfo(pageModelInfo)
print len(modelInfo_ID_List)

for eachone in modelInfo_ID_List:
    taonvlang = TAONVLANG('http://mm.taobao.com/self/aiShow.htm?spm=0.0.0.0.M3UhJS&userId=' + str(eachone['userId']))
    pageHome = taonvlang.getpage('gb2312')
    picURL_List = set(taonvlang.getPic(pageHome))
    result = taonvlang.mkDir('/home/zm/PycharmProjects/spider/' + eachone['realName'])
    if result:
        fileNameNum = 1
        print result
        for eachone in picURL_List:
            houzhui = eachone.split('.')[-1]
            taonvlang.saveImg(eachone, result + '/' + str(fileNameNum) + '.' + houzhui)
            fileNameNum = fileNameNum + 1

            