import sys
from controller import Motion
sys.path.append('../../')


class Module:
    def __init__(self, path_module, robot, s_d, module, l_r):
        self.path = path_module
        self.robot = robot
        self.s_d = s_d
        self.module = module
        self.l_r = l_r
        self.motions = self.get_motions()
        self.perform()

    def get_motions(self):
        if self.s_d == "dynamic":
            return self.get_dynamic_motions()
        else:
            return self.get_static_motions()

    def perform(self):
        if self.s_d == "dynamic":
            self.perform_dynamic()
        else:
            self.perform_static()

    def get_static_motions(self):
        if self.l_r == "L_R":
            return [
                Motion(self.path + self.module[0] + '_R' + '.motion'),
                Motion(self.path + self.module[1] + '_L' + '.motion')
            ]
        else:
            return [Motion(self.path + self.module[0] + '_' + self.l_r + '.motion')]

    def get_dynamic_motions(self):
        if self.l_r == "L_R":
            motions_dx = []
            motions_sx = []
            for motion in self.module[0]:
                motions_dx.append(
                    Motion(self.path + motion + '_R' + '.motion')
                )
            for motion in self.module[1]:
                motions_sx.append(
                    Motion(self.path + motion + '_L' + '.motion')
                )
            return [motions_dx, motions_sx]
        else:
            motions = []
            for motion in self.module:
                motions.append(
                    Motion(self.path + motion + '_' + self.l_r + '.motion')
                )
            return [motions]

    def perform_static(self):
        if self.l_r == "L_R":
            self.motions[0].play()
            while not self.motions[0].isOver():
                self.motions[1].play()
                while not self.motions[1].isOver():
                    self.motions[1].play()
                    self.robot.step(self.robot.timeStep)
                self.robot.step(self.robot.timeStep)
        else:
            self.motions[0].play()
            while not self.motions[0].isOver():
                self.robot.step(self.robot.timeStep)

    def perform_dynamic(self):
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
            self.play(self.rest_position)
        else:
            for _ in range(3):
                for motion in self.motions[0]:
                    self.play(motion)

    def play(self, motion):
        motion.play()
        while not motion.isOver():
            self.robot.step(self.robot.timeStep)

