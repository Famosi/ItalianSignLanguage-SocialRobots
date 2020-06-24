from performer import Performer
from error import Error
import os
import utils


class Sign:
    def __init__(self, robot, location, hand_configuration, hand_orientation, movement, movement_speed, param_order):
        self.robot = robot

        self.location = location
        self.location_dx = location[0]
        self.location_sx = location[1]

        self.hand_configuration = hand_configuration
        self.hand_configuration_dx = hand_configuration[0]
        self.hand_configuration_sx = hand_configuration[1]

        self.hand_orientation = hand_orientation
        self.hand_orientation_dx = hand_orientation[0]
        self.hand_orientation_dx = hand_orientation[1]

        self.movement = movement
        self.movement_dx = movement[0]
        self.movement_sx = movement[1]

        self.movement_speed = movement_speed
        self.movement_speed_dx = movement_speed[0]
        self.movement_speed_sx = movement_speed[1]

        self.param_order = param_order
        self.param_order_dx = param_order[0]
        self.param_order_sx = param_order[1]

        self.set_speed()
        self.get_settings()

    def set_speed(self):
        new_lines = []
        for i in range(0, 2):
            if self.movement_speed[i][0] is not None:
                for motion in self.movement[i]:
                    if len(motion) > 0:
                        motion_path = utils.path_movement + motion + utils.r_l[i]
                        new_speeds = get_new_speeds(motion_path, self.movement_speed[i][0])

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

                        new_motion_path = utils.path_movement + motion + utils.r_l[i]
                        with open(new_motion_path, "w+") as new_f:
                            for line, _ in enumerate(new_lines):
                                new_f.writelines(new_lines[line])
                        new_lines = []
                        new_f.close()

    def perform_sign(self):
        settings_dx, settings_sx = self.get_settings()
        for i in range(0, 4):
            Performer(
                self.robot,
                [[settings_dx[i][0]], [settings_sx[i][0]]],
                [settings_dx[i][1], settings_sx[i][1]],
                [settings_dx[i][2], settings_sx[i][2]],
            )
        utils.rest_position(self.robot)

    def get_settings(self):
        settings = [[], []]
        for i in range(0, 2):
            if self.param_order[i] is not None:
                for idx, param in enumerate(self.param_order[i]):
                    if param == "hand_configuration":
                        settings[i].append(["Hand Configuration", utils.path_hand_configuration, self.hand_configuration[i]])
                    if param == "location":
                        settings[i].append(["Location", utils.path_location, self.location[i]])
                    if param == "hand_orientation":
                        settings[i].append(["Hand Orientation", utils.path_hand_orientation, self.hand_orientation[i]])
                    if param == "movement":
                        settings[i].append(["Movement", utils.path_movement, self.movement[i]])
            else:
                for _ in range(0, 4):
                    settings[i].append([None, None, [None]])
        return settings[0], settings[1]


def get_new_speeds(path, speed):
    num_lines = sum(1 for _ in open(path))
    speed = int(speed * 1000)
    if speed < 100:
        Error().bad_time_definition()
        return None
    else:
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
