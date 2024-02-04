MIDI_TO_KEY_SHIFT = 24

def midiToKey(midiNoteNumber: int) -> int:
    return midiNoteNumber - MIDI_TO_KEY_SHIFT

def keyToMidi(keyIdx: int) -> int:
    return keyIdx + MIDI_TO_KEY_SHIFT