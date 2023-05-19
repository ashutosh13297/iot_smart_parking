#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>


const char* wifiName = "Ashutosh's Galaxy S20 FE 5G";
const char* wifiKey = "12345678";

//MQTT server credentials
const char* mqtt_server = "192.168.230.222";
const int mqtt_port = 1883;
// const char* mqtt_username = "your_MQTT_username";
// const char* mqtt_password = "your_MQTT_password";
String PARKING_SLOT = "";
const String PUBLISH_TOPIC = "parking_slot/availability";
String SUBSCRIBE_TOPIC = "";
// const String BUSY_SLOT = "1";
// const String FREE_SLOT = "0";
String STARTUP_MSG = "";

int PARKING_TIME = 0;
bool status = true;

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(9600);
  setup_WiFi();
  Serial.println(STARTUP_MSG);
  pinMode(LED_BUILTIN, OUTPUT);
  // Connect to WiFi network

  // Connect to MQTT server
  connectMqttBrocker();
  client.setCallback(callback);
}

void setup_WiFi(){
  WiFi.mode(WIFI_STA);
  String connection_string = "Connecting to wifi network.";
  Serial.print("Connecting to wifi network : ");
  Serial.println(wifiName);
  WiFi.begin(wifiName, wifiKey);
  delay(3000);
  while(WiFi.status() != WL_CONNECTED){
     delay(500);
     Serial.print(".");
  }
  Serial.println();
  Serial.print("WiFi connected: Node IP : ");
  const IPAddress& ipAddress = WiFi.localIP();
  String ipAddr = String(ipAddress[0]) + String(".") + String(ipAddress[1]) + String(".") + String(ipAddress[2]) + String(".") + String(ipAddress[3]);
  PARKING_SLOT = ipAddr;
  SUBSCRIBE_TOPIC = "parking_slot/arrival_" + PARKING_SLOT;
  STARTUP_MSG = "NodeMCU Parking Slot : " + PARKING_SLOT;
  Serial.println(ipAddr);
  Serial.println();
}

void connectMqttBrocker() {
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT server...");
    // client.connect("NodeMCU Praking Slot 1", mqtt_username, mqtt_password)) {
    if (client.connect(STARTUP_MSG.c_str())) {
      Serial.println("Connected to MQTT server");
      client.subscribe(SUBSCRIBE_TOPIC.c_str());
      Serial.print("Subscribed to topic : [");
      Serial.print(SUBSCRIBE_TOPIC);
      Serial.println("]");
    } else {
      delay(1000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String receivedMsg;
  for (int i = 0; i < length; i++) {
    receivedMsg += (char)payload[i];
    Serial.print((char)payload[i]);
  }
  Serial.println();
  PARKING_TIME = receivedMsg.toInt();
  status = true;
}

void loop() {
  while (!client.connected()) {
    connectMqttBrocker();
  }
  // client.unsubscribe("parking_slot/arrival_1");
  if(PARKING_TIME == 0) {
    // Turn on LED to show status as free
    digitalWrite(BUILTIN_LED, LOW);
    if(status) {
      status = false;
      publishMessage(PUBLISH_TOPIC, true);
    }
    while (client.loop() != 1) {
      delay(300);
    }
  } else {
    PARKING_TIME--;
    Serial.println(PARKING_TIME);
    // publishMessage(PUBLISH_TOPIC, BUSY_SLOT, true);
    // Turn off LED to show status as busy
    digitalWrite(BUILTIN_LED, HIGH);
  }
  delay(1000);
}

void publishMessage(String topic, boolean retained) {
  String payload = getMsgToPublish();
  Serial.print("Publishing to topic : [");
  Serial.print(topic);
  Serial.print("], Message : [");
  Serial.print(payload);
  Serial.println("]");
  client.publish(topic.c_str(), payload.c_str(), retained);
}

String getMsgToPublish() {
  return String(PARKING_SLOT);
}