from piano_leds import PianoKeyLEDsRealTime, colors
from midi_reader import extract_notes
from base_classes import Threaded, RealTime, Event
from neopixel_translation import LEDMatrix

from pathlib import Path

class PianoLEDsRealTime(RealTime, Threaded):

    def __init__(self, fall_time, note_offset, midi_file, speed):
        self.set_time_zero()
        self.fall_time = fall_time
        self.key_offset = note_offset
        self.pixels = LEDMatrix(brightness=0.5)
        self.keys: dict[int, PianoKeyLEDsRealTime] = self.construct_piano()
        self.load_midi(midi_file, speed, note_offset)
        self.end_time = self.timing_dict['end']
        self.song_over_event = Event()
        self.song_over_event.clear()
    
    def song_over(self):
        return self.time_since_zero > self.end_time

    
    def load_midi(self, midi_file, speed, note_offset):
        self.midi_file: Path = Path(midi_file)
        self.timing_dict = extract_notes(self.midi_file, speed, note_offset)
        for key_num, key in self.keys.items():
            key.make_notes(self.timing_dict.get(key_num))

    def begin(self):
        self.set_time_zero(self.now - self.fall_time)   
        super().begin()

    def loop(self):
        """ Threaded loop function/ Started by running piano.begin() """
        now = self.now()
        self.refresh()
        prev = now
        if self.song_over():
            self.song_over_event.set()

    def refresh(self):
        for key in self.keys.values():
            key.refresh()
        self.pixels.show()

    def construct_piano(self):
        keys = {
            key_num+self.key_offset: 
                PianoKeyLEDsRealTime(
                    self.pixels, 
                    key_num, 
                    colors[(key_num + self.key_offset) % 12], 
                    self.fall_time
                ) 
            for key_num in range(60) 
        }
        
        return keys




            

        


    
