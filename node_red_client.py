import socket
import json
import logging as LOG
import parking_slot_model

node_red_port = 7777
node_red_host = "192.168.205.222"

node_red_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

LOG.basicConfig(format='%(asctime)s - %(message)s', level=LOG.INFO)

def serialize_parking_slot(obj):
    if isinstance(obj, parking_slot_model.ParkingSlotModel):
        return {
            'slot_id': obj.slot_id,
            'is_available': obj.is_available,
            'last_car': obj.last_car,
            'departure_time': obj.departure_time.strftime('%Y-%m-%d %H:%M:%S') if obj.departure_time else None,
        }

def send_data_to_node_red(data):
    res = {}
    for key in data:
        res[data[key].slot_id] = data[key]
    sorted_dict = {k: res[k] for k in sorted(res)}
    json_data = json.dumps(sorted_dict, default=serialize_parking_slot)
    LOG.info(f"[Node-Red Client] - Sending data to node-red client : {json_data}")
    # LOG.info(f"Json Data : {json_data}")
    node_red_socket.sendto(json_data.encode(), (node_red_host, node_red_port))