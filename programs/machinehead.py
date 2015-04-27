import common
import lights
import time


class MachineheadProgram(common.Program):
    def reset(self):
        self.firstIntro = True
        self.lastn = -1
        self.btnCount = 0
        self.lastBPMUpdate = time.time()
        self.bpm = 113
        self.spb = 60.0 / self.bpm
        self.autoBtns = [
                (1, 0.0),
                (1, 4.2)
                ]

    def updateBPM(self, beats):
        self.bpm = 60.0/(time.time() - self.lastBPMUpdate)*beats
        self.lastBPMUpdate = time.time()
        self.spb = 60.0 / self.bpm

    def intro(self, n):
        self.updateBPM(8)
        if self.firstIntro:
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
        if not self.firstIntro or n >= 3:
            if n < 6:
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
                self.setLights(['frontTanner', 'frontRight', 'backSpencer'],
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
            else:
                self.setLights(['frontSpencer', 'frontLeft', 'backTanner'],
                                lambda: lights.getRGBSequenceController(
                                    (
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*2 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*3 +
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*4
                                    )*2
                                ))
                self.setLights(['frontTanner', 'frontRight', 'backSpencer'],
                                lambda: lights.getRGBSequenceController(
                                    (
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*2 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*3 +
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.5),
                                        ((100,0,0), self.spb*0.0)]*1 +
                                        [((255,255,255), self.spb*0.25),
                                        ((100,0,0), self.spb*0.0)]*4
                                    )*2
                                ))
            if n%2 == 1:
                self.setLights(['rear1', 'rear4', 'backTravis'],
                               lambda: lights.getRGBSequenceController([
                                   ((255,255,255), self.spb*4.0),
                                   ((255,255,0), self.spb*4.0),
                                   ((255,0,0), self.spb*2.0),
                               ]))
                self.setLights(['rear2', 'rear3', 'backDoug'],
                               lambda: lights.getRGBSequenceController([
                                   ((255,255,255), self.spb*4.0),
                                   ((255,0,0), self.spb*4.0),
                                   ((255,255,0), self.spb*2.0),
                               ]))
            else:
                self.setLights(['rear1', 'rear4', 'backTravis'],
                               lambda: lights.getRGBSequenceController([
                                   ((255,255,255), self.spb*4.0),
                                   ((255,0,0), self.spb*4.0),
                                   ((255,255,0), self.spb*2.0),
                               ]))
                self.setLights(['rear2', 'rear3', 'backDoug'],
                               lambda: lights.getRGBSequenceController([
                                   ((255,255,255), self.spb*4.0),
                                   ((255,255,0), self.spb*4.0),
                                   ((255,0,0), self.spb*2.0),
                               ]))

    def verse(self, n):
        pass

    def chorus(self, n):
        pass

    def solo(self, n):
        pass

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
                  3: self.solo}

        btnmap[n](self.btnCount)
