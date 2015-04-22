import lights


class Program:
    def __init__(self, allLights):
        self.allLights = allLights

    def buttonPressed(self, n):
        print "Error, this function should be overridden!"

    def reset(self):
        pass

    def dark(self):
        for name, l in self.allLights.items():
            l['light'].setController(
                lights.ConstantRGBController(0, 0, 0))

    def light(self):
        for name, l in self.allLights.items():
            l['light'].setController(
                lights.ConstantRGBController(255, 255, 255))

    def setLights(self, lightList, controllerFunc):
        for l in lightList:
            self.allLights[l]['light'].setController(
                controllerFunc())

    def setLightsExcept(self, lightExceptList, controllerFunc):
        for name, l in self.allLights.items():
            if not name in lightExceptList:
                l['light'].setController(controllerFunc())
