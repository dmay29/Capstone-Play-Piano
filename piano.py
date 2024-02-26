from piano_leds import PianoKeyLEDsRealTime, colors
from midi_reader import extract_notes
from base_classes import Threaded, RealTime

from time import time, sleep
from pathlib import Path
import board
import neopixel


class PianoLEDsRealTime(RealTime, Threaded):

    def __init__(self, first_index, num_leds, num_octaves, fall_time, note_offset, midi_file, speed):
        self.set_time_zero()
        self.first_index = first_index
        self.num_leds = num_leds
        self.num_octaves = num_octaves
        self.fall_time = fall_time
        self.note_offset = note_offset
        self.pixels = neopixel.NeoPixel(board.D21, 127*5, brightness=0.5, auto_write=False)
        self.load_midi(midi_file, speed, note_offset)
        self.keys: dict[int, PianoKeyLEDsRealTime] = self.construct_piano()
        

    def load_midi(self, midi_file, speed, note_offset):
        self.midi_file: Path = Path(midi_file)
        self.timing_dict = extract_notes(self.midi_file, speed, note_offset)

    def loop(self):
        self.refresh()
    
        if self.keys[self.note_offset].time_since_zero > 20:
            now = time()
            for key_num, key in self.keys.items():
                key.set_time_zero(now)

    def refresh(self):
        for key in self.keys.values():
            key.refresh()
        self.pixels.show()

    def construct_piano(self):
        keys = {
            key_num: None 
            for key_num in 
            range(self.note_offset, self.note_offset + 60) 
        }
        LEDs_per_octave = 3 * 7 + 2 * 5 + self.num_leds * 12
        for octave in range(self.num_octaves):
            
            key = 0

            first_led = octave * LEDs_per_octave
            last_led = first_led + LEDs_per_octave
            key_offset = self.note_offset + 12*octave

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

            ## Black Key ##
            keys[key_offset + key] = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 2
            last_led -= self.num_leds

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

             ## Black Key ##
            keys[key_offset + key] = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 2
            last_led -= self.num_leds

             ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

            ## Black Key ##
            keys[key_offset + key] = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 2
            last_led -= self.num_leds

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

            ## Black Key ##
            keys[key_offset + key] = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 2
            last_led -= self.num_leds

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 3
            last_led -= self.num_leds

            ## Black Key ##
            keys[key_offset + key] = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led - self.num_leds, last_led),
                [first_led, first_led + 1],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )

            key += 1
            first_led += 2
            last_led -= self.num_leds

            ## White Key ##
            keys[key_offset + key]  = PianoKeyLEDsRealTime(
                self.pixels,
                range(last_led-1, last_led-1-self.num_leds, -1),
                [first_led, first_led + 1, first_led + 2],
                colors[key],
                self.fall_time,
                note_times = self.timing_dict.get(key_offset + key)
            )
        
        return keys



            

        


    
