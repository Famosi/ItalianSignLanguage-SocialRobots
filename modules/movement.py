from controller import Robot, Keyboard, Motion
import sys
sys.path.append('../')
from utils import path_motions_movement


class Movement:
    def __init__(self, robot, configurations, l_r):
        self.robot = robot
        self.configurations = configurations
        self.l_r = l_r
        self.motions = self.get_motions()
        self.rest_position = Motion(path_motions_movement + 'rest_position.motion')
        self.set_movement()

    def get_motions(self):
        motions = []
        for configuration in self.configurations:
            motions.append(
                Motion(path_motions_movement + configuration + '.motion')
            )
        return motions

    def set_movement(self):
        for _ in range(4):
            for motion in self.motions:
                self.play_movement(motion)
        self.play_movement(self.rest_position)

    def play_movement(self, motion):
        motion.play()
        while not motion.isOver():
            self.robot.step(self.robot.timeStep)



