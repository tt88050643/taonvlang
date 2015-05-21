#coding=utf-8
#!/usr/bin/env python
import urllib2
import urllib
import re
import os
import simplejson as json
import chardet
import time
import FindToHomePage

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
            'Cookie' : 'cna=qVetDR7bXmkCAXtz2MiGKwJ2; thw=cn; miid=6047895603556384903; v=0; _tb_token_=7eee9bd88e43e; CNZZDATA30064595=cnzz_eid%3D1706728516-1432203658-%26ntime%3D1432219901; CNZZDATA30063598=cnzz_eid%3D132888848-1432202918-http%253A%252F%252Ftool.chinaz.com%252F%26ntime%3D1432218234; CNZZDATA30064598=cnzz_eid%3D794984706-1432200478-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1432223045; CNZZDATA30063600=cnzz_eid%3D280477778-1432200739-http%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1432222380; JSESSIONID=270E66A7650C3B41AD28CE03BAE36963; uc3=nk2=F4ItT%2BRNzT1W6A%3D%3D&id2=VWhZ6XpmGeVT&vt3=F8dAT%2BLPk%2BjrRKhOrrM%3D&lg2=URm48syIIVrSKA%3D%3D; existShop=MTQzMjIzMDE3NA%3D%3D; unt=tt88050643%26center; lgc=tt88050643; tracknick=tt88050643; sg=32e; cookie2=1c5cfb883f430ac23108502dab84d56a; mt=np=&ci=5_1&cyk=0_0; cookie1=B0as0VkCphZkhxs8xnE%2FUyLcJKEFAHoZTL2vsqgxCaE%3D; unb=672903372; t=1509c05a655237fba2de70dd36002959; _cc_=VT5L2FSpdA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=tt88050643; cookie17=VWhZ6XpmGeVT; uc1=lltime=1432202205&cookie14=UoW0EP9b%2BEzpkQ%3D%3D&existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=VFC%2FuZ9ainBZ&tag=3&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; isg=0B5590964A219D0562BAADCEC71F6296; l=ARDArk6AEPAQ8EWuCcwXnhDwGP8Q6xDw',
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

if __name__ == '__main__':
    for i in range(1,11):
        tmm = FindToHomePage.TMMINDEX('http://mm.taobao.com/json/request_top_list.htm?type=0&page=' + str(i))
        tmmPage = tmm.getpage('utf-8')
        tmmInfo_L = tmm.getMMInfo(tmmPage)
        tmmInfo_L_Final = []
        
        for eachone in tmmInfo_L:
            tmmInfo_L_Final.append({'userID':eachone[0].split('/')[3].split('.')[0], 'mmName':eachone[2], 'homeURL':eachone[0], 'mmInfo':eachone[1]})
        for eachone in tmmInfo_L_Final:
            print eachone['homeURL']        

        for eachone in tmmInfo_L_Final:
            
            taonvlang = TAONVLANG(str(eachone['homeURL']))
        
            pageHome = taonvlang.getpage('gb2312')
            picURL_List = set(taonvlang.getPic(pageHome))
            result = taonvlang.mkDir('/home/zm/PycharmProjects/spider/' + eachone['mmName'])
            if result:
                fileNameNum = 1
                print result
                time.sleep(0.3)
                for eachone1 in picURL_List:
                    houzhui = eachone1.split('.')[-1]
                    taonvlang.saveImg(eachone1, result + '/' + str(fileNameNum) + '.' + houzhui)
                    fileNameNum = fileNameNum + 1

                        

                    