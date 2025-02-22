import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # Game window dimensions
GRID_COLS, GRID_ROWS = 4, 25  # Grid dimensions
CELL_SIZE = 24  # Size of each cell in the grid (small squares)
GRID_MARGIN_X = 20  # Margin from the left edge of the screen
GRID_MARGIN_Y = 20  # Margin from the top edge of the screen
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

def draw_grid(screen, cols, rows, cell_size, margin_x, margin_y):
    """Draw a 4x25 grid on the left side of the screen with margins."""
    for x in range(cols):
        for y in range(rows):
            rect = pygame.Rect(
                margin_x + x * cell_size,  # X-coordinate
                margin_y + y * cell_size,  # Y-coordinate
                cell_size,  # Width
                cell_size,  # Height
            )
            pygame.draw.rect(screen, GRAY, rect, 1)  # Draw cell border

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Qube Prototype")
    clock = pygame.time.Clock()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update logic here

        # Draw everything
        screen.fill(BLUE)
       
