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
        if self.l_r == "L_R":
            motions_dx = []
            motions_sx = []
            for configuration in self.configurations[0]:
                motions_dx.append(
                    Motion(path_motions_movement + configuration + '_R' + '.motion')
                )
            for configuration in self.configurations[1]:
                motions_sx.append(
                    Motion(path_motions_movement + configuration + '_L' + '.motion')
                )
            return [motions_dx, motions_sx]
        else:
            motions = []
            for configuration in self.configurations[0]:
                motions.append(
                    Motion(path_motions_movement + configuration + '_' + self.l_r + '.motion')
                )
            return [motions]

    def set_movement(self):
        if self.l_r == "L_R":
            for _ in range(3):
                for motion_dx in self.motions[0]:
                    motion_dx.play()
                    while not motion_dx.isOver():
                        for motion_sx in self.motions[1]:
                            motion_sx.play()
                            while not motion_sx.isOver():
                                self.robot.step(self.robot.timeStep)
                        self.robot.step(self.robot.timeStep)
            self.play_movement(self.rest_position)
        else:
            for _ in range(3):
                for motion in self.motions[0]:
                    self.play_movement(motion)
        self.play_movement(self.rest_position)

    def play_movement(self, motion):
        motion.play()
        while not motion.isOver():
            self.robot.step(self.robot.timeStep)



