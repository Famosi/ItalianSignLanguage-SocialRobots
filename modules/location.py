"""
 - shoulderPitch
 - shoulderRoll
 - elbowYaw
 - elbowRoll
"""
import sys
sys.path.append('../../')
from utils import get_angles, definitions_path

path_locations = definitions_path + 'locations.json'


class Location:
    def __init__(self, location, actuators):
        self.location = get_angles(path_locations, location)
        self.actuators = actuators
        self.set_location()

    def set_location(self):
        l_r = self.actuators[0]
        for idx, actuator in enumerate(self.actuators[1:]):
            actuator.setPosition(l_r * self.location[idx])

