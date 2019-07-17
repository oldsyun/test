from flask import Flask, request
from zeep import Client
import json,time,re

server=Flask(__name__)

@server.route('/message',methods=['post'])
def get_message():
    data = request.data
    json_data=json.loads(data)
    Num=json_data["eventContent"]["phone"]
    msg=json_data["eventContent"]["message"]
    C_msg=str2chines(msg)
    sendmsg(Num,C_msg)
    print ("发送号码："+Num+" 短信内容："+ C_msg)   
    return '{"status":"500"}'

def convert2Chr(str):
    convertOne=lambda x:chr(x)
    res=''
    for n in str.split(','):
        res+=convertOne(int(n,16))
    return res
    
def str2chines(string):
    chinesestr=''
    b=re.findall(r'.{4}', string)
    charstr=','.join(b)
    chinesestr=convert2Chr(charstr)
    return chinesestr

def sendmsg(pNumstr,Msg):
    ls=pNumstr.split(",")
    SimpleUserInfo={"username":"","password":""}#企信通帐号
    client = Client('http://202.102.41.99:8090/wsewebsm/services/SendMessageService?WSDL')
    for sendnum in ls:
        SendSmsRequest={"content":Msg,"receiveNum":sendnum,"sendType":"1","signature":""}
        client.service.sendSms(SimpleUserInfo,SendSmsRequest)
        time.sleep(0.5)

if __name__ == "__main__":
     server.run(host='0.0.0.0',port=1998)
