"""
Paths Declaration
"""
from controller import Motion


#local_path = '/Volumes/Extra/'
local_path = '/Users/Famosi/Desktop/'
path_motions_location = local_path +'SocialRobot-ISL/motions/location/'
path_motions_configuration = local_path +'SocialRobot-ISL/motions/hand_configuration/'
path_motions_orientation = local_path +'SocialRobot-ISL/motions/hand_orientation/'
path_motions_movement = local_path +'SocialRobot-ISL/motions/movement/'
path_dictionary = local_path +'SocialRobot-ISL/sign_dictionary.json'

def rest_position(robot):
    rest_position = Motion(path_motions_movement + 'rest_position.motion')
    rest_position.play()
    while not rest_position.isOver():
        robot.step(robot.timeStep)