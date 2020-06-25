"""
Paths Declaration
"""
from controller import Motion


# local_path = '/Volumes/Extra/'
local_path = '/Users/Famosi/Desktop/'
path_location = local_path + 'SocialRobot-ISL/motions/location/'
path_hand_configuration = local_path + 'SocialRobot-ISL/motions/hand_configuration/'
path_hand_orientation = local_path + 'SocialRobot-ISL/motions/hand_orientation/'
path_movement = local_path + 'SocialRobot-ISL/motions/movement/'

path_dictionary = local_path +'SocialRobot-ISL/sign_dictionary.json'

r_l = ["_R.motion", "_L.motion"]


def get_rest_position(robot):
    rest_position = Motion(path_movement + 'rest_position_natural.motion')
    rest_position.play()
    while not rest_position.isOver():
        robot.step(robot.timeStep)


def signs_are_similar(sign_x, sign_y):
    if sign_x[0] is not None and sign_x[1] is not None:
        if sign_x[0] == sign_x[1]:
            if [sign_x[0], [None]] == sign_y or [[None], sign_x[1]] == sign_y:
                return True
    return False
