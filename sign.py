from performer import Performer
import utils as path
from controller import Robot, Keyboard, Motion


class Sign:
    def __init__(self, robot, l_r, location, configuration, orientation, movement, order):
        self.robot = robot
        self.l_r = l_r
        self.location = location
        self.configuration = configuration
        self.orientation = orientation
        self.movement = movement
        self.order = order

    def rest_position(self):
        rest_position = Motion(path.path_motions_movement + 'rest_position.motion')
        rest_position.play()
        while not rest_position.isOver():
            self.robot.step(self.robot.timeStep)

    # order solo di dx se ci sono entrambi (chiedere come fare)
    def perform_sign(self):
        for param in self.order:
            settings = self.get_settings(param)
            Performer(settings[0], settings[1], self.robot, settings[2], settings[3], self.l_r)
        self.rest_position()

    def get_settings(self, param):
        if param == "hand_configuration":
            return ["Configuration", path.path_motions_configuration, "static", self.configuration]
        if param == "location":
            return ["Location", path.path_motions_location, "static", self.location]
        if param == "hand_orientation":
            return ["Orientation", path.path_motions_orientation, "static", self.orientation]
        if param == "movement":
            return ["Movement", path.path_motions_movement, "dynamic", self.movement]
        # Handle erroR!!!!
        return ["Errore","ERRORE","Errore"]

