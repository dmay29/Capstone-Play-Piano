FILE_NAME = "hot-cross-buns-midi.ly"

with open(FILE_NAME) as ly_file:
    ly_no_highlight = ly_file.read()
    ly_split_at_notes = ly_no_highlight.split("\\relative c {\n")
    ly_split_at_notes = ly_split_at_notes[1::]
    # print(ly_split_at_notes[0])
    note_block = ly_split_at_notes[0].split("}")
    note_block = note_block[0]
    print(note_block)
    note_lines = note_block.split("\n")
    note_lines = [line for line in note_lines if not ("\\" in line or "|" in line)]
    print(note_lines)
    total_note_count = 0
    for line in note_lines:
        notes = line.split(" ")
        notes = [note for note in notes if len(note) > 0]
        i = 0
        while i < len(notes):
            note = notes[i]
            if "<" in note:
                while ">" not in notes[i]:
                    i += 1
                    note += " " + notes[i]
            note += " "
            ly_highlighted_note = ly_no_highlight.replace(note, "\staffHighlight \"lightsteelblue\"\n" + note + "\n" + "\stopStaffHighlight\n")
            with open("highlight_output/" + str(total_note_count) + FILE_NAME, "w") as output_ly_file:
                output_ly_file.write(ly_highlighted_note)
            i += 1
            total_note_count += 1
