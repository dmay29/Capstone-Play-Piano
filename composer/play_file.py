import mido
from utils.midi_and_key_converter import midiToKey
from utils.cli_piano import CLIPiano

class MidiInterface():

    def __init__(self):
        self.midi_file = mido.MidiFile("sound_files/mary_little_lamb.mid")
        self.cli_piano = CLIPiano(61)
        self.active_keys = []

    def run(self):
        try:
            print(self.midi_file)
            while True:
                for msg in self.midi_file.play():
                    if msg.type == 'note_on':
                        self.active_keys.append(midiToKey(msg.note))
                        self.cli_piano.renderPiano(self.active_keys)
                        print('')

                    elif msg.type == 'note_off':
                        self.active_keys.remove(midiToKey(msg.note))      
                
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    midi = MidiInterface()
    midi.run()