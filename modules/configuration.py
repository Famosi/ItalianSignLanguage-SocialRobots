from controller import Robot, Keyboard, Motion
import sys
sys.path.append('../../')
from utils import path_motions_configuration


class Configuration:

    def __init__(self, robot, configuration, l_r):
        self.robot = robot
        self.configuration = configuration
        self.l_r = l_r
        self.motion = self.get_motion()
        self.set_configuration()

    def set_configuration(self):
        if self.l_r == "L_R":
            self.motion[0].play()
            while not self.motion[0].isOver():
                self.motion[1].play()
                while not self.motion[1].isOver():
                    self.motion[1].play()
                    self.robot.step(self.robot.timeStep)
                self.robot.step(self.robot.timeStep)
        else:
            self.motion[0].play()
            while not self.motion[0].isOver():
                self.robot.step(self.robot.timeStep)

    def get_motion(self):
        if self.l_r == "L_R":
            return [
                Motion(path_motions_configuration + self.configuration[0] + '_R' + '.motion'),
                Motion(path_motions_configuration + self.configuration[1] + '_L' + '.motion')
            ]
        else:
            return [Motion(path_motions_configuration + self.configuration[0] + '_' + self.l_r + '.motion')]


