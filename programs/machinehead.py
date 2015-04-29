import common
import lights
import time
import random
import math


class MachineheadProgram(common.Program):
    def reset(self):
        self.firstIntro = True
        self.firstChorus = True
        self.lastn = -1
        self.btnCount = 0
        self.lastBPMUpdate = time.time()
        self.bpm = 113
        self.spb = 60.0 / self.bpm
        self.autoSong = 'mh.mp3'
        self.autoBtns = [
                (0, 0.3),
                (0, 4.94),
                (0, 9.22),
                (0, 13.41),
                (0, 17.67),
                (0, 21.89),
                (0, 26.24),
                (0, 30.33),
                (0, 34.69)
                ]
        """
                (0, 4.67),
                (0, 8.99),
                (0, 13.22),
                (0, 17.53),
                (0, 21.8),
                (0, 25.99),
                (0, 30.33),
                (0, 34.61)
            """

    def updateBPM(self, beats, applyChanges=True):
        if applyChanges:
            self.bpm = 60.0/(time.time() - self.lastBPMUpdate)*beats
        self.lastBPMUpdate = time.time()
        self.spb = 60.0 / self.bpm

    def intro(self, n):
        if not self.firstIntro and n == 1:
            self.updateBPM(8, False)
        else: 
            self.updateBPM(8, True)
	if not self.firstIntro:
            n += 7

        self.setLights(['frontLeftMagic'], lambda: lights.FadeInController(
                        lights.ConstantRGBController(0,0,0), 0.1))

        print "intro with n = " + str(n)
        if n == 1:
            print "fisrt intro"
            self.allLights['backTanner']['light'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(255, 0, 0), 0.5
                ))
            self.allLights['frontTanner']['light'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(255, 255, 255), 0.5
                ))
        if n == 2:
            c = lights.getRGBSequenceController([
                ((255, 255, 255), self.spb*4.0),
                ((255, 0, 0), self.spb*10),
                ((0, 0, 0), 1.0)
            ])
            for name, l in self.allLights.items():
                l['light'].setController(c)
        def bassLights():
            return lights.getRGBSequenceController(
                                [((255,255,255), self.spb*0.5),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*0.5),
                                ((255,0,0), self.spb*0.75),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*0.5),
                                ((255,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*0.25),
                                ((255,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*0.5),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0)
                                ]*2
                            )
        if n > 2 and n < 6:
            self.setLights(['frontSpencer', 'frontLeft', 'backTanner'],
                            lambda: lights.getRGBSequenceController([
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0)
                            ]))
            self.setLights(['frontTanner', 'frontRight', 'backSpencer', 'backDoug'],
                            lambda: lights.getRGBSequenceController([
                                ((255,255,255), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((255,0,0), self.spb*1.0),
                                ((100,0,0), self.spb*0.0),
                                ((255,255,255), self.spb*1.0),
                                ((100,0,0), self.spb*0.0)
                            ]))
        if n >= 6 and n < 10:
            self.setLights(['frontSpencer', 'frontLeft', 'backTanner'],bassLights)
            self.setLights(['frontTanner', 'frontRight', 'backSpencer', 'backDoug'], bassLights)

        if n == 10 or n == 12:
            self.setLights(['frontSpencer', 'backSpencer'],
                            lambda: lights.ConstantRGBController(255,0,0))
            self.setLights(['frontLeft','frontTanner', 'frontRight', 'backTanner'],
                            lambda: lights.ConstantRGBController(0,0,0))
            self.setLights(['backDoug'], bassLights)

        if n == 11 or n == 13:
            self.setLights(['frontSpencer', 'backSpencer'],
                            lambda: lights.ConstantRGBController(0,0,0))
            self.setLights(['frontTanner', 'backTanner'],
                            lambda: lights.ConstantRGBController(255,0,0))
            self.setLights(['frontLeft', 'frontRight','backDoug'], bassLights)

        if n> 2 and n%2 == 1:
            self.setLights(['rear1', 'rear4', 'backTravis'],
                           lambda: lights.getRGBSequenceController([
                               ((255,255,255), self.spb*4.0),
                               ((255,255,0), self.spb*4.0),
                               ((255,0,0), self.spb*2.0),
                           ]))
            self.setLights(['rear2', 'rear3'],
                           lambda: lights.getRGBSequenceController([
                               ((255,255,255), self.spb*4.0),
                               ((255,0,0), self.spb*4.0),
                               ((255,255,0), self.spb*2.0),
                           ]))
        elif n > 2:
            self.setLights(['rear1', 'rear4', 'backTravis'],
                           lambda: lights.getRGBSequenceController([
                               ((255,255,255), self.spb*4.0),
                               ((255,0,0), self.spb*4.0),
                               ((255,255,0), self.spb*2.0),
                           ]))
            self.setLights(['rear2', 'rear3'],
                           lambda: lights.getRGBSequenceController([
                               ((255,255,255), self.spb*4.0),
                               ((255,255,0), self.spb*4.0),
                               ((255,0,0), self.spb*2.0),
                           ]))

    def verse(self, n):
        def redLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(200,255)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(0,70)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(0,70))
                ), 0.1
            )
        self.setLights(['rear1', 'rear4', 'rear2', 'rear3', 'backTravis', 
                        'backSpencer', 'backTanner', 'frontTanner', 'frontLeft',
                        'frontRight', 'backDoug'], redLight)
        self.setLights(['frontSpencer'], lambda: lights.FadeInController(
                        lights.ConstantRGBController(255,255,255), 1.0))


    def chorus(self, n):
        def yellowLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(200,255)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(200,255)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(0,70))
                ), 0.5
            )
        def anyLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(1,4), random.uniform(0,2*math.pi),
                        random.uniform(50,200), random.uniform(0,255)),
                    (random.uniform(1,4), random.uniform(0,2*math.pi),
                        random.uniform(50,200), random.uniform(0,255)),
                    (random.uniform(1,4), random.uniform(0,2*math.pi),
                        random.uniform(50,200), random.uniform(0,255))
                ), 0.4
            )
        if self.firstChorus:
            self.firstChorus = False
            self.setLights(['backTravis', 'backDoug', 'backTanner', 'backSpencer'], 
                        yellowLight)
            self.setLights(['frontSpencer'], lambda: lights.FadeInController(
                            lights.ConstantRGBController(100,100,255), 1.0))
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(128, lights.FadeInController(
                            lights.ConstantRGBController(0,0,255), 1.0)))
            self.setLights(['frontTanner', 'frontLeft', 'frontRight', 'rear1', 
                        'rear2', 'rear3', 'rear4'], lambda: lights.FadeInController(
                            lights.ConstantRGBController(0,0,0), 3.0))
        else: 
            self.setLights(['backTravis', 'backDoug', 'backTanner', 'backSpencer'], 
                        anyLight)
            self.setLights(['frontSpencer'], lambda: lights.FadeInController(
                            lights.ConstantRGBController(255,255,255), 1.0))
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(200,
                            lights.FadeInController(
                            lights.ConstantRGBController(255,255,255), 1.0)))
            self.setLights(['frontTanner', 'frontLeft', 'frontRight', 'rear1', 
                        'rear2', 'rear3', 'rear4'], anyLight)


    def endChorus(self, n):
        def greenLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255)),
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70))
                ), 0.4
            )
        self.setLights(['backTravis', 'backDoug', 'backTanner', 'backSpencer'], 
                    greenLight)
        self.setLights(['frontSpencer'], lambda: lights.FadeInController(
                        lights.ConstantRGBController(255,200,200), 1.0))
        self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(0,
                        lights.FadeInController(
                        lights.ConstantRGBController(0,0,0), 1.0)))
        self.setLights(['frontTanner', 'frontLeft', 'frontRight', 'rear1', 
                    'rear2', 'rear3', 'rear4'], greenLight)

    def outro(self, n):
        self.setLightsExcept(['frontSpencer', 'backSpencer'],lambda: lights.FadeInController(lights.ConstantRGBController(0,0,0), .5))
        if n == 1:
            self.setLights(['frontSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(255,255,255), .5))
            self.setLights(['backSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(255,0,0), .5))
        if n == 2:
            self.setLights(['frontSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(0,0,0), 1.5))
            self.setLights(['backSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(255,0,0), .5))
        if n == 3:
            self.setLights(['frontSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(0,0,0), .5))
            self.setLights(['backSpencer'], lambda: lights.FadeInController(lights.ConstantRGBController(0,0,0), 1.5))

    def buttonPressed(self, n):
        if hasattr(self, 'lastn') and self.lastn == n:
            self.btnCount += 1
        else:
            self.btnCount = 1
        self.lastn = n

        if n != 0:
            self.firstIntro = False

        btnmap = {0: self.intro,
                  1: self.verse,
                  2: self.chorus,
                  3: self.endChorus,
                  4: self.outro}

        btnmap[n](self.btnCount)
