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
    msg=String(node.getResponseBuffer(0));
    String (node.getResponseBuffer(0)).toCharArray(msg_buff,10); 
    client.publish("outTopic", msg_buff);
    node.clearResponseBuffer();  
  }
}
