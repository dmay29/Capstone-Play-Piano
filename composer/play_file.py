import mido
from utils.midi_and_key_converter import midiToKey
from utils.cli_piano import CLIPiano

from typing import List, Tuple
from time import time
from utils.key_led_control import pixels, red, PianoKeyLEDsRealTime, LEDPiano

class TimingInfo():
    keyIdx: int
    startTimeUs: float
    durationUs: float

    def __init__(self, keyIdx, startTimeUs, durationUs):
        self.keyIdx = keyIdx
        self.startTimeUs = startTimeUs
        self.durationUs = durationUs
    
    def __str__(self):
        return f"[{self.keyIdx}, {self.startTimeUs}, {self.durationUs}]"
    
    def __repr__(self):
        return f"[{self.keyIdx}, {self.startTimeUs}, {self.durationUs}]"

class MidiInterface():

    sequence = []
    tempo = 500000
    time = (4, 4)

    def __init__(self):
        self.midi_file = mido.MidiFile("sound_files/mary_little_lamb.mid")
        self.ticks_per_beat = self.midi_file.ticks_per_beat
        self.cli_piano = CLIPiano(61)
        self.led_piano = LEDPiano(61)
        self.active_keys = []
        self.active_notes = []
        self.timing_infos : List[TimingInfo] = []
        self.now_us = 0
    
    def run(self):
        time_step = 0
        loop = True
        try:
            print(self.midi_file)
            while loop:
                for msg in self.midi_file.play(meta_messages=True):
                    if msg.type == 'note_on':
                        note_repr = [0] * 12
                        idx = midiToKey(msg.note) - 24
                        note_repr[idx] = 1
                        self.sequence.append([time_step, note_repr])
                        time_step = time_step + 1
                        self.active_notes.append(msg.note)
                        self.timing_infos.append(TimingInfo(midiToKey(msg.note), self.now_us, 0))
                        self.active_keys.append(midiToKey(msg.note))
                        self.cli_piano.renderPiano(self.active_keys)
                        print('')
                        self.led_piano.renderPiano(self.active_keys)

                    elif msg.type == 'note_off':
                        if (msg.note in self.active_notes):
                            self.active_notes.remove(msg.note)
                            note_timing = [x for x in self.timing_infos if x.keyIdx == midiToKey(msg.note)][-1]
                            duration = msg.time * 1e6
                            note_timing.durationUs = duration
                            self.now_us += duration
                        self.active_keys.remove(midiToKey(msg.note))    

                    elif msg.type == "end_of_track":
                        loop = False
                    
                    elif msg.type == "time_signature":
                        self.time = (msg.numerator, msg.denominator)

                    elif msg.type == "set_tempo":
                        self.tempo = msg.tempo
                
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    midi = MidiInterface()
    midi.run()
    print(f"Tempo: {midi.tempo}, Time: {midi.time}, BPM: {mido.tempo2bpm(midi.tempo, midi.time)}")

    # keys = [
    #     PianoKeyLEDsRealTime(range(79,72,-1), [0, 1, 2], red),
    #     PianoKeyLEDsRealTime(range(72,65,-1), [3, 4], red),
    #     PianoKeyLEDsRealTime(range(65,58,-1), [5, 6, 7], red),
    #     PianoKeyLEDsRealTime(range(58,51,-1), [8, 9], red),
    #     PianoKeyLEDsRealTime(range(51,44,-1), [10, 11, 12], red),
    #     PianoKeyLEDsRealTime(range(44,37,-1), [13, 14, 15], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [16, 17], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [18, 19, 20], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [21, 22], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [23, 24, 25], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [26, 27], red),
    #     PianoKeyLEDsRealTime(range(37,30,-1), [28, 29, 30], red),
    # ]

    # notes_sequence = []
    # prev_time = time()
    # while True:
    #     # print(time() - prev_time)
    #     prev_time = time()
    #     if not notes_sequence:
    #         notes_sequence = midi.sequence.copy()
    #         start = time()
    #     now = time() - start
    #     if now > notes_sequence[0][0]:
    #         t, notes = notes_sequence.pop(0)
    #         for i, note in enumerate(notes):
    #             if note: keys[i].waterfall_begin(2)

    #     for key in keys:
    #         key.waterfall_refresh()
    #     pixels.show()