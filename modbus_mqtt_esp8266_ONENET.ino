#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ModbusMaster.h> 

#define MQTT_VERSION == MQTT_VERSION_3_1_1
#define DE_RE  15
#define LED 2
unsigned int flag = HIGH;

// Onenet 设置
const char *clientID = "xxxxxxxx"; //ONENET 设备ID
const char *username = "xxxxxx";   //ONENET产品ID
const char *password = "xxxxxxxxx"; //ONENET鉴权信息  
const char *mqtt_server ="183.230.40.39";

long lastMsg = 0;

WiFiClient espClient;
PubSubClient client(espClient);
ModbusMaster node;

void setup()
{
  pinMode(D6,OUTPUT);
  digitalWrite(D6, LOW);
  pinMode(D3,INPUT);
  pinMode(DE_RE, OUTPUT);
  digitalWrite(DE_RE, 0);
  pinMode(LED, OUTPUT);   
  digitalWrite(LED, HIGH);
  Serial.begin(19200,SERIAL_8E1);
  node.begin(1, Serial);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);
  if(!autoConfig()){
    smartConfig();
  }
  client.setServer(mqtt_server, 6002);
  client.connect(clientID, username, password);
  client.setCallback(callback);
}

void preTransmission()
{
   digitalWrite(DE_RE, 1);
}

void postTransmission()
{
  digitalWrite(DE_RE, 0);
}
/**
* 开启SmartConfig功能
*/
void smartConfig()
{
  WiFi.mode(WIFI_STA);
  delay(2000);
  WiFi.beginSmartConfig();
  while (1){
    delay(500);
    flag = !flag;
    digitalWrite(LED, flag);
    if (WiFi.smartConfigDone()){
      WiFi.setAutoConnect(true);  // 设置自动连接
      digitalWrite(LED, HIGH);
      delay(2000);
      break;
    }
  }
}

bool autoConfig(){
  WiFi.mode(WIFI_STA);     //设置esp8266 工作模式
  WiFi.begin();
  delay(1000);//刚启动模块的话 延时稳定一下
  for(int i=0;i<20;i++){
    if (WiFi.status() == WL_CONNECTED){
       return true;
    }else{
     delay(1000);
     flag = !flag;
     digitalWrite(LED, flag);
    } 
  }
  return false;
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(clientID, username, password)) {
      //client.subscribe("$creq");
    } else {
      delay(5000);
    }
  }
}

void senddata() {
  node.readCoils(0x1480, 8);
  const size_t bufferSize = 8*JSON_ARRAY_SIZE(1) + JSON_ARRAY_SIZE(8) + 9*JSON_OBJECT_SIZE(1) + 8*JSON_OBJECT_SIZE(2);
  DynamicJsonBuffer jsonBuffer(bufferSize);

  JsonObject& root = jsonBuffer.createObject();

  JsonArray& datastreams = root.createNestedArray("datastreams");

  JsonObject& datastreams_0 = datastreams.createNestedObject();
  datastreams_0["id"] = "c81";

  JsonArray& datastreams_0_datapoints = datastreams_0.createNestedArray("datapoints");
  JsonObject& datastreams_0_datapoints_0 = datastreams_0_datapoints.createNestedObject();
  datastreams_0_datapoints_0["value"] = 1+(node.getResponseBuffer(0)&0x01)*10;

  JsonObject& datastreams_1 = datastreams.createNestedObject();
  datastreams_1["id"] = "c82";

  JsonArray& datastreams_1_datapoints = datastreams_1.createNestedArray("datapoints");
  JsonObject& datastreams_1_datapoints_0 = datastreams_1_datapoints.createNestedObject();
  datastreams_1_datapoints_0["value"] = 2+((node.getResponseBuffer(0)&0x02)>>1)*10;

  JsonObject& datastreams_2 = datastreams.createNestedObject();
  datastreams_2["id"] = "c83";

  JsonArray& datastreams_2_datapoints = datastreams_2.createNestedArray("datapoints");
  JsonObject& datastreams_2_datapoints_0 = datastreams_2_datapoints.createNestedObject();
  datastreams_2_datapoints_0["value"] =3+((node.getResponseBuffer(0)&0x04)>>2)*10;

  JsonObject& datastreams_3 = datastreams.createNestedObject();
  datastreams_3["id"] = "c84";

  JsonArray& datastreams_3_datapoints = datastreams_3.createNestedArray("datapoints");
  JsonObject& datastreams_3_datapoints_0 = datastreams_3_datapoints.createNestedObject();
  datastreams_3_datapoints_0["value"] = 4+((node.getResponseBuffer(0)&0x08)>>3)*10;

  JsonObject& datastreams_4 = datastreams.createNestedObject();
  datastreams_4["id"] = "c85";

  JsonArray& datastreams_4_datapoints = datastreams_4.createNestedArray("datapoints");
  JsonObject& datastreams_4_datapoints_0 = datastreams_4_datapoints.createNestedObject();
  datastreams_4_datapoints_0["value"] = 5+((node.getResponseBuffer(0)&0x10)>>4)*10;

  JsonObject& datastreams_5 = datastreams.createNestedObject();
  datastreams_5["id"] = "c86";

  JsonArray& datastreams_5_datapoints = datastreams_5.createNestedArray("datapoints");
  JsonObject& datastreams_5_datapoints_0 = datastreams_5_datapoints.createNestedObject();
  datastreams_5_datapoints_0["value"] =6+((node.getResponseBuffer(0)&0x20)>>5)*10;

  JsonObject& datastreams_6 = datastreams.createNestedObject();
  datastreams_6["id"] = "c87";

  JsonArray& datastreams_6_datapoints = datastreams_6.createNestedArray("datapoints");
  JsonObject& datastreams_6_datapoints_0 = datastreams_6_datapoints.createNestedObject();
  datastreams_6_datapoints_0["value"] =7+((node.getResponseBuffer(0)&0x40)>6)*10;

  JsonObject& datastreams_7 = datastreams.createNestedObject();
  datastreams_7["id"] = "c88";

  JsonArray& datastreams_7_datapoints = datastreams_7.createNestedArray("datapoints");
  JsonObject& datastreams_7_datapoints_0 = datastreams_7_datapoints.createNestedObject();
  datastreams_7_datapoints_0["value"] =8+((node.getResponseBuffer(0)&0x80)>7)*10;
  
  char t_json[root.measureLength() + 1];
  root.printTo(t_json, sizeof(t_json));
  
  int payload_len = 3 + sizeof(t_json)/sizeof(char)-1;
  char t_payload[payload_len+1];
    //type
  t_payload[0] =  '\x01';
    //length
  unsigned short json_len = sizeof(t_json)/sizeof(char)-1;
  t_payload[1] = json_len >> 8;
  t_payload[2] = (json_len) & 0xFF;
  memcpy(t_payload+3, t_json, json_len); 
  client.connect(clientID, username, password);
  client.publish_P("$dp",(const uint8_t*)t_payload,payload_len,false);
  node.clearResponseBuffer(); 
}

void callback(char* topic, byte* payload, unsigned int length) {
 if(length==2){
    switch ((char)payload[1]){
    case '1':
          node.writeSingleCoil(0x1480, 1);
          break;
    case '2':
          node.writeSingleCoil(0x1481, 1);
          break;
    case '3':
          node.writeSingleCoil(0x1482, 1);
          break;
    case '4':
          node.writeSingleCoil(0x1483, 1);
          break;
    case '5':
          node.writeSingleCoil(0x1484, 1);
          break;
    case '6':
          node.writeSingleCoil(0x1485, 1);
          break;
    case '7':
          node.writeSingleCoil(0x1486, 1);
          break;
    case '8':
          node.writeSingleCoil(0x1487, 1);
          break;
      }
  }
  else { 
    switch ((char)payload[0]){
    case '1':
          node.writeSingleCoil(0x1480, 0);
          break;
    case '2':
          node.writeSingleCoil(0x1481, 0);
          break;
    case '3':
          node.writeSingleCoil(0x1482, 0);
          break;
    case '4':
          node.writeSingleCoil(0x1483, 0);
          break;
    case '5':
          node.writeSingleCoil(0x1484, 0);
          break;
    case '6':
          node.writeSingleCoil(0x1485, 0);
          break;
    case '7':
          node.writeSingleCoil(0x1486, 0);
          break;
    case '8':
          node.writeSingleCoil(0x1487, 0);
          break;
      }
  }
  senddata() ;
}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  long now = millis();
  if (now - lastMsg > 5000) {
  lastMsg = now;
  senddata();
  flag = !flag;
  digitalWrite(LED, flag);
  }
  int D3_Value=digitalRead(D3);
  if(D3_Value==LOW){
     smartConfig(); 
   }
}
