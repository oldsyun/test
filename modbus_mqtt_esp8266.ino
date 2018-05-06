#include <ArduinoJson.h>
#include <ModbusMaster.h> //https://github.com/4-20ma/ModbusMaster
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define DE_RE  15
#define LED 2
// Update these with values suitable for your network.

const char* ssid = "cskgj10";
const char* password = "12369874";
const char* mqtt_server = "153.37.196.203";

WiFiClient espClient;
PubSubClient client(espClient);
ModbusMaster node;
long lastMsg = 0;
int value = 0;
char msg_buff[50];
String msg;
const size_t bufferSize = JSON_ARRAY_SIZE(8) + JSON_OBJECT_SIZE(4);
DynamicJsonBuffer jsonBuffer(bufferSize);


void preTransmission()
{
   digitalWrite(DE_RE, 1);
}

void postTransmission()
{
  digitalWrite(DE_RE, 0);
}

void setup() {
  pinMode(DE_RE, OUTPUT);
  digitalWrite(DE_RE, 0);
  pinMode(LED, OUTPUT);   
  digitalWrite(LED, HIGH);
  Serial.begin(19200,SERIAL_8E1);
  node.begin(1, Serial);
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);
  setup_wifi();
  client.setServer(mqtt_server, 4000);
  client.setCallback(callback);

}

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  if ((char)payload[0] == '1') {
   node.writeSingleCoil(0x1480, 1);
  } else {
    node.writeSingleCoil(0x1480, 0);// Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP8266Client")) {
      //node.readCoils(0x1480, 8);
      client.publish("outTopic", "hello world");
      client.subscribe("inTopic");
    } else {
      delay(5000);
    }
  }
}
void loop() {     
  uint8_t j, result;
  uint16_t data[8];
  
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    node.readCoils(0x1480, 8);

  JsonObject& root = jsonBuffer.createObject();
  
  root["mac"] = "";
  root["status"] = "ok";
  root["time"] = "";
 JsonArray& C8 = root.createNestedArray("C8");
 C8.add(node.getResponseBuffer(0)&0x01);
 C8.add((node.getResponseBuffer(0)&0x02)>>1);
 C8.add((node.getResponseBuffer(0)&0x04)>>2);
 C8.add((node.getResponseBuffer(0)&0x08)>>3);
 C8.add((node.getResponseBuffer(0)&0x10)>>4);
 C8.add((node.getResponseBuffer(0)&0x20)>>5);
 C8.add((node.getResponseBuffer(0)&0x40)>>6);
 C8.add((node.getResponseBuffer(0)&0x80)>>7);
//String (root.toCharArray(msg_buff,50);
 char buffer[root.measureLength() + 1];
 root.printTo(buffer, sizeof(buffer));
 client.publish("outTopic", buffer);
 node.clearResponseBuffer();  
  }
}
