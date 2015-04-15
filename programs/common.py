import lights


class Program:
    def __init__(self, allLights):
        self.allLights = allLights

    def buttonPressed(self, n):
        print "Error, this function should be overridden!"

    def dark(self):
        for name, l in self.allLights.items():
            l['light'].setController(
                lights.ConstantRGBController(0, 0, 0))

    def light(self):
        for name, l in self.allLights.items():
            l['light'].setController(
                lights.ConstantRGBController(255, 255, 255))
