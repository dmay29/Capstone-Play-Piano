from piano_reader import NotesPianoReader
from piano import PianoLEDsRealTime
from scoring import score_note, getMaxScore
from speaker import set_volume
from time import sleep

from base_classes import RealTime



class ScoringModePiano(NotesPianoReader):
    
    def __init__(self, midi_file, speed, **kwargs):
        super().__init__(keys_offset=48)
        self.leds = PianoLEDsRealTime(0,8,5,2,24,midi_file=midi_file, speed=speed, **kwargs)
        self.sync(self.leds)
        self.attach_vol_knob_callback(lambda vol: set_volume(int(vol/2)))
        self.totalScore = 0

    def begin(self, threaded = True):
        self.leds.begin(multithreaded=True)
        super().begin(threaded)

    def loop(self):
        super().loop()
        for note in self.get_notes():
            score = score_note(self.leds.timing_dict, note)
            print(f"{self.totalScore} + {score} = {self.totalScore + score}")
            self.totalScore += score
        # if self.leds.song_over():
        #     self.leds.end()
        #     self.end()
            
    def max_score(self):
        return getMaxScore(self.leds.timing_dict)

    def close(self):
        self.leds._end()
        super()._end()

        



if __name__ == '__main__':
    # RealTime.now = lambda _: time()/5
    piano = ScoringModePiano("composer/sound_files/mary_little_lamb.mid", 2)
    
    piano.begin()
    piano.leds.song_over_event.wait()
    print(f"Song complete\nScore: {piano.totalScore} / {piano.max_score()}")
    piano.close()

    #score_note(piano.timing_dict, piano.get_notes())