import common, math, lights, random


class BasicProgram(common.Program):
    def cycle(self):
        for name, l in self.allLights.items():
            l['light'].setController(lights.SineRGBController(
                (1,0, 1e6, 0),
                (1,2.0*math.pi/3.0, 1e6, 0),
                (1,4.0*math.pi/3.0, 1e6, 0)))

    def blue(self, n):
        def blueLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(0,2), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255))
                ), 0.4
            )
        if n == 1:
            self.setLightsExcept(['frontLeftMagic'], blueLight)
            self.setLights(['frontLeftMagic'], lambda: lights.BasicController())
        if n == 2:
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(150, blueLight()))

    def green(self, n):
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
        if n == 1:
            self.setLightsExcept(['frontLeftMagic'], greenLight)
            self.setLights(['frontLeftMagic'], lambda: lights.BasicController())
        if n == 2:
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(150, greenLight()))

    def red(self, n):
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
        if n == 1:
            self.setLightsExcept(['frontLeftMagic'], redLight)
            self.setLights(['frontLeftMagic'], lambda: lights.BasicController())
        if n == 2:
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(150, redLight()))

    def yellow(self, n):
        def yellowLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(200,255)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(200,255)),
                    (random.uniform(3,6), random.uniform(0,2*math.pi),
                        random.uniform(5,30), random.uniform(0,70))
                ), 0.1
            )
        if n == 1:
            self.setLightsExcept(['frontLeftMagic'], yellowLight)
            self.setLights(['frontLeftMagic'], lambda: lights.BasicController())
        if n == 2:
            self.setLights(['frontLeftMagic'], lambda: lights.ConstantSpeedController(150, yellowLight()))

    def outro(self, n):
        pass

    def test(self):
        self.allLights['frontSpencer']['light'].setController(lights.getRGBSequenceController([
            ((0,0,0), 1.0),
            ((255,0,0), 1.0),
            ((0,255,0), 1.0),
            ((0,255,0), 1.0),
            ((0,0,255), 1.0),
            ((255,0,255), 1.0),
        ]))

    def buttonPressed(self, n):
        if hasattr(self, 'lastn') and self.lastn == n:
            self.btnCount += 1
        else:
            self.btnCount = 1
        self.lastn = n
        print 'btn idx ' + str(n) + 'pressed'

        btnmap = {0: self.blue,
                1: self.red,
                2: self.green,
                3: self.yellow,
                4: self.outro}

        btnmap[n](self.btnCount)
