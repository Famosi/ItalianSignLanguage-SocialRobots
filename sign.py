from performer import Performer
import utils as path
from utils import rest_position
from error import Error
from fileinput import FileInput
import os
import datetime
import copy

class Sign:
    def __init__(self, robot, l_r, location, configuration, orientation, movement, speed=None, order=None):
        self.robot = robot
        self.l_r = l_r
        self.location = location
        self.configuration = configuration
        self.orientation = orientation
        self.movement = movement
        self.speed = speed
        self.order = order
        self.set_speed()

    def set_speed(self):
            new_lines = []
            if self.l_r == "L_R":
                self.l_r = "R"
                movement = copy.deepcopy(self.movement)
                self.movement = movement[0]
                self.set_speed()
                self.movement = movement[1]
                self.l_r = "L"
                self.speed = [self.speed[1]]
                self.set_speed()
                self.movement = movement
                self.l_r = "L_R"
            else:
                if self.speed[0] is not None:
                    for motion in self.movement:
                        if len(motion) > 0:
                            motion_path = path.path_motions_movement + motion + '_' + self.l_r + '.motion'
                            new_speeds = get_new_speeds(motion_path, self.speed[0])

                            if new_speeds is None:
                                break

                            with open(motion_path, "r") as old_f:
                                for idx, line in enumerate(old_f):
                                    if idx > 0:
                                        for value in range(0, 9):
                                            if value != 2 and value != 5:
                                                line = line.replace(line[:9], new_speeds[idx-1])
                                        new_lines.append(line)
                                    else:
                                        new_lines.append(line)

                            old_f.close()

                            os.remove(motion_path)

                            new_motion_path = path.path_motions_movement + motion + '_' + self.l_r + '.motion'
                            with open(new_motion_path, "w+") as new_f:
                                for line, _ in enumerate(new_lines):
                                    new_f.writelines(new_lines[line])
                            new_lines = []
                            new_f.close()

    # order solo di dx se ci sono entrambi (chiedere come fare)
    def perform_sign(self):
        for param in self.order:
            settings = self.get_settings(param)
            if settings is None:
                break
            Performer(settings[0], settings[1], self.robot, settings[2], settings[3], self.l_r)
        rest_position(self.robot)

    def get_settings(self, param):
        if param == "hand_configuration":
            return ["Configuration", path.path_motions_configuration, "static", self.configuration]
        if param == "location":
            return ["Location", path.path_motions_location, "static", self.location]
        if param == "hand_orientation":
            return ["Orientation", path.path_motions_orientation, "static", self.orientation]
        if param == "movement":
            return ["Movement", path.path_motions_movement, "dynamic", self.movement]
        if param == "speed":
            return None
        # Handle error!!!!
        # Error().bad_definition()
        return None


def get_new_speeds(path, speed):
    num_lines = sum(1 for _ in open(path))
    #TODO:verifica troppo piccolo speed*1000< 1
    speed = int(speed * 1000)
    interval_lenght = (speed / (num_lines - 1))
    i = 0
    new_speeds = ["00:00:000"]
    for _ in range(0, num_lines-1):
        i += interval_lenght
        if i < 10:
            new_speeds.append("00:00:00" + str(i))
        elif i < 100:
            new_speeds.append("00:00:0" + str(i))
        elif i < 1000:
            new_speeds.append("00:00:" + str(i))
        elif i < 10000:
            new_speeds.append("00:0" + str(i)[0] + ":" + str(i)[1:])
        elif i < 100000:
            new_speeds.append("00:" + str(i)[:2] + ":" + str(i)[2:])
        elif i < 1000000:
            new_speeds.append("0" + str(i)[0] + ":" + str(i)[1:3] + ":" + str(i)[3:])
        elif i < 10000000:
            new_speeds.append(str(i)[:2] + ":" + str(i)[2:4] + ":" + str(i)[4:])
        else:
            Error().bad_time_definition()
            return None
    return new_speeds




