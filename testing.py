from piano_reader import NotesPianoReader
from piano import PianoLEDsRealTime
from scoring import score_notes
from speaker import set_volume
from time import time, sleep

from base_classes import RealTime

if __name__ == '__main__':
    # RealTime.now = lambda _: time()/5
    piano = PianoLEDsRealTime(0, 8, 5, 1, 24, "composer/sound_files/mary_little_lamb.mid", 2)
    piano_reader = NotesPianoReader(keys_offset=49)
    piano.sync(piano_reader)
    piano_reader.attach_vol_knob_callback(lambda vol: set_volume(int(vol/2)))
    piano.begin(multithreaded=True)
    piano_reader.begin()

    sleep(20)
    score_notes(piano.timing_dict, piano_reader.get_notes())