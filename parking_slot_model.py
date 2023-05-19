class ParkingSlotModel:
  def __init__(parking_slot, slot_id, is_available, car, departure_time):
    parking_slot.slot_id = slot_id
    parking_slot.is_available = is_available
    parking_slot.last_car = car
    parking_slot.departure_time = departure_time