#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const PROGMEM uint8_t LED_PIN = 2;
unsigned int flag = HIGH;//默认当前灭灯
boolean m_light_state = false; // light is turned off by default

#define MQTT_VERSION MQTT_VERSION_3_1_1
// MQTT: ID, server IP, port, username and password
const PROGMEM char* MQTT_CLIENT_ID = "office_light1";
const PROGMEM char* MQTT_SERVER_IP = "153.37.196.203";
const PROGMEM uint16_t MQTT_SERVER_PORT = 4000;
const PROGMEM char* MQTT_USER = "esp11";
const PROGMEM char* MQTT_PASSWORD = "";

// MQTT: topics
const char* MQTT_LIGHT_STATE_TOPIC = "office/light1/status";
const char* MQTT_LIGHT_COMMAND_TOPIC = "office/light1/switch";

// payloads by default (on/off)
const char* LIGHT_ON = "ON";
const char* LIGHT_OFF = "OFF";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup()   {                
  Serial.begin(115200);
  pinMode(LED_PIN,OUTPUT);
  pinMode(D3,INPUT);
  digitalWrite(LED_PIN, HIGH);
  if(!autoConfig()){
    smartConfig();
    while (WiFi.status() != WL_CONNECTED) {
    //这个函数是wifi连接状态，返回wifi链接状态
       delay(500);
       Serial.print(".");
    }
  }
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());//WiFi.localIP()返回8266获得的ip地址
  delay(3000);
  client.setServer(MQTT_SERVER_IP, MQTT_SERVER_PORT);
  client.setCallback(callback);
}
 
void loop() {
  int D3_Value=digitalRead(D3);
  if(D3_Value==LOW){
     smartConfig(); 
   }
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

/**
* 自动连接20s 超过之后自动进入SmartConfig模式
*/
bool autoConfig(){
  WiFi.mode(WIFI_STA);     //设置esp8266 工作模式
  WiFi.begin();
  delay(2000);//刚启动模块的话 延时稳定一下
  Serial.println("AutoConfiging ......");
  for(int i=0;i<20;i++){
    int wstatus = WiFi.status();
    if (wstatus == WL_CONNECTED){
      Serial.println("AutoConfig Success");
      Serial.print("SSID:");
      Serial.println(WiFi.SSID().c_str());
      Serial.print("PSW:");
      Serial.println(WiFi.psk().c_str());
      return true;
    }else{
      Serial.print(".");
      delay(1000);
      flag = !flag;
      digitalWrite(LED_PIN, flag);
    } 
  }
  Serial.println("AutoConfig Faild!");
  return false;
}
 
/**
* 开启SmartConfig功能
*/
void smartConfig()
{
  WiFi.mode(WIFI_STA);
  delay(2000);
  Serial.println("Wait for Smartconfig");// 等待配网
  WiFi.beginSmartConfig();
  while (1){
    delay(500);
    flag = !flag;
    digitalWrite(LED_PIN, flag);
    if (WiFi.smartConfigDone()){
      //smartconfig配置完毕
      Serial.println("SmartConfig Success");
      Serial.print("SSID:");
      Serial.println(WiFi.SSID().c_str());
      Serial.print("PSW:");
      Serial.println(WiFi.psk().c_str());
      WiFi.setAutoConnect(true);  // 设置自动连接
      digitalWrite(LED_PIN, HIGH);
      delay(2000);
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());//WiFi.localIP()返回8266获得的ip地址
      break;
    }
  }
}

// function called to publish the state of the light (on/off)
void publishLightState() {
  if (m_light_state) {
    client.publish(MQTT_LIGHT_STATE_TOPIC, LIGHT_ON, true);
  } else {
    client.publish(MQTT_LIGHT_STATE_TOPIC, LIGHT_OFF, true);
  }
}

// function called to turn on/off the light
void setLightState() {
  if (m_light_state) {
    digitalWrite(LED_PIN, LOW);
    Serial.println("INFO: Turn light on...");
  } else {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("INFO: Turn light off...");
  }
}

// function called when a MQTT message arrived
void callback(char* p_topic, byte* p_payload, unsigned int p_length) {
  // concat the payload into a string
  String payload;
  for (uint8_t i = 0; i < p_length; i++) {
    payload.concat((char)p_payload[i]);
  }
  
  // handle message topic
  if (String(MQTT_LIGHT_COMMAND_TOPIC).equals(p_topic)) {
    // test if the payload is equal to "ON" or "OFF"
    if (payload.equals(String(LIGHT_ON))) {
      if (m_light_state != true) {
        m_light_state = true;
        setLightState();
        publishLightState();
      }
    } else if (payload.equals(String(LIGHT_OFF))) {
      if (m_light_state != false) {
        m_light_state = false;
        setLightState();
        publishLightState();
      }
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("INFO: Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("INFO: connected");
      // Once connected, publish an announcement...
      publishLightState();
      // ... and resubscribe
      client.subscribe(MQTT_LIGHT_COMMAND_TOPIC);
    } else {
      Serial.print("ERROR: failed, rc=");
      Serial.print(client.state());
      Serial.println("DEBUG: try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
