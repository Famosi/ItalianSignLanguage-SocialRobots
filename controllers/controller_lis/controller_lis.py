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
sys.path.append('../../modules')
sys.path.append('../../modules/location')

import json
from controller import Robot, Keyboard, Motion
from time import sleep
from location import Location
from sign import Sign


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

    def setHandsAngle(self, angleList):
        # for i in range(0, self.PHALANX_MAX):
        #    clampedAngle = angle
        #    if clampedAngle > self.maxPhalanxMotorPosition[i]:
        #        clampedAngle = self.maxPhalanxMotorPosition[i]
        #   elif clampedAngle < self.minPhalanxMotorPosition[i]:
        #        clampedAngle = self.minPhalanxMotorPosition[i]

        #    if len(self.rphalanx) > i and self.rphalanx[i] is not None:
        #        self.rphalanx[i].setPosition(clampedAngle)
        #    if len(self.lphalanx) > i and self.lphalanx[i] is not None:
        #        self.lphalanx[i].setPosition(clampedAngle)

        # @Simone
        # for i in range(0, self.PHALANX_MAX):
        #     self.lphalanx[i].setPosition(angleList[i])
        pass

    def printHelp(self):
        print('----------nao_demo_python----------')
        print('Use the keyboard to control the robots (one at a time)')
        print('(The 3D window need to be focused)')
        print('[Up][Down]: move one step forward/backwards')
        print('[<-][->]: side step left/right')
        print('[Shift] + [<-][->]: turn left/right')
        print('[U]: print ultrasound sensors')
        print('[A]: print accelerometers')
        print('[G]: print gyros')
        print('[S]: print gps')
        print('[I]: print inertial unit (roll/pitch/yaw)')
        print('[F]: print foot sensors')
        print('[B]: print foot bumpers')
        print('[Home][End]: print scaled top/bottom camera image')
        print('[PageUp][PageDown]: open/close hands')
        print('[7][8][9]: change all leds RGB color')
        print('[0]: turn all leds off')
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
        self.keyboard.enable(10 * self.timeStep)

    def execute_sign(self, data):
        # if DX
        if data[0] is not None:
            dx = data[0]
            Sign(
                self,
                'R',
                dx['location'],
                dx['configuration'],
                dx['orientation'],
                dx['movement']
            ).perform_sign()
        # if SX
        if data[1] is not None:
            sx = data[1]
            Sign(
                self,
                'L',
                sx['location'],
                sx['configuration'],
                sx['orientation'],
                sx['movement']
            ).perform_sign()

    def __init__(self):
        Robot.__init__(self)
        # initialize stuff
        self.findAndEnableDevices()

    def run(self):

        # Opening JSON file
        f = open('/Users/Famosi/Desktop/SocialRobot-ISL/definitions/sign_dictionary.json')

        # returns JSON object
        # as a dictionary
        data = json.load(f)

        # Main loop
        while True:
            key = self.keyboard.getKey()

            if key == ord('M'):
                input = "pensare"
                self.execute_sign(data[input])

            if robot.step(self.timeStep) == -1:
                # Closing file
                f.close()
                break


# create the Robot instance and run main loop
robot = Nao()
robot.run()