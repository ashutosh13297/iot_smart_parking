import socket
import random
import time
import logging as LOG

LOG.basicConfig(format='%(asctime)s [Traffic Generator] - %(message)s', level=LOG.INFO)

# Car arrival following uniform distribution
def generate_car_arrival_rate(min_rate, max_rate):
    return random.uniform(min_rate, max_rate)

host = 'localhost'
port = 8888

min_rate = 5  # Minimum arrival rate in cars per minute
max_rate = 10  # Maximum arrival rate in cars per minute

car_id = 1
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = (host, port)

# Connect to the server
client_socket.connect(server_address)
LOG.info("Connected to server.")

while True:
    try:
        # Generate a random value from the exponential distribution
        wait_time = generate_car_arrival_rate(min_rate, max_rate)
        LOG.info("Next car comming in : " + str(wait_time))
        time.sleep(wait_time)
        LOG.info("Sending car id : " + str(car_id))
        client_socket.send(str(car_id).encode())
        car_id += 1
    except:
        LOG.info("Connection Failed. Exiting...")
        break