
"""
Paths Declaration
"""
# local_path = '/Volumes/Extra/'
local_path = '/Users/Famosi/Desktop/'
path_motions_location = local_path +'SocialRobot-ISL/motions/location/'
path_motions_movement = local_path +'SocialRobot-ISL/motions/movement/'
path_motions_configuration = local_path +'SocialRobot-ISL/motions/configuration/'
path_dictionary = local_path +'SocialRobot-ISL/sign_dictionary.json'


"""
Utilities for modules
"""


from controller import Robot, Keyboard, Motion


def get_motions(path, l_r, module):
    if l_r == "L_R":
        return [
            Motion(path + module[0] + '_R' + '.motion'),
            Motion(path + module[1] + '_L' + '.motion')
        ]
    else:
        return [Motion(path + module[0] + '_' + l_r + '.motion')]


def perform_module(motion, l_r, robot):
    if l_r == "L_R":
        motion[0].play()
        while not motion[0].isOver():
            motion[1].play()
            while not motion[1].isOver():
                motion[1].play()
                robot.step(robot.timeStep)
            robot.step(robot.timeStep)
    else:
        motion[0].play()
        while not motion[0].isOver():
            robot.step(robot.timeStep)
