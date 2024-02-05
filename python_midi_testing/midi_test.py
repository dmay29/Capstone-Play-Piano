import mido
from mido import MidiFile, MidiTrack, Message
from mido.backends.rtmidi import Input, Output
# from fluidsynth import Synth
import time

'''
fluid synth can be run from command line, will add in some sort of call here

for now run: fluidsynth -a alsa -g 5 /usr/share/sounds/sf2/FluidR3_GM.sf2
in new terminal: aconnect -o
  this returns something like:
    client 14: 'Midi Through' [type=kernel]
        0 'Midi Through Port-0'
    client 20: 'Impact GX61' [type=kernel,card=1] <---- Get the client number from this line
        0 'Impact GX61 MIDI1'
    client 128: 'FLUID Synth (1527)' [type=user,pid=1527] <----- And this line
        0 'Synth input port (1527:0)'

Run: aconnect 20:0 128:0
Replace the 20 and 128 with the client IDS you saw
   
'''
SOUND_PATH = 'python_midi_testing/[GD] Clean Concert Grand.sf2'
# download from https://musical-artifacts.com/artifacts/3212, was too big to add to github
PIANO_NAME = 'Impact GX61 MIDI1'
# OUTPUT = 'FluidSynth virtual port (77349)'

# Attempted to pass the midi through so the piano could still be used with an external controller,
# Not sure I did it right, couldn't find an output port to send to. Instead its trying to send back 
# to the piano, not sure why.

class MidiInterface():

     # FluidSynth setup
    soundfont_path:str = None
    # fs: Synth = None

    input_port:Input = None
    output_port:Output = None
    

    def __init__(self, soundfont_path = SOUND_PATH, piano_name = PIANO_NAME):
        # self.fs = Synth()
        # self.fs.start(driver='coreaudio')  # use coreaudio driver. Might be mac specific
        # self.sfid = self.fs.sfload(soundfont_path)
        # self.fs.program_select(0, self.sfid, 0, 0)
        # self.soundfont_path = soundfont_path
        self.input_port:Input = mido.open_input(piano_name)
        # self.output_port:Output = mido.open_output()

    def run(self):
        try:
            while True:
                for msg in self.input_port.iter_pending():
                    # if msg.type == 'note_on':
                    #     # Play the note with FluidSynth
                    #     self.fs.noteon(0, msg.note, 127)#msg.velocity) # using 127 becuase using the key velocity directly was too quiet 

                    # elif msg.type == 'note_off':
                    #     # Stop the note with FluidSynth
                    #     self.fs.noteoff(0, msg.note)
                    msg: Message
                    # Parse MIDI message
                    if hasattr(msg, 'note'):
                        note_name, octave = note_number_to_name(msg.note)
                        print(f'{msg.type}: {note_name}{octave}, Velocity: {msg.velocity}')
                    else:
                        print(f'{msg.type}, {msg}')

                    # Pass the MIDI message to the output port
                    # self.output_port.send(msg)

                    
                

        except KeyboardInterrupt:
            pass
        finally:
            self.input_port.close()
            # self.output_port.close()


    


# Function to convert note number to frequency
def note_number_to_frequency(note_number):
    return 440.0 * (2.0 ** ((note_number - 69) / 12.0))

# Function to convert note number to note name
def note_number_to_name(note_number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = note_number // 12 - 1
    note_name = notes[note_number % 12]
    return note_name, octave

if __name__ == '__main__':
    midi = MidiInterface()
    midi.run()







