import paho.mqtt.client as mqtt
import datetime,json
import re
from influxdb import InfluxDBClient

hubAddress = '193.112.184.216'
deviceId = 'Low12'
hubTopicSubscribe = '/gateway/#'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe(hubTopicSubscribe)

def data2influx(SN,dictstr):
    try:
        point=[]
        client = InfluxDBClient('localhost', 8086, '', '', 'home') 
        current_time = datetime.datetime.utcnow().isoformat("T")
        for dev in dictstr['device']:
            devname=dev['dev_name']
            comstate=dev['comm_s']
            field=dev['variable']
            L1=list()
            L2=list()
            if comstate:
                for k,v in field.items():
                    if field[k]!='bad':
                        field[k]=float(v)
                    L1.append(devname+k)
                    L2.append(v)
                newfield=dict(zip(L1,L2))
                json_body = {
                    "measurement": SN,
                    "time": current_time,
                    "fields": newfield
                    }
                point.append(json_body)
        client.write_points(point)
    except Exception as e:
        print (str(e))
        pass


def on_message(client, userdata, msg):
    data_json = msg.payload.decode("utf-8")
    if is_json(data_json):
        d = json.loads(data_json)
        result = re.split(r'/gateway/(.+?)/data',msg.topic)
        sn=result[1]
        data2influx(sn,d)

def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True

client = mqtt.Client(client_id=deviceId)
client.on_connect = on_connect
client.on_message = on_message
client.connect(hubAddress, port=1883, keepalive=60)
client.subscribe(hubTopicSubscribe,qos=0)
client.loop_forever()
