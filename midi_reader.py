import mido

def extract_notes(midi_file, speed = 1, note_offset = 24):
    note_dict = {}
    mid = mido.MidiFile(midi_file)
    current_time = 0
    
    for msg in mid:
        current_time += speed * msg.time
        
        if msg.type == 'note_on':
            if msg.note - note_offset not in note_dict:
                note_dict[msg.note - note_offset] = []
            note_dict[msg.note - note_offset].append((current_time, 0))
        elif msg.type == 'note_off':
            if msg.note - note_offset in note_dict and note_dict[msg.note - note_offset][-1][1] == 0:
                note_dict[msg.note - note_offset][-1] = (note_dict[msg.note - note_offset][-1][0],

 current_time - note_dict[msg.note - note_offset][-1][0])
    
    return note_dict

def main():
    midi_file = "composer/sound_files/mary_little_lamb.mid"
    note_dict = extract_notes(midi_file)
    print("Note Dictionary:")
    for note, timestamps in note_dict.items():
        print(f"Note {note}: {timestamps}")

if __name__ == "__main__":
    main()

{28: [  
        (0, 0.27272725),
        (1.090909, 0.27272725),
        (1.3636362499999999, 0.27272725),
        (1.6363634999999999, 0.27272725),
        (3.2727269999999997, 0.27272725),
        (4.363636, 0.27272725),
        (5.4545449999999995, 0.27272725),
        (5.7272722499999995, 0.27272725),
        (5.9999994999999995, 0.27272725),
        (7.090908499999999, 0.27272725)
    ],
 26: [  
        (0.27272725, 0.27272725),
        (0.8181817499999999, 0.27272725),
        (2.181818, 0.27272725),
        (2.45454525, 0.27272725),
        (2.7272724999999998, 0.27272725),
        (4.63636325, 0.27272725),
        (5.18181775, 0.27272725),
        (6.545453999999999, 0.27272725),
        (6.818181249999999, 0.27272725),
        (7.363635749999999, 0.27272725)
    ],
 24:[  
        (0.5454545, 0.27272725),
        (4.9090905, 0.27272725),
        (7.636362999999999, 0.27272725)
    ],
 31:[
        (3.5454542499999997, 0.27272725),
        (3.8181814999999997, 0.27272725)
    ]
}

