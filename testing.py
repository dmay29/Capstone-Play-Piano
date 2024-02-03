from LEDS.key_start import *
import time
from python_midi_testing.midi_test import MidiInterface
from LEDS import key_start
import threading


    
keys = [
    PianoKeyLEDs(range(48,41,-1),[49,50], red),
    PianoKeyLEDs(range(41,34,-1),[51,52], green),
]

notes_sequence = [[1,0],
                  [0,0],
                  [0,0],
                  [0,1],
                  [0,0],
                  [0,0],
                  [0,0],
                  [0,0],
                  [0,0],
                  [0,0],
                  [0,0],
                  [0,0],]

midi = MidiInterface()
threading.Thread(target=midi.run).start()

key_start.main()

    
    
