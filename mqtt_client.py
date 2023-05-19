import paho.mqtt.client as mqtt
import service
import logging as LOG

LOG.basicConfig(format='%(asctime)s [MQTT Client] - %(message)s', level=LOG.INFO)

broker_address = "192.168.205.222"
broker_port = 1883
mqtt_topic_aiailable_slots = "parking_slot/availability"

mqtt_client = None

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            LOG.info("[MQTT Client] - Connected to MQTT Broker!")
        else:
            LOG.info("[MQTT Client] - Failed to connect, return code %d\n", rc)
    global mqtt_client
    mqtt_client = mqtt.Client()
    # client.username_pw_set(username, password)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(broker_address, broker_port)
    return mqtt_client

def subscribe():
    def on_message(mqtt_client, userdata, msg):
        LOG.info(f"[MQTT Client] - Record Read [{msg.topic}] : {msg.payload.decode()}")
        service.handle_slot_status(msg.payload.decode())

    mqtt_client.subscribe(mqtt_topic_aiailable_slots)
    mqtt_client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe()
    client.loop_forever()

def publish(topic, message):
    result = mqtt_client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        LOG.info(f"[MQTT Client] - Publishing [{topic}] : {message}")
    else:
        LOG.info(f"[MQTT Client] - Failed to send message to topic {topic}")