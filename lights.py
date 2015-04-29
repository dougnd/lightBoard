import time, math

def mixColors(c1,c2, fraction):
    return (fraction*c1[0] + (1-fraction)*c2[0],
            fraction*c1[1] + (1-fraction)*c2[1],
            fraction*c1[2] + (1-fraction)*c2[2])

# Light types:
class BasicLight:
    def setController(self, controller):
        controller.setPreviousController(self.controller)
        self.controller = controller

    def setSimWidget(self, w):
        self.simWidget = w

    def clampTuple(self, t, minn=0, maxn=255):
        def clamp(n, minn, maxn):
            return max(min(maxn, n), minn)
        t = list(t)
        for i in range(len(t)):
            t[i] = clamp(t[i], minn, maxn)
        return tuple(t)



class DMXPar(BasicLight):
    def __init__(self, dmxAddr):
        self.addr = dmxAddr
        self.controller = BasicController()
        self.simWidget = None
        self.dmxArray = None

    def update(self):
        color = self.clampTuple(self.controller.getRGB())
        if self.simWidget:
            self.simWidget.configure(bg='#%02x%02x%02x' % color)
            """
            print ("Setting par light (" + str(self.addr) +
                   ") to (r,g,b) = " + str(color))
            """
        if self.dmxArray:
            if (self.addr+3 < len(self.dmxArray)):
                self.dmxArray[self.addr] = int(color[0])
                self.dmxArray[self.addr+1] = int(color[1])
                self.dmxArray[self.addr+2] = int(color[2])


class DMXPar7Ch(DMXPar):
    def update(self):
        color = self.clampTuple(self.controller.getRGB())
        if self.simWidget:
            self.simWidget.configure(bg='#%02x%02x%02x' % color)
        if self.dmxArray:
            if (self.addr+7 < len(self.dmxArray)):
                self.dmxArray[self.addr] = 255 # dimmer
                self.dmxArray[self.addr+1] = 0 # strobe
                self.dmxArray[self.addr+2] = 0 # function
                self.dmxArray[self.addr+3] = 0 # speed
                self.dmxArray[self.addr+4] = int(color[0])
                self.dmxArray[self.addr+5] = int(color[1])
                self.dmxArray[self.addr+6] = int(color[2])

class DMXPar6Ch(DMXPar):
    def update(self):
        color = self.clampTuple(self.controller.getRGB())
        if self.simWidget:
            self.simWidget.configure(bg='#%02x%02x%02x' % color)
        if self.dmxArray:
            if (self.addr+6 < len(self.dmxArray)):
                self.dmxArray[self.addr] = 255 # dimmer
                self.dmxArray[self.addr+1] = int(color[1])
                self.dmxArray[self.addr+2] = int(color[0])
                self.dmxArray[self.addr+3] = int(color[2])
                self.dmxArray[self.addr+4] = 0 # function
                self.dmxArray[self.addr+5] = 0 # speed

class DMXMagic(BasicLight):
    def __init__(self, dmxAddr):
        self.addr = dmxAddr
        self.controller = BasicController()
        self.simWidget = None
        self.dmxArray = None

    def update(self):
        color = self.clampTuple(self.controller.getRGB())
        speed = self.controller.getSpeed()
        if self.simWidget:
            self.simWidget.configure(bg='#%02x%02x%02x' % color)
            """
            print ("Setting magic light (" + str(self.addr) +
                   ") to (r,g,b) = " + str(color) +
                   ", and speed = " + str(speed))
            """
        if self.dmxArray:
            if (self.addr+7 < len(self.dmxArray)):
                self.dmxArray[self.addr] = 255 # dimmer
                self.dmxArray[self.addr+1] = int(color[0])
                self.dmxArray[self.addr+2] = int(color[1])
                self.dmxArray[self.addr+3] = int(color[2])
                self.dmxArray[self.addr+4] = 0 # strobe
                self.dmxArray[self.addr+5] = speed # speed
                self.dmxArray[self.addr+6] = 0 # function


# Controllers:
class BasicController:
    def getRGB(self):
        return (0, 0, 0)

    def getSpeed(self):
        return 0

    def reset(self, t=None):
        pass

    def setPreviousController(self, c):
        pass

class ConstantSpeedController(BasicController):
    def __init__(self, speed, rgbcontroller):
        self.rgbcontroller = rgbcontroller
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def getRGB(self):
        return self.rgbcontroller.getRGB()

class ConstantRGBController(BasicController):
    def __init__(self, r, g, b):
        self.color = (r, g, b)

    def getRGB(self):
        return self.color

class SineRGBController(BasicController):
    def __init__(self, r, g, b):
        # the arguments are tuples of the form:
        #   (omega, phi, amp, off)
        # and to create a sinusoid of the form:
        # amp*sin(omega*t+phi) + off
        self.r = r
        self.g = g
        self.b = b
        self.start_time = time.time()

    def reset(self, t=None):
        if t is None:
            t = time.time()
        self.start_time = t

    def getRGB(self):
        t = time.time() - self.start_time
        r = math.sin(self.r[0]*t + self.r[1])
        g = math.sin(self.g[0]*t + self.g[1])
        b = math.sin(self.b[0]*t + self.b[1])
        r = self.r[2]*r + self.r[3]
        g = self.g[2]*g + self.g[3]
        b = self.b[2]*b + self.b[3]
        return (r,g,b)

class StrobeController(BasicController):
    def __init__(self, period, onColor, offColor):
        self.onColor = onColor
        self.offColor = offColor
        self.period = period
        self.start_time = time.time()

    def reset(self, t=None):
        if t is None:
            t = time.time()
        self.start_time = t

    def getRGB(self):
        t = time.time() - self.start_time
        on = (t%self.period)/self.period < 0.5
        if on:
            return self.onColor
        else:
            return self.offColor

class FadeInController(BasicController):
    def __init__(self, newController, fadeTime):
        self.fadeTime = fadeTime
        self.newController = newController
        self.lastRGB = (0,0,0)
        self.start_time = time.time()

    def setPreviousController(self, c):
        self.lastRGB = c.getRGB()
        self.start_time = time.time()

    def getRGB(self):
        t = time.time() - self.start_time

        if t > self.fadeTime:
            return self.newController.getRGB()
        else:
            return mixColors(self.newController.getRGB(),
                             self.lastRGB,
                             t/self.fadeTime)

class FadeController(BasicController):
    def __init__(self, startColor, endColor, fadeTime):
        self.fadeTime = fadeTime
        self.startColor = startColor
        self.endColor = endColor
        self.start_time = time.time()

    def reset(self, t=None):
        if t is None:
            t = time.time()
        self.start_time = t

    def getRGB(self):
        t = time.time() - self.start_time

        if t > self.fadeTime:
            return self.endColor
        else:
            return mixColors(self.endColor,
                             self.startColor,
                             t/self.fadeTime)

class SequenceController(BasicController):
    def __init__(self, controllers, loop=False):
        self.controllers = controllers
        self.start_time = time.time()
        self.loop = loop
        tm = self.start_time
        for controller, period in self.controllers:
            controller.reset(tm)
            tm+=period

    def reset(self, t=None):
        if t is None:
            t = time.time()
        self.start_time = t
        tm = self.start_time
        for controller, period in self.controllers:
            controller.reset(tm)
            tm+=period

    def getRGB(self):
        t = time.time() - self.start_time
        for controller, period in self.controllers:
            t -= period
            if t < 0:
                return controller.getRGB()
        if self.loop:
            self.reset(time.time())
        return self.controllers[-1][0].getRGB()

def getRGBSequenceController(colors):
    #import ipdb; ipdb.set_trace()
    controllers = []
    for i in range(len(colors)-1):
        controllers.append((
            FadeController(colors[i][0], colors[i+1][0], colors[i][1]),
            colors[i][1]
        ))
    return SequenceController(controllers)

def getChaseControllers(n, onDuration, onColor, offColor):
    controllers = []
    for i in range(n):
        controllers.append(SequenceController([
            (ConstantRGBController(*offColor), i*onDuration),
            (ConstantRGBController(*onColor), onDuration),
            (ConstantRGBController(*offColor), (n-i-1)*onDuration),
            ], True))
    return controllers

