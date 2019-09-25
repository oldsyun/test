import paho.mqtt.client as mqtt
import datetime,pymysql,json
import re

hubAddress = '127.0.0.1'
deviceId = 'LMte'
hubTopicSubscribe = '/gateway/#'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe(hubTopicSubscribe)

def on_message(client, userdata, msg):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    data_json = msg.payload.decode("utf-8")
    d = json.loads(data_json)
    result = re.split(r'/gateway/(.+?)/data',msg.topic)
    sn=result[1]
    strkv=""
    Li=[]
    devname=d['device'][0]['dev_name']
    comstate=d['device'][0]['comm_s']
    devstr='`'+devname+'com_s`='+str(comstate)
    Li.append('com_s')
    for i in d['device'][0]['variable']:
        devstr=devstr+',`'+(devname+i)+'`='+d['device'][0]['variable'][i]
        Li.append(i)
    strkv='INSERT INTO `'+sn+'` SET '+devstr+',`timestrap`='+'\''+now+'\''
    if comsql(strkv)==0:
        a=Getcolumn_name(sn)
        b = [y for y in (a+Li) if y not in a]
        if len(b)>0:
            for i in range(0,len(b)):
                AddColumn(sn,str(devname+b[i]))

def Createtable(sn):
    sql="CREATE TABLE `dev`.`"+sn+"`( `id` int(11) NOT NULL AUTO_INCREMENT, `timestrap` timestamp(0) NULL, PRIMARY KEY (`id`))"
    comsql(sql)

def Getcolumn_name(sn):
    sql='select column_name from information_schema.columns where table_name=\''+sn+'\' and table_schema=\'dev\'' 
    se=comsql(sql)
    if not se:
        Createtable(sn)
    else:
        se1=comsql(sql)
        ls=[]
        ls2=[]
        for data in se1:
            ls.append(list(data))
        for i in range(0,len(ls)):
            ls2.append(str(ls[i][0]))
        return(ls2[2:])

def AddColumn(sn,Column):
    sql='ALTER TABLE `'+sn+'`ADD COLUMN `'+Column+'`  float(11,2) NULL' 
    comsql(sql)
   
def comsql(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                user='zcpd',
                                passwd='cslg!@#123',
                                db='dev',
                                port=3306,
                                charset='utf8'
                                )
    cur=connection.cursor()
    try: 
        cur.execute(sql)
        see=cur.fetchall()
        connection.commit()
        print (sql)
        return see 
    except :
        connection.rollback()
        return 0
    finally:
        cur.close()
        connection.close()

client = mqtt.Client(client_id=deviceId)
client.on_connect = on_connect
client.on_message = on_message
client.connect(hubAddress, port=1883, keepalive=60)
client.subscribe(hubTopicSubscribe,qos=0)
client.loop_forever()
