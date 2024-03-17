from piano_reader import ControlPianoReader
from speaker import set_volume
from time import sleep
import mido
from mido import Message
from mido.backends.rtmidi import Input
from neopixel_translation import LEDMatrix
from piano_leds import colors
from multiprocessing import Queue

from base_classes import RealTime, Threaded

PIANO_NAME = 'Impact GX61 MIDI1'

class LEDNoteEcho(RealTime):

    def __init__(self, key_num, led_array_shape:tuple[int, int], pixel_array:LEDMatrix, piano:"PlayerModePiano"):
        ''' Shape = (w,h) '''
        self.set_time_zero()
        self.piano = piano
        self.key_num = key_num
        self.width, self.height = led_array_shape
        self.pixel_array = pixel_array

    def calc(self):
        now = self.time_since_zero
        for row in range(self.height):
            for col in range(self.width):
                d = (row**2 + (col-self.key_num)**2)**0.5
                self.pixel_array[row][col] = 1 if abs(now-d) < 10 else 0

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

class PlayerModePiano(ControlPianoReader, RealTime):
   
    def __init__(self, matrix: LEDMatrix, piano_name = PIANO_NAME, time_zero = None, keys_offset = 0):
        self.set_time_zero()
        super().__init__(piano_name, keys_offset)
        self.notes_queue = Queue()
        self.leds = PlayerModeLEDs(matrix, self.notes_queue)
        self.sync(self.leds)

    def begin(self, threaded = True):
        self.leds.begin(multithreaded=True)
        super().begin(threaded)

    def read_note_msg(self, msg: Message, now = None):
        if now is None:
            now = self.time_since_zero
        if msg.type == "note_on": 
            note_num = msg.note - self.keys_offset
            self.notes_queue.put([note_num, now, None, msg.velocity])

        elif msg.type == "note_off":
            note_num = msg.note - self.keys_offset
            self.notes_queue.put([note_num, now])
    
      
    def loop(self):
        for msg in self._input_port.iter_pending():
            print(msg)
            self.read_msg(msg)
            now = self.time_since_zero
            self.read_note_msg(msg, now)


class PlayerModeLEDs(RealTime, Threaded):
    
    def __init__(self, matrix: LEDMatrix, queue: Queue):
        self.notes_queue = queue
        self.matrix = matrix
        self.current_notes = []

    def read_queue(self):
        while not self.notes_queue.empty():
            new_note = self.notes_queue.get()
            if len(new_note) == 4:
                self.current_notes.append(new_note) 
            else:
                for i, note in enumerate(self.current_notes):
                    if note[0] == new_note[0] and note[2] is None:
                        self.current_notes[i][2] = new_note[1]
                        break         

    def show(self):
        now = self.time_since_zero
        self.matrix.clear()
        done_echos = []
        for i,note in enumerate(self.current_notes):
            showed = False
            key_num, start, end, velocity = note
            key_num -= 72 # DEBUGGING
            color = colors[key_num % 12]
            if end is None: 
                end = now
                self.matrix[key_num, 'key'] = color
            speed = velocity/6
            brightness = velocity/127
            splash_radius = max(2,int(velocity/10))
            outer_edge = (now-start)*speed
            inner_edge = min(outer_edge - 1,(now-end)*speed)
            
            for row in range(min(splash_radius,8)):
                for col in range(max(0,key_num-splash_radius),min(key_num+splash_radius,60)):
                    d = (row**2 + (col-(key_num))**2)**0.5
                    if outer_edge >= d >= inner_edge: 
                        showed = True
                        b = max(0,brightness * (1-d/outer_edge) * (1-d/splash_radius))
                        self.matrix.average_pixel((col, 7-row), color,weight = b)#[col, 7-row] += color
            if not showed:
                done_echos.append(i)
        for i in done_echos[::-1]:
            self.current_notes.pop(i)

        self.matrix.show()
    
    def loop(self):
        self.read_queue()
        self.show()


            

        



if __name__ == '__main__':
    # RealTime.now = lambda _: time()/5
    matrix = LEDMatrix(brightness=0.5)
    piano = PlayerModePiano(matrix)
    
    piano.begin()
    while True:
        sleep(1)

    #score_note(piano.timing_dict, piano.get_notes())