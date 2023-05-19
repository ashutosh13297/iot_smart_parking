import threading
import mqtt_client as mqtt
import car_client
import logging

# Configure the logging module with the desired format
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Create a logger instance
logger = logging.getLogger()

# Start the MQTT client in a separate thread
logger.info('[Server] - Starting MQTT Thread.')
mqtt_thread = threading.Thread(target=mqtt.run)
mqtt_thread.start()

logger.info('[Server] - Starting Server Thread.')
server_socket = car_client.startServer()
car_client.listenAndReceiveMsg(server_socket)
