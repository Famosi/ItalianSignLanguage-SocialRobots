# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import sys
sys.path.append('../../')

import json
from collections import OrderedDict
from random import randint
import utils as path
from controller import Robot, Keyboard, Motion
from sign import Sign
from error import Error
from utils import get_rest_position, signs_are_similar


class Nao(Robot):
    PHALANX_MAX = 8

    def printHelp(self):
        print('----------NAO_ROBOT-ISL----------')
        print('Use the keyboard to control the robots (one at a time)')
        print('(The 3D window need to be focused)')
        print('[A]: Amare')
        print('[C]: Conoscere')
        print('[D]: Dimenticare')
        print('[F]: Fidarsi')
        print('[I]: Invidia')
        print('[G]: Gelosia')
        print('[P]: Pensare')
        print('[Q]: Arrabbiarsi')
        print('[R]: Ricordare')
        print('[W]: Ragionare')
        print('[H]: print this help message')
        print('--------------')

    def findAndEnableDevices(self):
        # get the time step of the current world.
        self.timeStep = int(self.getBasicTimeStep())

        # there are 7 controlable LED groups in Webots
        self.leds = []
        self.leds.append(self.getLED('ChestBoard/Led'))
        self.leds.append(self.getLED('RFoot/Led'))
        self.leds.append(self.getLED('LFoot/Led'))
        self.leds.append(self.getLED('Face/Led/Right'))
        self.leds.append(self.getLED('Face/Led/Left'))
        self.leds.append(self.getLED('Ears/Led/Right'))
        self.leds.append(self.getLED('Ears/Led/Left'))

        # get phalanx motor tags
        # the real Nao has only 2 motors for RHand/LHand
        # but in Webots we must implement RHand/LHand with 2x8 motors
        self.lphalanx = []
        self.rphalanx = []
        self.maxPhalanxMotorPosition = []
        self.minPhalanxMotorPosition = []
        for i in range(0, self.PHALANX_MAX):
            self.lphalanx.append(self.getMotor("LPhalanx%d" % (i + 1)))
            self.rphalanx.append(self.getMotor("RPhalanx%d" % (i + 1)))

            # assume right and left hands have the same motor position bounds
            self.maxPhalanxMotorPosition.append(self.rphalanx[i].getMaxPosition())
            self.minPhalanxMotorPosition.append(self.rphalanx[i].getMinPosition())

        # Shoulder motors
        self.RShoulderPitch = self.getMotor("RShoulderPitch")
        self.LShoulderPitch = self.getMotor("LShoulderPitch")
        self.RShoulderRoll = self.getMotor("RShoulderRoll")
        self.LShoulderRoll = self.getMotor("LShoulderRoll")

        # Elbow motors
        self.LElbowRoll = self.getMotor("LElbowRoll")
        self.RElbowRoll = self.getMotor("RElbowRoll")
        self.LElbowYaw = self.getMotor("LElbowYaw")
        self.RElbowYaw = self.getMotor("RElbowYaw")


        # Wirst motors
        self.LWristYaw = self.getMotor("LWristYaw")
        self.RWristYaw = self.getMotor("RWristYaw")

        # keyboard
        self.keyboard = self.getKeyboard()
        self.keyboard.enable(5 * self.timeStep)

    def getCasualSign(self):
        same_location_dict = dict()
        old_sign = self.data.pop(self.old_sign)

        old_locations = [[], []]
        for i in range(0, 2):
            if old_sign[i] is not None:
                old_locations[i].append(old_sign[i]['location'])
            else:
                old_locations[i].append(None)

        casual_sign = [[], []]
        for sign in self.data.keys():
            for i in range(0, 2):
                if self.data[sign][i] is not None:
                    casual_sign[i].append(self.data[sign][i]['location'])
                else:
                    casual_sign[i].append(None)

            if signs_are_similar(casual_sign, old_locations) or signs_are_similar(old_locations, casual_sign):
                same_location_dict[sign] = self.data[sign]

            if casual_sign == old_locations:
                same_location_dict[sign] = self.data[sign]
            casual_sign = [[], []]

        candidate = same_location_dict.keys()

        if len(candidate) == 0:
            self.data[self.old_sign] = old_sign
            return None

        num = randint(0, len(candidate)-1)
        sign_same_location = candidate[num]

        self.data[self.old_sign] = old_sign

        return sign_same_location

    def is_good_defined(self, sign):
        for idx, _ in enumerate(self.data[sign]):
            if self.data[sign][idx] is not None:
                for param in self.data[sign][idx]:
                    if len(self.data[sign][idx]) != self.number_of_params or (not param.startswith("location")
                            and not param.startswith("hand_configuration")
                            and not param.startswith("hand_orientation")
                            and not param.startswith("movement")
                            and not param.startswith("speed")):
                        self.bad_def = True
                        Error().bad_definition()
                        return False
        return True

    def execute_sign(self, sign):
        self.bad_def = False
        # if DX & SX
        data = self.data[sign]
        if self.is_good_defined(sign):
            sign_dx = [None]*6
            sign_dx[3] = [None]
            sign_sx = [None]*6
            sign_sx[3] = [None]
            if data[0] is not None:
                for i in range(0, 5):
                    sign_dx[i] = data[0][self.params[i]]
                    sign_dx[5] = data[0].keys()
            if data[1] is not None:
                for i in range(0, 5):
                    sign_sx[i] = data[1][self.params[i]]
                    sign_sx[5] = data[1].keys()
            print("Performing \"" + sign + "\"...\n")
            Sign(
                self,
                [[sign_dx[0]], [sign_sx[0]]],
                [[sign_dx[1]], [sign_sx[1]]],
                [[sign_dx[2]], [sign_sx[2]]],
                [sign_dx[3], sign_sx[3]],
                [[sign_dx[4]], [sign_sx[4]]],
                [sign_dx[5], sign_sx[5]]
            ).perform_sign()

        if not self.bad_def and self.old_sign is None:
            self.printHelp()

    def __init__(self):
        Robot.__init__(self)
        # initialize stuff
        self.number_of_params = 5
        self.params = ['location', 'hand_configuration', 'hand_orientation', 'movement', 'movement_speed']
        self.findAndEnableDevices()

    def print_interaction(self, sign):
        interaction = {
            "chest": "The sign \"" + sign + "\" refers to an emotional state. Thus, it is performed near the chest",
            "head": "The sign \"" + sign + "\" refers to a mental activity. Thus, it is performed near the head"
        }

        sign = self.data[sign]
        location = None

        if sign[0] is not None:
            location = sign[0]["location"]
        elif sign[1] is not None:
            location = sign[1]["location"]

        if location is not None:
            if "chest" in location:
                print(interaction["chest"])
            elif "head" in location:
                print(interaction["head"])
        print('')
        print(
            "Do you want the robot performs another sign with the same location?"
            "\n[Y]: Yes"
            "\nPress any other defined key to perform the related sign")
        print('--------------\n')

    def run(self):
        self.printHelp()
        get_rest_position(self)

        # Opening JSON file
        f = open(path.path_dictionary)

        # returns JSON object
        # as a order dictionary
        self.data = json.load(f, object_pairs_hook=OrderedDict)

        self.old_sign = None

        # Main loop
        while True:
            try:
                key = self.keyboard.getKey()
                sign = None

                if key == ord('A'):
                    sign = "amare"
                if key == ord('D'):
                    sign = "dimenticare"
                if key == ord('P'):
                    sign = "pensare"
                if key == ord('I'):
                    sign = "invidia"
                if key == ord('C'):
                    sign = "conoscere"
                if key == ord('F'):
                    sign = "fidarsi"
                if key == ord('R'):
                    sign = "ricordare"
                if key == ord('W'):
                    sign = "ragionare"
                if key == ord('Q'):
                    sign = "arrabbiarsi"
                if key == ord('G'):
                    sign = "gelosia"
                """
                if key == ord('NEW_KEY'):
                    sign = "new_sign"
                """
                if key == ord('Y') and self.old_sign is not None:
                    self.bad_def = False
                    sign_same_location = self.getCasualSign()
                    if sign_same_location is not None:
                        self.old_sign = sign_same_location
                        self.execute_sign(sign_same_location)
                        self.print_interaction(sign_same_location)
                    else:
                        print("There aren't other signs with same location!\nTry to add new signs!")

                if key == ord('H'):
                    self.printHelp()
                    sign = None

                if sign is not None:
                    self.old_sign = None
                    self.execute_sign(sign)
                    self.old_sign = sign
                    self.print_interaction(sign)

            except KeyError as e:
                Error().no_verb()

            if robot.step(self.timeStep) == -1:
                # Closing file
                f.close()
                break


# create the Robot instance and run main loop
robot = Nao()
robot.run()
