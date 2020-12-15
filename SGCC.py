import requests
import json
from datetime import datetime
import time
import os
import openpyxl

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60",
"Content-Type": "application/json",
"Referer": "https://ecp.sgcc.com.cn/ecp2.0/portal/",
}
codelist=[]

def getNoticeBid(lstid):
    getNoticeBidurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeBid'
   # caigou='{"index":1,"size":20,"firstPageMenuId":"2018032900295987","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    res=json.loads(requests.post(url=getNoticeBidurl,data=json.dumps(lstid), headers=headers).text)   
    print('采购项目名称：'+res["resultValue"]["notice"]["PURPRJ_NAME"])
    print('采购项目编号：'+res["resultValue"]["notice"]["PURPRJ_CODE"])
    print('采购文件获取截止时间：'+res["resultValue"]["notice"]["BIDBOOK_BUY_END_TIME"])
    print('采购类型：'+res["resultValue"]["notice"]["PUR_TYPE_NAME"])
    print('开启应答文件时间：'+res["resultValue"]["notice"]["BIDBOOK_SELL_BEGIN_TIME"])
    print('采购人：'+res["resultValue"]["notice"]["PUBLISH_ORG_NAME"])
   # print('联系人：'+res["resultValue"]["notice"]["CONTACT"])
    print('开启应答文件地点:'+res["resultValue"]["notice"]["OPENBID_ADDR"])
    #print('招标代理机构:'+res["resultValue"]["notice"]["BID_AGT"])
    #print('招标代理机构邮编:'+res["resultValue"]["notice"]["BID_AGT_ADDR_ZIP_CODE"])
    #print('联系电话:'+res["resultValue"]["notice"]["TEL"])
    #print('E_MAIL:'+res["resultValue"]["notice"]["E_MAIL"])
   
 
def getChangeBid(lstid): 
    getChangeBidurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getChangeBid'
   # caigou='{"index":1,"size":20,"firstPageMenuId":"2018032900295987","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    res=json.loads(requests.post(url=getChangeBidurl,data=json.dumps(lstid), headers=headers).text)

#def writexls(Bidjson):


def getDownloadurl(lstid):
    downloadurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/downLoadBid?noticeId='+str(lstid)+'&noticeDetId='
    print ("downloading with requests")
    r = requests.get(downloadurl) 
    with open(str(lstid)+".zip", "wb") as code:
        code.write(r.content)

def caigou():
    url = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
    #zizhi='{"index":1,"size":20,"firstPageMenuId":"2018032700290425","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    #toubiao='{"index":1,"size":20,"firstPageMenuId":"2018032700291334","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    caigou='{"index":1,"size":20,"firstPageMenuId":"2018032900295987","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    res = requests.post(url=url,data=caigou)
    result=json.loads(res.text)
    for i in range(0,20):
        #status=result['resultValue']["noteList"][i]['purOrgStatus']
        listid=result['resultValue']["noteList"][i]['id']
        code=result['resultValue']["noteList"][i]['code']
        doctype=result['resultValue']["noteList"][i]['doctype']#doci-bid采购公告 doci-change：变更
        if doctype=="doci-bid":
            print("新增采购公告\r")
            if code in codelist:
                pass
            else:
                codelist.append(code)
                with open('list.txt', "a") as f:
                    f.write(code+"\r")
                getNoticeBid(listid)
        if doctype=="doci-change":
            print("新增变更公告\r")
            #getChangeBid(listid)
            pass
    
    

if __name__ =="__main__":
    if not os.path.exists('list.txt'):
        with open('list.txt', "w") as f:
            f.write("")
    else:
        with open('list.txt', "r") as f:
            for line in f:
                codelist.append(list(line.strip('\n').split(',')))
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        caigou()
        time.sleep(300)
