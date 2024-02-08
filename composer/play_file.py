import mido
from utils.midi_and_key_converter import midiToKey
from utils.cli_piano import CLIPiano

from time import time
from utils.key_start import pixels, red, PianoKeyLEDsRealTime


class MidiInterface():

    sequence = []

    def __init__(self):
        self.midi_file = mido.MidiFile("sound_files/mary_little_lamb.mid")
        self.cli_piano = CLIPiano(61)
        self.active_keys = []

    def run(self):
        time_step = 0
        loop = True
        try:
            print(self.midi_file)
            while loop:
                for msg in self.midi_file:
                    if msg.type == 'note_on':
                        note_repr = [0] * 12
                        idx = midiToKey(msg.note) - 24
                        note_repr[idx] = 1
                        self.sequence.append([time_step, note_repr])
                        time_step = time_step + 1
                        self.active_keys.append(midiToKey(msg.note))
                        self.cli_piano.renderPiano(self.active_keys)
                        print('')

                    elif msg.type == 'note_off':
                        self.active_keys.remove(midiToKey(msg.note))    

                    elif msg.type == "end_of_track":
                        loop = False 
                
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    midi = MidiInterface()
    midi.run()
    print(midi.sequence)

    keys = [
        PianoKeyLEDsRealTime(range(48,41,-1), [0, 1, 2], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [3, 4], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [5, 6, 7], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [8, 9], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [10, 11, 12], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [13, 14, 15], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [16, 17], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [18, 19, 20], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [21, 22], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [23, 24, 25], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [26, 27], red),
        PianoKeyLEDsRealTime(range(41,34,-1), [28, 29, 30], red),
    ]

    notes_sequence = []
    prev_time = time()
    while True:
        # print(time() - prev_time)
        prev_time = time()
        if not notes_sequence:
            notes_sequence = midi.sequence.copy()
            start = time()
        now = time() - start
        if now > notes_sequence[0][0]:
            t, notes = notes_sequence.pop(0)
            for i, note in enumerate(notes):
                if note: keys[i].waterfall_begin(2)

        for key in keys:
            key.waterfall_refresh()
        pixels.show()
