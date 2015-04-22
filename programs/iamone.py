import common, math, lights, random, time

class HitController(lights.BasicController):
    def __init__(self, controller):
        self.fadeTime = .6
        self.controller = controller
        self.hits = 3
        self.pre_hit_time = -1e5
        self.hit_time = -1e5

    def setPreviousController(self, c):
        self.controller.setPreviousController(c)

    def preHit(self):
        self.pre_hit_time = time.time()

    def hit(self):
        self.hit_time = time.time()

    def getRGB(self):
        c = self.controller.getRGB()
        period = (self.hit_time - self.pre_hit_time)/12
        period = max(.0001, period)
        t = time.time() - self.hit_time
        dt = t % period
        h = t / period
        if h < self.hits and dt < self.fadeTime:
            return lights.mixColors(c, (255,255,255), dt/self.fadeTime)
        else:
            return c


class IAmOneProgram(common.Program):
    def intro(self, n):
        if n == 1:
            self.dark()
            self.allLights['backSpencer']['light'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(
                        40, 0, 255
                    ), 1.0
                )
            )
        if n == 2:
            self.allLights['backDoug']['light'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(
                        40, 0, 255
                    ), 1.0
                )
            )


    def verse(self, n):
        lightsToEnable = ['backDoug', 'backSpencer', 'backTravis', 'backTanner',
                          'rear1', 'rear2', 'rear3', 'rear4']
        def blueLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255))
                ), 1.4
            )

        if n == 1:
            for name, l in self.allLights.items():
                if name in lightsToEnable:
                    l['light'].setController(HitController(
                        blueLight()))
                else:
                    l['light'].setController(HitController(lights.FadeInController(
                        lights.ConstantRGBController(0,0,0), 1.0)))
        if n == 2:
            self.allLights['frontSpencer']['light'].setController(
                HitController(lights.FadeInController(
                    lights.ConstantRGBController(
                        180, 50, 255
                    ), 1.0
                ))
            )
        if n > 2:
            for name, l in self.allLights.items():
                if n%2 == 1:
                    l['light'].controller.preHit()
                else:
                    l['light'].controller.hit()

    def chorus(self, n):
        def redLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70))
                ), .2
            )
        for name, l in self.allLights.items():
            l['light'].setController(redLight())
            #l['light'].controller.lastRGB = (255,255,255)

        self.allLights['frontSpencer']['light'].setController(
            lights.FadeInController(
                lights.ConstantRGBController(
                    255, 255, 255
                ), .2
            )
        )

    def bridge(self, n):
        def greenLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70))
                ), .2
            )
        for name, l in self.allLights.items():
            l['light'].setController(greenLight())
            #l['light'].controller.lastRGB = (255,255,255)

    def outro(self, n):
        for name, l in self.allLights.items():
            l['light'].setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 2.0
            ))
            l['light'].controller.lastRGB = (255,255,255)


    def buttonPressed(self, n):
        if hasattr(self, 'lastn') and self.lastn == n:
            self.btnCount += 1
        else:
            self.btnCount = 1

        btnmap = {
            0: self.intro,
            1: self.verse,
            2: self.chorus,
            3: self.bridge,
            4: self.outro
        }
        try:
            btnmap[n](self.btnCount)
        except KeyError:
            pass
        self.lastn = n

