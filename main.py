import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # Adjusted resolution
GRID_COLS, GRID_ROWS = 4, 25  # Grid dimensions
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Calculate cell size dynamically based on width
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

def draw_grid(screen, cols, rows, cell_size):
    """Draw a simple grid on the screen."""
    for x in range(cols):
        pygame.draw.line(screen, GRAY, (x * cell_size, 0), (x * cell_size, rows * cell_size))
    for y in range(rows):
        pygame.draw.line(screen, GRAY, (0, y * cell_size), (cols * cell_size, y * cell_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Squares Prototype")
    clock = pygame.time.Clock()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update logic here

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen, GRID_COLS, GRID_ROWS, CELL_SIZE)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
