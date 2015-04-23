import lights
import programs
import sys
import subprocess
import time
import array
#import pkgutil
#import ipdb as pdb
#import time


allLights = {
    'frontSpencer': {
        'light': lights.DMXPar(0),
        'simX': 160,
        'simY': 50
    },
    'frontTanner': {
        'light': lights.DMXPar(3),
        'simX': 210,
        'simY': 50
    },
    'backSpencer': {
        'light': lights.DMXPar(100),
        'simX': 160,
        'simY': 100
    },
    'backTanner': {
        'light': lights.DMXPar(103),
        'simX': 210,
        'simY': 100
    },
    'backDoug': {
        'light': lights.DMXPar(106),
        'simX': 260,
        'simY': 130
    },
    'backTravis': {
        'light': lights.DMXPar(109),
        'simX': 175,
        'simY': 310
    },
    'frontLeftMagic': {
        'light': lights.DMXMagic(12),
        'simX': 50,
        'simY': 10
    },
    'frontLeft': {
        'light': lights.DMXPar(6),
        'simX': 10,
        'simY': 10
    },
    'frontRight': {
        'light': lights.DMXPar(9),
        'simX': 360,
        'simY': 10
    },
    'rear1': {
        'light': lights.DMXPar(112),
        'simX': 100,
        'simY': 340
    },
    'rear2': {
        'light': lights.DMXPar(115),
        'simX': 150,
        'simY': 340
    },
    'rear3': {
        'light': lights.DMXPar(118),
        'simX': 200,
        'simY': 340
    },
    'rear4': {
        'light': lights.DMXPar(121),
        'simX': 250,
        'simY': 340
    },
}


class Master:
    def __init__(self):
        self.allPrograms = programs.programList
        self.currentProgram = None
        self.currentProgramIndex = 0
        self.loadProgram(0)

    def loadProgram(self, index):
        #print 'loading ' + str(self.allPrograms[index])
        self.currentProgramIndex = index
        currentProgramModule = __import__('programs.' +
                                          self.allPrograms[index][1],
                                          fromlist=[
                                              self.allPrograms[index][1]])
        programClass = getattr(currentProgramModule,
                               self.allPrograms[index][2])
        self.currentProgram = programClass(allLights)
        self.currentProgram.reset()
        print "------------------"
        print self.allPrograms[index][0]
        #self.currentProgramModule.setAllLights(allLights)

    def btn(self,number):
        #print "Button " + str(number) + " pressed"
        #testProgram.buttonPressed(number)
        self.currentProgram.buttonPressed(number)

    def nextProgram(self):
        self.loadProgram((self.currentProgramIndex+1)%len(self.allPrograms))

    def prevProgram(self):
        self.loadProgram((self.currentProgramIndex-1)%len(self.allPrograms))

    def darkBtn(self):
        self.currentProgram.reset()
        for name, l in allLights.items():
            l['light'].setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 0.1
            ))

    def frontBtn(self):
        frontLights = ['frontSpencer', 'frontTanner', 'frontLeft', 'frontRight']
        for name, l in allLights.items():
            l['light'].setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 0.1
            ))
        for l in frontLights:
            allLights[l]['light'].setController(lights.FadeInController(
                lights.ConstantRGBController(255,255,255), 0.3
            ))

    def getProgramName(self):
        return self.allPrograms[self.currentProgramIndex][0]


    def runReal(self):
        import Adafruit_BBIO.GPIO as GPIO
        class ButtonHandler:
            def __init__(self, pin, callback):
                self.pin = pin
                self.lastEventTime = 0
                self.debounceTime = .1
                self.callback = callback

            def handler(self, x):
                if GPIO.input(x) and time.time() - self.lastEventTime > self.debounceTime:
                    #print self.pin + ' was pressed!'
                    self.callback()
                self.lastEventTime = time.time()

        def setupPins(pins):
            # build node script to set pin direction:
            mux = 7
            pud = "pulldown"
            script = "var b = require('bonescript');"
            for (p, _) in pins:
                script += " b.pinMode('%s',b.INPUT,%i,'%s','fast');" % (p, mux, pud)
            command = ["node", "-e", script]
            subprocess.call(command, cwd="/usr/local/lib")

            # now use adafruit python lib
            for (p, callback) in pins:
                GPIO.setup(p, GPIO.IN)
                GPIO.add_event_detect(p, GPIO.BOTH)
                GPIO.add_event_callback(p, ButtonHandler(p, callback).handler)


        print "Doing pin initialization..."
        setupPins([
            ("P8_15", self.prevProgram),
            ("P8_16", self.nextProgram),
            ("P8_17", self.frontBtn),
            ("P8_18", self.darkBtn),
            ("P8_9", lambda : self.btn(0)),
            ("P8_10", lambda : self.btn(1)),
            ("P8_11", lambda : self.btn(2)),
            ("P8_12", lambda : self.btn(3)),
            ("P8_14", lambda : self.btn(4))
        ])

        print "Done with pin initialization!"

        from ola.ClientWrapper import ClientWrapper
        self.dmxArray = array.array('B', [0]*100)



        for name, l in allLights.items():
            l['light'].dmxArray = self.dmxArray


        try:
            import usb.core
            import usb.util

# udmx stuff:
            dev = usb.core.find(idVendor=0x16C0, idProduct=0x05DC)

            if dev is None:
                raise ValueError('Device not found')

            udmxSetChannelRange = 2
            bmRequestType = 0x40
            targetFps = 24.0
            t = time.time()

            while True:
                for name, l in allLights.items():
                    l['light'].update()

                dev.ctrl_transfer(bmRequestType, udmxSetChannelRange,
                        len(self.dmxArray), 0, self.dmxArray)

                wait = 1.0/targetFps - time.time()+t
                if wait > 0:
                    time.sleep(wait)
                t = time.time()

        except Exception:
            GPIO.cleanup()
            raise



    def runSim(self):
        import Tkinter
        from Tkinter import Tk, Button, Frame, Label
        root = Tk()
        root.title('lights simulator')

        def onNext():
            self.nextProgram()
            pgmName.configure(text=str(self.currentProgramIndex) + ') ' +
                              self.getProgramName())
            print self.getProgramName()

        def onPrev():
            self.prevProgram()
            pgmName.configure(text=str(self.currentProgramIndex) + ') ' +
                              self.getProgramName())
            print self.getProgramName()

        pgmFrame = Frame(root)
        nxt = Button(pgmFrame, text="next", command=onNext)
        nxt.pack(side=Tkinter.LEFT)
        prev = Button(pgmFrame, text="prev", command=onPrev)
        prev.pack(side=Tkinter.LEFT)
        pgmName = Label(pgmFrame, text=self.getProgramName())
        pgmName.configure(text=str(self.currentProgramIndex) + ') ' +
                              self.getProgramName())
        pgmName.pack(side=Tkinter.LEFT, fill=Tkinter.X)
        pgmFrame.pack(fill=Tkinter.X)

        lightDarkFrame = Frame(root)
        front = Button(lightDarkFrame, text="front", command=lambda: self.frontBtn())
        front.pack(side=Tkinter.LEFT)
        dark = Button(lightDarkFrame, text="dark", command=lambda: self.darkBtn())
        dark.pack(side=Tkinter.LEFT)
        lightDarkFrame.pack()

        btnFrame = Frame(root)
        for i in range(5):
            b = Button(btnFrame, text=str(i), command=lambda n=i: self.btn(n))
            b.pack(side=Tkinter.LEFT)
        btnFrame.pack()

        lightFrame = Frame(root, height=400, width=400)
        lightFrame.pack()
        for name, l in allLights.items():
            w = Label(lightFrame, text="  ", bg="black")
            l['light'].setSimWidget(w)
            w.place(x=l['simX'], y=350-l['simY'])

        def update():
            for name, l in allLights.items():
                l['light'].update()
            root.after(10, update)
        update()
        root.mainloop()

if len(sys.argv) > 1 and sys.argv[1] == 'sim':
    Master().runSim()
else:
    Master().runReal()
