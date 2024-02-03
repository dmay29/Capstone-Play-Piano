import board
import neopixel
from time import time, sleep

BPM = 300
DELAY = 60/BPM

NUM_LEDS = 54
FULL = 1
DIM = .25
VERY_DIM = .05

white = [255, 255, 255]
off = [0,0,0]
black = off
red = [255,0,0]
orange = [255,100,0]
yellow = [255,255,0]
green = [0,255,0]
teal = [0,255,255]
blue = [0,0,255]
purple = [100, 0, 255]
magenta = [255, 0, 255]


colors = [red, orange, yellow, green, teal, blue, purple, magenta]
pixels = neopixel.NeoPixel(board.D21, NUM_LEDS, brightness = .5, auto_write=False)

def dimmer(color, brightness):
    return [int(max(min(i*brightness,255),0)) for i in color]

class PianoKeyLEDs:
    def __init__(self,above_key_indexes:list, key_indexes:list, color:list):
        self.above_key_indexes = list(above_key_indexes)
        self.key_indexes = list(key_indexes)
        self.color = color
        self.pixel_array = [0 for pixel in range(len(self.above_key_indexes) + 3)]

    def set_pixels(self):
        for i,brightness in enumerate(self.pixel_array[2:-1]):
            index = self.above_key_indexes[i]
            pixels[index] = dimmer(self.color, brightness)

        self.light_key(self.pixel_array[-1] != 0)

    
    def light_key(self, brightness):
        for index in self.key_indexes:
                pixels[index] = dimmer(self.color, brightness)

    def waterfall_begin(self):
        self.pixel_array[0] = VERY_DIM
        self.pixel_array[1] = DIM
        self.pixel_array[2] = FULL
        self.set_pixels()

    def waterfall_advance(self):
        self.pixel_array = [0]+self.pixel_array[0:-1]
        self.set_pixels()


class PianoKeyLEDsRealTime:
    width = 4
    A = (2/width)**4
    B = 2*(2/width)**2
    start_time=None
    speed = 1

    def __init__(self,above_key_indexes:list, key_indexes:list, color:list):
        self.above_key_indexes = list(above_key_indexes)
        self.key_indexes = list(key_indexes)
        self.color = color
        self.pixel_array = [0 for pixel in range(len(self.above_key_indexes) + 1)]

    @property
    def time_since_start(self):
        if self.start_time is not None:
            return time() - self.start_time
        

    def set_pixels(self):
        for i,brightness in enumerate(self.pixel_array[0:-1]):
            index = self.above_key_indexes[i]
            pixels[index] = dimmer(self.color, brightness)

        self.light_key(self.pixel_array[-1] != 0)

    
    def light_key(self, brightness):
        for index in self.key_indexes:
                pixels[index] = dimmer(self.color, brightness)

    def waterfall_begin(self, fall_time):
        self.speed = len(self.pixel_array)/fall_time
        self.start_time = time()


    def waterfall_refresh(self):
        now = self.time_since_start
        if now is None:
            return

        else:
            now *= self.speed
        for i,pixel in enumerate(self.pixel_array):
            x = now - i
            if abs(x) <= self.width/2:
                self.pixel_array[i] = self.A*(x**4)-self.B*(x**2)+1
            else:
                self.pixel_array[i] = 0
        self.set_pixels()



def main():      
    keys = [
        PianoKeyLEDsRealTime(range(48,41,-1),[49,50], red),
        PianoKeyLEDsRealTime(range(41,34,-1),[51,52], green),
    ]

    sequence = [[1,[1,0]],
                [3,[0,1]],
                [6,[1,0]],
                [7,[0,1]],
                [11,[1,0]],
                [11,[0,1]],
                [15,[0,0]],]
    notes_sequence = []

    while True:
        if not notes_sequence:
            notes_sequence = sequence.copy()
            start = time()
        now = time() - start
        if now > notes_sequence[0][0]:
            t, notes = notes_sequence.pop(0)
            for i, note in enumerate(notes):
                if note: keys[i].waterfall_begin(2)

        for key in keys:
            key.waterfall_refresh()
        pixels.show()
            
if __name__ == '__main__':
    main()