# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import re
import json
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60",
"Content-Type": "application/json",
"Referer": "https://ecp.sgcc.com.cn/ecp2.0/portal/",
}

def getNoticeBid(lstid):
    getNoticeBidurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeBid'
   # caigou='{"index":1,"size":20,"firstPageMenuId":"2018032900295987","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    res=json.loads(requests.post(url=getNoticeBidurl,data=json.dumps(lstid), headers=headers).text)
   
    print('TEL:'+res["resultValue"]["notice"]["TEL"])
    print('采购项目名称'+res["resultValue"]["notice"]["PURPRJ_NAME"])
    print('采购项目编号'+res["resultValue"]["notice"]["PURPRJ_CODE"])
    print('采购文件获取截止时间'+res["resultValue"]["notice"]["BIDBOOK_BUY_END_TIME"])


def getDownloadurl(lstid):
    downloadurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/downLoadBid?noticeId='+str(lstid)+'&noticeDetId='
    print ("downloading with requests")
    r = requests.get(downloadurl) 
    with open(str(lstid)+".zip", "wb") as code:
        code.write(r.content)

    
def main():
    url = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
    #data='{"index":1,"size":20,"firstPageMenuId":"2018032700291334","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    caigou='{"index":1,"size":20,"firstPageMenuId":"2018032900295987","purOrgStatus":"","purOrgCode":"","purType":"","orgId":"","key":""}'
    res = requests.post(url=url,data=caigou)
    #print(res.text)
    result=json.loads(res.text)
    for i in range(0,20):
        status=result['resultValue']["noteList"][i]['purOrgStatus']
        listid=result['resultValue']["noteList"][i]['id']
        code=result['resultValue']["noteList"][i]['code']
        BeginTime=result['resultValue']["noteList"][i]['topBeginTime']
        #print(listid,status,code,BeginTime)
        getNoticeBid(listid)
    getDownloadurl(2020121546309518)
   #res1=requests.post(url=viewurl,data=json.dumps('2020121118298053'), headers=headers)
   # print(res1.text)
    #url2='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeBid'
    #data2=str(id)
   # print(id)
    #res2 = requests.post(url=url2,data='2020121446116564')
   # print(res2.text)
   # downloadurl='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/downLoadBid?noticeId='+id+'&noticeDetId='


if __name__ =="__main__":
    main()
