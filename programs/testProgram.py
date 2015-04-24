import lights, math, common

class TestProgram(common.Program):
    def cycle(self):
        for name, l in self.allLights.items():
            l['light'].setController(lights.SineRGBController(
                (1,0, 127, 127),
                (1,2.0*math.pi/3.0, 127, 127),
                (1,4.0*math.pi/3.0, 127, 127)))

    def cycle2(self):
        for name, l in self.allLights.items():
            l['light'].setController(lights.SineRGBController(
                (1,0, 1e6, 0),
                (1,2.0*math.pi/3.0, 1e6, 0),
                (1,4.0*math.pi/3.0, 1e6, 0)))
    def strobe(self):
        lightNames = ['frontSpencer', 'frontLeft', 'frontLeftMagic']
        n = len(self.allLights)
        controllers = lights.getChaseControllers(n, .25, (255,255,255), (0,0,0))
        i=0
        for name, l in self.allLights.items():
            l['light'].setController(controllers[i])
            i+=1

    def buttonPressed(self, n):
        print 'btn idx ' + str(n) + 'pressed'

        btnmap = {0: self.dark,
                1: self.light,
                2: self.cycle,
                3: self.cycle2,
                4: self.strobe}

        btnmap[n]()
    """
allLights = {}

def setAllLights(al):
    global allLights
    allLights = al
    """



