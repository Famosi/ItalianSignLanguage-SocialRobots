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
            settings = where(self,param)
            Performer(settings[0], settings[1], self.robot, settings[2], self.configuration, self.l_r)
            self.rest_position()

    def where(self,s):
        var = []
        if s == "configuration":
            return ["Configuration",path.path_motions_configuration,"static"]
        elif s == "location":
            return ["Location", path.path_motions_configuration, "static"]
        elif s == "orientation":
            return ["Orientation", path.path_motions_configuration, "static"]
        elif s == "movement":
            return ["Movement", path.path_motions_configuration, "dynamic"]
        # errore se var è vuoto
        return ["Errore","ERRORE","Errore"]

