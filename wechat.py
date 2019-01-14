# -*- coding: utf-8 -*-

"""
 author:steedyu
 time:2018-07-31 13:38
"""
import requests
import time
import jsonpath
import json
import itchat
from apscheduler.schedulers.background import BackgroundScheduler
workday=0

def weatherman():

    url = 'https://free-api.heweather.net/s6/weather/forecast?'
    parameters='location=CN101190402&key=f03aa23702374f658a8eebd78c9521cf'
    rs = requests.get(url+parameters)
    rs_dict = json.loads(rs.text)
    daily_data = rs_dict['HeWeather6'][0]['daily_forecast']
    airurl='https://free-api.heweather.net/s6/air/now?'
    aqi= requests.get(airurl+parameters)
    aqi_dict = json.loads(aqi.text)
    aqi = aqi_dict['HeWeather6'][0]['air_now_city']['aqi']
    pm25 = aqi_dict['HeWeather6'][0]['air_now_city']['pm25']
    qlty = aqi_dict['HeWeather6'][0]['air_now_city']['qlty']
    texts='常熟空气质量%s \naqi指数：%s pm2.5:%s'%(qlty,aqi,pm25)
    nowurl='https://free-api.heweather.net/s6/weather/now?'
    now= requests.get(nowurl+parameters)
    now_dict = json.loads(now.text)
    cond=now_dict['HeWeather6'][0]['now']['cond_txt']
    fl=now_dict['HeWeather6'][0]['now']['fl']
    tmp=now_dict['HeWeather6'][0]['now']['tmp']
    hum=now_dict['HeWeather6'][0]['now']['hum']
    texts+='\n实时天气 %s 体感温度：%s℃ 温度:%s℃ 湿度:%s %%\n'%(cond,fl,tmp,hum)
    if rs_dict['HeWeather6'][0]['status']=='ok':
        for weather_dict in daily_data:
            date = weather_dict['date']
            weather = weather_dict['cond_txt_d']
            winddir = weather_dict['wind_dir']
            windsc = weather_dict['wind_sc']
            temp1 = weather_dict['tmp_min']
            temp2 = weather_dict['tmp_max']
            texts+='\n%s %s %s %s级 温度:%s℃~%s℃'%(date,weather,winddir,windsc,temp1,temp2)
    else:
        texts='没有查询到天气信息'
    return texts

def getresp():
    header={'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1154',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=14bque1pwsllnzt4gvppjijj; NewSolar=UserName=&Pwd=&Remember=',
            'Host': 'www.riyuecloud.com',
            'Origin': 'http://www.riyuecloud.com',
            'Referer': 'http://www.riyuecloud.com/View/Maker/MakerStations.aspx?parentId=paramenu_sites&currItem=menu_stations',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
    data ={'condition': '[]',
            'params': '{"gridId":"div_station","dataMode":"auto","navId":"div_pgnav","customHead":true,"customHeadID":"tb_station","customDataRowID":"","url":"/Business/BLL/BLLMaker/BLLMakerStations.ashx?action=queryStations","perPage":50,"tableLine":"auto","callbackFun":null,"cols":[{"type":"CustomColumn","html":"","databind":"STATUSIMG,STATUSALT"},{"type":"CustomColumn","html":"","databind":"ID,USERID,PWIMG"},{"type":"CustomColumn","html":"","databind":"ID,USERID,POWERSTATIONNAME"},{"databind":"COUNTRY"},{"databind":"TERMINALUSER"},{"databind":"CAPACITY"},{"databind":"POWER"},{"databind":"ETOTAL"},{"databind":"LASTUPDATETIME"},{"type":"CustomColumn","html":"","databind":"ID,USERID,ID"},{"databind":"CreateTime"}]}',
            'currPage':' 1'}
    ajax_url='http://www.riyuecloud.com/Business/BLL/BLLMaker/BLLMakerStations.ashx?action=queryStations'
    try :
        requests.post(ajax_url,data=data, headers=header)     
    except :
        print("error")
    finally:
        resp = requests.post(ajax_url,data=data, headers=header)
    return resp

def GetText():
    a=getresp().json()
    POWERSTATIONNAME=jsonpath.jsonpath(a,'$.Data.[*].POWERSTATIONNAME')
    STATUSALT=jsonpath.jsonpath(a,'$.Data.[*].STATUSALT')
    #TotalCount = jsonpath.jsonpath(a, '$.TotalCount')
    L1=list()
    L2=list()
    for x in POWERSTATIONNAME:
        L1.append(x)
    for x in STATUSALT:
        L2.append(x)
    D = dict(zip(L1,L2))
    D.pop('沪港电力')
    m2={}
    for k, v in D.items():
        if v in D: 
            m2[v].append(k)
        else:
            m2[v]=[]
    for k, v in D.items():
        if v in m2: 
            m2[v].append(k)
        else:
            m2[v]=[]
    m2.pop('工作正常')
    aq=[]
    texts=getall()+'\n'
    if m2:
        for k, v in m2.items():
            aq.append(k)
        for x in range(0,len(aq)):
            ls=m2.get(aq[x])
            texts +=('\n'+aligns(aq[x]+'数量:')+str(len(ls))+'\n'+ (','.join(ls)))
    else:
        texts=texts+'\n 全部正常'
    return texts

def aligns(string,length=20):
    difference = length - len(string)  # 计算限定长度为20时需要补齐多少个空格
    if difference == 0:  # 若差值为0则不需要补
        return string
    elif difference < 0:
        print('错误：限定的对齐长度小于字符串长度!')
        return None
    new_string = ''
    space = '　'
    for i in string:
        codes = ord(i)  # 将字符转为ASCII或UNICODE编码
        if codes <= 126:  # 若是半角字符
            new_string = new_string + chr(codes+65248) # 则转为全角
        else:
            new_string = new_string + i  # 若是全角，则不转换
    return new_string + space*(difference)  # 返回补齐空格后的字符串

def getall():
    data ={'action': 'getRunningData'}
    ajax_url='http://www.riyuecloud.com/Business/BLL/BLLMaker/BLLMakerIndex.ashx'
    resp = requests.post(ajax_url,data=data, cookies=GetCookie())
    dict=json.loads(resp.text)
    text= '当前功率 %s \n当天电量 %s\n当月电量 %s\n当年电量 %s\n总电量 %s\n异常逆变器 %s'%(dict['Data']['POWERNOW'],dict['Data']['TODAYENERGY'],dict['Data']['MONTHENERGY'],dict['Data']['YEARENERGY'],dict['Data']['TOTALENERGY'],dict['Data']['ABNORMALINVERTER'])
    return text
    
def getworkday():
    date=time.strftime("%Y%m%d")
    r = requests.get(r'http://api.goseek.cn/Tools/holiday?date=' + date)  
    r.encoding = r.apparent_encoding
    json_data = json.loads(r.text)
    global workday
    workday=json_data['data']
    return workday

def GetCookie():
    imgUrl='http://www.riyuecloud.com/Business/BLL/BLLUser/BLLHUser.ashx'
    s=requests.session()
    res=s.get(imgUrl,stream=True)
    loginUrl='http://www.riyuecloud.com/Business/BLL/BLLUser/BLLHUser.ashx'
    postData={'action': 'login','user': 'm-cskg','pwd': 'j10j10j10','rememberMe': ''}
    rs=s.post(loginUrl,postData)
    c=requests.cookies.RequestsCookieJar()
    s.cookies.update(c)
    dict=s.cookies.get_dict()
    return s.cookies 
	
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply_msg(msg):
    if msg['Content'] == u'太阳能状态':
        sendstate()
    elif msg['Content'] == u'天气预报':
        sendweather()

def sendstate():
    if workday==0:
        t=GetText()
        group  = itchat.get_chatrooms(update=True)
        for g in group:
            if g['NickName'] == '技术十科':
                to_group = g['UserName']
                itchat.send(t+"\n---------"+"\n发自智障机器人",to_group)
                print(time.strftime("%Y-%m-%d %H:%M:%S") +"   send Group ok")

def sendding():
    if workday==0:
        users=itchat.search_friends("丁惠明")
        usName= users[0]['UserName']
        if GetText()!='':
            itchat.send(GetText()+"\n---------"+"\n技术10科机器人",toUserName=usName)
            print(time.strftime("%Y-%m-%d %H:%M:%S") +"   send Ding ok")

def sendweather():
    group  = itchat.get_chatrooms(update=True)
    for g in group:
        if g['NickName'] == '技术十科':
            to_group = g['UserName']
            itchat.send(weatherman()+"\n---------"+"\n发自智障机器人",to_group)
            print(time.strftime("%Y-%m-%d %H:%M:%S") +"   send weather ok")

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=True,hotReload = True)
    scheduler = BackgroundScheduler(misfire_grace_time=36000)
    scheduler.add_job(getworkday, 'cron', day_of_week='*', hour=6, minute=55)
    scheduler.add_job(sendstate, 'cron', day_of_week='*', hour=8, minute=30)
    scheduler.add_job(sendstate, 'cron', day_of_week='*', hour=12, minute=30)
    scheduler.add_job(sendstate, 'cron', day_of_week='*', hour=15, minute=00)
    scheduler.add_job(sendding, 'cron', day_of_week='*', hour=13, minute=00)	
    scheduler.start() 
    itchat.run()