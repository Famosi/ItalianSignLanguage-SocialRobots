from location import Location


class Sign:
    def __init__(self, robot, l_r, location, configuration, orientation, movement):
        self.robot = robot
        self.l_r = l_r
        self.location = location
        self.configuration = configuration
        self.orientation = orientation
        self.movement = movement
        self.actuators_location = self.get_actuators_location()

    def perform_sign(self):
        Location(self.location, self.actuators_location)
        # Configuration(self.config).setConfiguration()
        # Orientation(self.orientation).setOrientation()
        # Movement(self.mov).setMovement()

    def get_actuators_location(self):
        if self.l_r == 'sx':
            return [1, self.robot.LShoulderRoll, self.robot.LShoulderPitch, self.robot.LElbowRoll, self.robot.LElbowYaw]
        elif self.l_r == 'dx':
            return [-1, self.robot.RShoulderRoll, self.robot.RShoulderPitch, self.robot.RElbowRoll, self.robot.RElbowYaw]




