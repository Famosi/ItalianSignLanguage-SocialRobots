# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of Python controller for Nao robot.
   This demonstrates how to access sensors and actuators"""
import sys
sys.path.append('../../')

import json
from collections import OrderedDict
from random import seed
from random import randint
import utils as path
from controller import Robot, Keyboard, Motion
from sign import Sign
from error import Error
from time import sleep


class Nao(Robot):
    PHALANX_MAX = 8

    def setAllLedsColor(self, rgb):
        # these leds take RGB values
        for i in range(0, len(self.leds)):
            self.leds[i].set(rgb)

        # ear leds are single color (blue)
        # and take values between 0 - 255
        self.leds[5].set(rgb & 0xFF)
        self.leds[6].set(rgb & 0xFF)

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
        print('--------------')
        print('[H]: print this help message')

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
        sign = self.data[self.old_sign]
        # togliere da data sign
        toAdd = self.data.pop(self.signName)
        final = dict()
        l_r = False
        # creo location per dx&sx
        if sign[0] is not None and sign[1] is not None:
            l_r = True
            location = [sign[0]["location"], sign[1]["location"]]
        # creo location per dx
        elif sign[0] is not None:
            location = [sign[0]["location"]]
        # creo location per sx
        else:
            location = [sign[1]["location"]]

        for el in self.data.keys():
            # per dx & sx
            if self.data[el][0] is not None and self.data[el][1] is not None and l_r:
                if self.data[el][0]["location"] == location[0] and self.data[el][1]["location"] == location[1]:
                    final[el] = self.data[el]
            # per dx
            elif self.data[el][0] is not None:
                if self.data[el][0]["location"] == location[0]:
                    final[el] = self.data[el]
            # per sx
            elif self.data[el][1] is not None:
                if self.data[el][1]["location"] == location[1]:
                    final[el] = self.data[el]

        # scelgo un numero casuale fra 0 e lunghezza final.keys()
        # prendo elemento corrsipondente nella lista
        # nel caso eseguo l'elemeto nella lista
        candidate = final.keys()
        if len(candidate) == 0:
            self.data[self.signName] = toAdd
            return

        num = randint(0, len(candidate)-1)
        input = candidate[num]

        self.data[self.signName] = toAdd

        return input

    def execute_sign(self, data):
        # if DX & SX
        if data[0] is not None and data[1] is not None:
            dx = data[0]
            sx = data[1]
            # contollare se dx e sx hanno lo stesso ordine
            Sign(
                self,
                'L_R',
                [dx['location'], sx['location']],
                [dx['hand_configuration'], sx['hand_configuration']],
                [dx['hand_orientation'], sx['hand_orientation']],
                [dx['movement'], sx['movement']],
                dx.keys()
            ).perform_sign()
        # if DX
        elif data[0] is not None:
            dx = data[0]
            Sign(
                self,
                'R',
                [dx['location']],
                [dx['hand_configuration']],
                [dx['hand_orientation']],
                dx['movement'],
                dx.keys()
            ).perform_sign()
        # if SX
        elif data[1] is not None:
            sx = data[1]
            Sign(
                self,
                'L',
                [sx['location']],
                [sx['hand_configuration']],
                [sx['hand_orientation']],
                sx['movement'],
                sx.keys()
            ).perform_sign()

    def __init__(self):
        Robot.__init__(self)
        # initialize stuff
        self.findAndEnableDevices()

    def run(self):
        self.printHelp()

        # Opening JSON file
        f = open(path.path_dictionary)

        # returns JSON object
        # as a order dictionary
        self.data = json.load(f,object_pairs_hook=OrderedDict)

        self.old_sign = None

        # Main loop
        while True:
            key = self.keyboard.getKey()
            sign = None
            try:
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
                    input = "new_sign"
                    self.execute_sign(data[input])
                """
                if key == ord('Y') and self.old_sign is not None:
                    second = self.getCasualSign()
                    self.old_sign = None
                    self.execute_sign(self.data[second])
                    self.printHelp()

                if key == ord('H'):
                    self.printHelp()
                    sign = None

                if sign is not None:
                    self.execute_sign(self.data[sign])
                    self.old_sign = sign
                    print("Press \"y\" for another sign with the same location")

            except KeyError:
                Error().no_verb()

            if robot.step(self.timeStep) == -1:
                # Closing file
                f.close()
                break


# create the Robot instance and run main loop
robot = Nao()
robot.run()
