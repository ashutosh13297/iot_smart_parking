import mqtt_client
import random
import logging as LOG
import parking_slot_model
from datetime import datetime, timedelta
import node_red_client
from queue import Queue

LOG.basicConfig(format='%(asctime)s - %(message)s', level=LOG.INFO)

PUBLISH_TOPIC = "parking_slot/arrival_"
car_queue = Queue()
parking_slot_queue = Queue()
parking_status = {}
MEAN_TIME = 5
PARKING_SLOT_ID = 1 


def update_parking_status(parking_slot, status, car, parking_time):
    if(parking_slot in parking_status):
        slot = parking_status[parking_slot]
        slot.is_available = status
        current_time = datetime.now()
        detarture_time = current_time + timedelta(seconds=parking_time)
        slot.departure_time = detarture_time
        slot.last_car = car


def assignParkingSlot():
    if(car_queue.empty() == True or parking_slot_queue.empty() == True):
        if(car_queue.empty() == True):
            LOG.info("[Service] - No cars available in queue")
        if(parking_slot_queue.empty() == True):
            LOG.info("[Service] - No parking slot is available.")
        return
    if(car_queue.empty() == False and parking_slot_queue.empty() == False):
        LOG.info("[Service] - Assigning parking slot...")
        # Get assignment Details
        car = car_queue.get()
        parking_slot = parking_slot_queue.get()
        parking_time = get_parking_time()
        # Publishing to MQTT broker
        mqtt_client.publish(PUBLISH_TOPIC + parking_slot, parking_time)
        # Update Information
        update_parking_status(parking_slot, False, car, parking_time)
        # Send to node-red client
        node_red_client.send_data_to_node_red(parking_status)

        LOG.info(f"[Service] - Assigned parking slot [{parking_status[parking_slot].slot_id}] to car [{car}], for time : {parking_time} sec")
        LOG.info(f"[Service] - Parking slot available : {list(parking_slot_queue.queue)}")
        LOG.info(f"[Service] - Car's in queue : {list(car_queue.queue)}")

def handle_car(car):
    car_queue.put(car)
    LOG.info(f"[Service] - Car {car} Arrived for parking.")
    LOG.info(f"[Service] - Car's in queue : {list(car_queue.queue)}")
    assignParkingSlot()

def handle_slot_status(message):
    global PARKING_SLOT_ID
    parking_slot_queue.put(message)
    if(message in parking_status):
        parking_slot = parking_status[message]
        parking_slot.is_available = True
    else:
        slot = parking_slot_model.ParkingSlotModel(PARKING_SLOT_ID, True, None, None)
        parking_status[message] = slot
        PARKING_SLOT_ID += 1
    node_red_client.send_data_to_node_red(parking_status)
    assignParkingSlot()

def get_parking_time():
    return int(random.expovariate(1 / MEAN_TIME))