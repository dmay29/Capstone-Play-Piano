from typing import List

class CLIPiano():
    numKeys: int
    activeKeys: List[int] = []

    def __init__(self, numKeys):
        self.numKeys = numKeys
    
    def renderPiano(self, activeKeys: List[int]):
        self.activeKeys = activeKeys
        self.renderBlackKeys()
        self.renderWhiteKeys()

    def renderBlackKeys(self):
        black_key_chars = [' ', 'C#', ' ', 'D#', '   ', ' ', 'F#', ' ', 'G#', ' ', 'A#', ' ']
        black_key_mask = [False, True, False, True, False, False, True, False, True, False, True, False]
        for i in range(0, self.numKeys):
            if (i % 12) == 0:
                print('|', end='')
            if (self.activeKeys.count(i) != 0 and black_key_mask[i % 12]):
                output = black_key_chars[i % 12]
                output = output.replace(output[0], '_')
                output = output.replace(output[1], ' ')
                print(f'\033[92m{output}\033[0m', end='')
            else:
                print(black_key_chars[i % 12], end='')
        print('')

    def renderWhiteKeys(self):
        white_key_chars = ['C', '  ', 'D', '  ', 'E  ', 'F', '  ', 'G', '  ', 'A', '  ', 'B']
        white_key_mask = [True, False, True, False, True, True, False, True, False, True, False, True]
        for i in range(0, self.numKeys):
            if (i % 12) == 0:
                print('|', end='')
            if (self.activeKeys.count(i) != 0 and white_key_mask[i % 12]):
                output = white_key_chars[i % 12]
                output = output.replace(output[0], '_')
                print(f'\033[92m{output}\033[0m', end='')
            else:
                print(white_key_chars[i % 12], end='')
        print('')