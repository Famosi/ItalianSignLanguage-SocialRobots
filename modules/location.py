"""
 - shoulderPitch
 - shoulderRoll
 - elbowYaw
 - elbowRoll
"""

from controller import Robot, Keyboard, Motion
from time import sleep
import sys
sys.path.append('../../')
from utils import path_motions_location


class Location:
    def __init__(self, robot, location, l_r):
        self.robot = robot
        self.location = location
        self.l_r = l_r
        self.motion = Motion(path_motions_location + self.location + '_' + self.l_r + '.motion')
        self.set_location()

    def set_location(self):
        self.motion.play()
        while not self.motion.isOver():
            self.robot.step(self.robot.timeStep)


