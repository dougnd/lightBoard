import common, math, lights, random, time

class IfYouCould(common.Program):
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
