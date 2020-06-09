from performer import Performer
import utils as path
from controller import Robot, Keyboard, Motion


class Sign:
    def __init__(self, robot, l_r, location, configuration, orientation, movement):
        self.robot = robot
        self.l_r = l_r
        self.location = location
        self.configuration = configuration
        self.orientation = orientation
        self.movement = movement

    def perform_sign(self):
        Performer("Configuration", path.path_motions_configuration, self.robot, "static", self.configuration, self.l_r)
        Performer("Location", path.path_motions_location, self.robot, "static", self.location, self.l_r)
        Performer("Orientation", path.path_motions_orientation, self.robot, "static", self.orientation, self.l_r)
        Performer("Movement", path.path_motions_movement, self.robot, "dynamic", self.movement, self.l_r)
        self.rest_position()

    def rest_position(self):
        rest_position = Motion(path.path_motions_movement + 'rest_position.motion')
        rest_position.play()
        while not rest_position.isOver():
            self.robot.step(self.robot.timeStep)


