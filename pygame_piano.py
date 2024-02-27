import pygame
import sys
import random
import numpy as np
from base_classes import RealTime, Threaded
from midi_reader import extract_notes
# Initialize Pygame


PIXELS = 20
# Column settings
NUM_COLUMNS = 61
NUM_ROWS = 20
COLUMN_WIDTH = PIXELS

# Set up the display
PIXELS_HEIGHT = NUM_ROWS*PIXELS


# Rectangle settings
RECT_WIDTH = COLUMN_WIDTH  # Adjust for spacing
MAX_RECT_HEIGHT = 5*PIXELS
MIN_RECT_HEIGHT = PIXELS
RECT_SPEED =  int(PIXELS_HEIGHT) # pixels per second

TIME_PER_PIXEL = PIXELS_HEIGHT/RECT_SPEED



# Piano settings

KEY_WIDTH = COLUMN_WIDTH
KEY_HEIGHT = PIXELS * 2
PADDING = 1  # Padding between keys

WIDTH, HEIGHT = NUM_COLUMNS*PIXELS, PIXELS_HEIGHT+KEY_HEIGHT

pygame.display.set_caption("Piano")

PIXELS_RECT = pygame.Rect(0, 0, WIDTH, PIXELS_HEIGHT)


# List to hold falling rectangles

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Make Note

# Function to create a gradient surface
def create_gradient_surface(width, height, center_color, outer_color):
    gradient_surf = pygame.Surface((width, height))
    A = (2/height)**4
    B = 2*(2/height)**2
    for y in range(height):
        progress = -(A*((y-height/2)**4)-B*((y-height/2)**2))
        color = (
            int(center_color[0] + (outer_color[0] - center_color[0]) * progress),
            int(center_color[1] + (outer_color[1] - center_color[1]) * progress),
            int(center_color[2] + (outer_color[2] - center_color[2]) * progress)
        )
        pygame.draw.line(gradient_surf, color, (0, y), (width, y))
    return gradient_surf

def map_screen(screen, block_size = PIXELS):
    screen_array = pygame.surfarray.array3d(screen)
    
    averaged_array = np.zeros((NUM_ROWS, NUM_COLUMNS), dtype=np.uint8)
    for y in range(0, NUM_ROWS):
        for x in range(0, NUM_COLUMNS):
            x_coord = x * block_size
            y_coord = y * block_size
            block = screen_array[x_coord:x_coord+block_size, y_coord:y_coord+block_size]
            average_color = np.mean(block, axis=(0, 1)).astype(np.uint8)
            averaged_array[y, x] = average_color[0]

    # Print the first few elements of the averaged array
    # [print(row) for row in averaged_array.tolist()]
    # print('\n\n\n')

class PyGamePiano(RealTime, Threaded):
    falling_rectangles:list = None
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def __init__(self, midi):
        # Generate a new rectangle at a random column
        self.falling_rectangles = []
        notes = extract_notes(midi,50)
        for note_num, note_info in notes.items():
            for start, duration in note_info:
                self.make_note(note_num, start*10, duration, (255,255,255))
            
        

        
    def make_note(self, note_num, start_time, duration, color):
        column = note_num
        rect_height = int(duration*TIME_PER_PIXEL*PIXELS)
        gradient_surf = create_gradient_surface(RECT_WIDTH, rect_height, color, (0, 0, 0))
        self.falling_rectangles.append((column, rect_height, -start_time*TIME_PER_PIXEL, gradient_surf))


    def loop(self):
        # Event handling
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.running = False

        # Clear the screen
        self.screen.fill((0, 0, 0))
        y_step = RECT_SPEED * clock.get_time() / 1000.0
        print(y_step)
        # Place Keys
        for i in range(NUM_COLUMNS):
            key_x = i * COLUMN_WIDTH
            if i % 12 in [0,2,4,5,7,9,11]:
                key_color = (255,255,255)
            else:
                key_color = (50,50,50)
            
            pygame.draw.rect(self.screen, key_color, (key_x, HEIGHT - KEY_HEIGHT, KEY_WIDTH - PADDING, KEY_HEIGHT))

        # Update and draw falling rectangles
        for i, (column, rect_height, rect_y, gradient_surf) in enumerate(self.falling_rectangles):
            rect_x = column * COLUMN_WIDTH + (COLUMN_WIDTH - RECT_WIDTH) // 2
            
            if -rect_height < rect_y:
                self.screen.blit(gradient_surf, (rect_x, rect_y))
            
            # Move the rectangle downwards
            rect_y += y_step
            self.falling_rectangles[i] = (column, rect_height, rect_y, gradient_surf)

            # Check if the rectangle reaches the bottom
            if rect_y > PIXELS_HEIGHT:
                self.falling_rectangles.pop(i)

        # Update the display
        pygame.display.flip()
        map_screen(self.screen)

        # Cap the frame rate
        clock.tick(60)

    
if __name__ == '__main__':
    pygame.init()
    piano = PyGamePiano('composer/sound_files/mary_little_lamb.mid')
    piano.running = True
    piano.begin()
