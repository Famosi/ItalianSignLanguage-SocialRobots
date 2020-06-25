from os.path import exists
from controller import Motion
import utils


class Performer:
    def __init__(self, robot, module_name, path_module, module_value):
        self.robot = robot

        # [[module_name_dx], [module_name_sx]]
        self.module_name = module_name
        self.module_name_dx = module_name[0]
        self.module_name_sx = module_name[1]

        # [[path_dx], [[path_sx]]
        self.path_module = path_module
        self.path_module_dx = path_module[0]
        self.path_module_sx = path_module[1]

        # [[module_value_dx], [module_value_sx]]
        self.module_value = module_value
        self.module_value_dx = module_value[0]
        self.module_value_sx = module_value[1]

        # [[Motions_dx, ...], [Motions_sx, ...]]
        self.motions = self.get_motions()

        self.perform()

    def get_motions(self):
        # RETURN: [[motion_dx, ...], [motion_sx, ..]]
        motions = [[], []]
        for i in range(0, 2):
            # if this side exists:
            if self.module_name[i][0] is not None:
                for idx, module_value in enumerate(self.module_value[i]):
                    if module_value is not None:
                        motion_path = self.path_module[i] + module_value + utils.r_l[i]
                        if exists(motion_path):
                            motions[i].append(Motion(motion_path))
                    else:
                        motions[i].append(None)
            else:
                motions[i].append(None)
        return motions

    def perform(self):
        for _ in range(3):
            for motion_dx in self.motions[0]:
                if motion_dx is not None:
                    motion_dx.play()
                    while not motion_dx.isOver():
                        for motion_sx in self.motions[1]:
                            if motion_sx is not None:
                                motion_sx.play()
                                while not motion_sx.isOver():
                                    self.robot.step(self.robot.timeStep)
                        self.robot.step(self.robot.timeStep)
                else:
                    for motion_sx in self.motions[1]:
                        if motion_sx is not None:
                            motion_sx.play()
                            while not motion_sx.isOver():
                                self.robot.step(self.robot.timeStep)
