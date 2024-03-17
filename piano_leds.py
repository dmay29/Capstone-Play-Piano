import board
import neopixel
from time import time, sleep
from midi_reader import extract_notes

from base_classes import RealTime

BPM = 300
DELAY = 60 / BPM

NUM_LEDS = 128
FULL = 1
DIM = 0.25
VERY_DIM = 0.05

white = [255, 255, 255]
off = [0, 0, 0]
black = off
red = [255, 0, 0]
orange = [255, 100, 0]
yellow = [255, 255, 0]
yellow_green = [100, 255, 0]
green = [0, 255, 0]
green_teal = [0, 255, 100]
teal = [0, 255, 255]
blue_teal = [0, 100, 255]
blue = [0, 0, 255]
purple = [100, 0, 255]
magenta = [255, 0, 255]
magenta_red = [255, 0, 100]


colors = [
    red,
    orange,
    yellow,
    yellow_green,
    green,
    green_teal,
    teal,
    blue_teal,
    blue,
    purple,
    magenta,
    magenta_red,
]
pixels = neopixel.NeoPixel(board.D21, NUM_LEDS, brightness=0.5, auto_write=False)


def dimmer(color, brightness):
    return [int(max(min(i * brightness, 255), 0)) for i in color]


class LEDNote:

    def __init__(self, start_time, duration, parent_key: "PianoKeyLEDsRealTime"):
        self.parent_key = parent_key

        self.pixels_start_time = start_time - parent_key.fall_time # The pixels must start 'fall_time' before the note would hit the key
        self.pixels_end_time = start_time + duration # pixels end 'duration' time after the note has hit the key
        self.width = duration / self.parent_key.time_per_pixel
        self.A = (2 / self.width) ** 4
        self.B = 2 * (2 / self.width) ** 2
        

    def in_range(self, now):
        return self.pixels_start_time < now < self.pixels_end_time

    def show(self, now):
        start_pixel = (now - self.pixels_start_time) / self.parent_key.time_per_pixel
        # print(start_pixel)
        for i in range(len(self.parent_key.pixel_array)):
            x = i - start_pixel + self.width / 2
            if -self.width / 2 < x < self.width / 2:
                val = self.A * (x**4) - self.B * (x**2) + 1
                self.parent_key.pixel_array[i] = val


class PianoKeyLEDsRealTime(RealTime):
    """

    """
    num_pixels = 8

    def __init__(
        self,
        pixels,
        key_num:int,
        color: list,
        fall_time: int = 1,
        note_times: list[list[float, float]] = None,
    ):
        self.set_time_zero()
        self.pixels = pixels
        self.key_num = key_num
        self.color = color
        self.fall_time = fall_time
        
        self.time_per_pixel = self.fall_time / self.num_pixels
        self.pixel_array = [0 for pixel in range(self.num_pixels + 1)]
        self.make_notes(note_times)
        

    def refresh(self):
        self.pixel_array = [0 for _ in self.pixel_array]
        now = self.time_since_zero
        for note in self.notes:
            if note.in_range(now):
                note.show(now)
        self.set_pixels()

    def set_pixels(self):
        for i, brightness in enumerate(self.pixel_array[0:-1]):
            self.pixels[self.key_num, i] = dimmer(self.color, brightness)

        self.light_key(self.pixel_array[-1] != 0)

    def light_key(self, brightness):
        self.pixels[self.key_num, 'key'] = dimmer(self.color, brightness)


    def make_notes(self, note_times=None):
        if note_times is None: 
            self.notes = []
            return 
        
        self.notes = [LEDNote(note_times[0][0], note_times[0][1], self)]
        for start, duration in note_times[1:]:
            previous_note = self.notes[-1]
            off_time = start - previous_note.pixels_end_time
            if off_time < self.time_per_pixel / 2:
                note_start_adjust = self.time_per_pixel / 2 - off_time
                self.notes.append(
                    LEDNote(
                        start + note_start_adjust, duration - note_start_adjust, self
                    )
                )
            else:
                self.notes.append(LEDNote(start, duration, self))
