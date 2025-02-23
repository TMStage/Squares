import pygame
import sys
import os
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 760
CELL_SIZE = 24
GRID_MARGIN_X = 20
GRID_MARGIN_Y = 20
GRID_ROWS, GRID_COLS = 25, 4  # Persistent 4x25 grid
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)  # Blue for marking

def load_random_puzzle(puzzles_folder="Puzzles"):
    """Load a random puzzle from the Puzzles folder."""
    try:
        puzzle_files = [
            f for f in os.listdir(puzzles_folder) if f.endswith(".blox")
        ]
        if not puzzle_files:
            raise FileNotFoundError("No .blox files found in the Puzzles folder.")

        selected_file = random.choice(puzzle_files)
        print(f"Loading puzzle: {selected_file}")

        puzzle = []
        with open(os.path.join(puzzles_folder, selected_file), 'r') as file:
            for line in file:
                row = [int(char) for char in line.strip()]
                puzzle.append(row)

        if len(puzzle) > GRID_ROWS or any(len(row) != GRID_COLS for row in puzzle):
            raise ValueError(f"Puzzle dimensions exceed allowed size (4x{GRID_ROWS}).")

        return puzzle

    except Exception as e:
        print(f"Error loading puzzle: {e}")
        sys.exit()

def draw_mark_triangle(screen, rect):
    """Draw a small blue triangle centered in the given rectangle."""
    triangle_size = rect.width // 2
    center_x = rect.centerx
    center_y = rect.centery
    point1 = (center_x, center_y - triangle_size // 2)
    point2 = (center_x - triangle_size // 2, center_y + triangle_size // 2)
    point3 = (center_x + triangle_size // 2, center_y + triangle_size // 2)
    pygame.draw.polygon(screen, BLUE, [point1, point2, point3])

def draw_grid_with_puzzle(screen, puzzle, puzzle_offset, cell_size, margin_x, margin_y, marked_tile):
    """
    Draw the persistent grid and overlay the puzzle starting from its current offset.
    If a cell is marked and the puzzle covers it, draw a blue triangle.
    Otherwise, if a cell is marked and no puzzle block is covering it, fill it blue.
    """
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(
                margin_x + x * cell_size,
                margin_y + y * cell_size,
                cell_size,
                cell_size,
            )

            # Determine base cell color
            if puzzle_offset <= y < puzzle_offset + len(puzzle):
                cube = puzzle[y - puzzle_offset][x]
                if cube == -1:
                    cell_color = WHITE  # Cleared block
                elif cube == 0:
                    cell_color = GRAY   # Normal cube
                elif cube == 1:
                    cell_color = BLACK  # Forbidden cube
                elif cube == 2:
                    cell_color = GREEN  # Advantage cube
            else:
                cell_color = WHITE

            # If the cell is marked and not covered by the puzzle, fill it with blue.
            if marked_tile == (x, y) and not (puzzle_offset <= y < puzzle_offset + len(puzzle)):
                cell_color = BLUE

            pygame.draw.rect(screen, cell_color, rect)
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)

            # If the cell is marked and is covered by the puzzle, overlay a blue triangle.
            if marked_tile == (x, y) and (puzzle_offset <= y < puzzle_offset + len(puzzle)):
                draw_mark_triangle(screen, rect)

def draw_cursor(screen, cursor_x, cursor_y, cell_size, margin_x, margin_y):
    """Draw the cursor as a yellow square."""
    rect = pygame.Rect(
        margin_x + cursor_x * cell_size,
        margin_y + cursor_y * cell_size,
        cell_size,
        cell_size,
    )
    pygame.draw.rect(screen, YELLOW, rect)

def is_cursor_blocked(cursor_x, cursor_y, puzzle, puzzle_offset):
    """Check if the cursor is in a row occupied by the puzzle."""
    return puzzle_offset <= cursor_y < puzzle_offset + len(puzzle)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Qube Prototype")
    clock = pygame.time.Clock()

    puzzle = load_random_puzzle("Puzzles")
    puzzle_offset = 0  # Puzzle starts at the top
    cursor_x, cursor_y = 0, GRID_ROWS - 1  # Cursor starts at the bottom
    marked_tile = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    cursor_y = max(puzzle_offset + len(puzzle), cursor_y - 1)
                if event.key == pygame.K_s:
                    cursor_y = min(GRID_ROWS - 1, cursor_y + 1)
                if event.key == pygame.K_a:
                    cursor_x = max(0, cursor_x - 1)
                if event.key == pygame.K_d:
                    cursor_x = min(GRID_COLS - 1, cursor_x + 1)
                if event.key == pygame.K_SPACE:
                    # If already marked, unmark and clear block if under puzzle.
                    if marked_tile == (cursor_x, cursor_y):
                        if puzzle_offset <= cursor_y < puzzle_offset + len(puzzle):
                            # Clear the puzzle block.
                            puzzle[cursor_y - puzzle_offset][cursor_x] = -1
                        marked_tile = None
                    else:
                        marked_tile = (cursor_x, cursor_y)
                if event.key == pygame.K_q:
                    if puzzle_offset + len(puzzle) < GRID_ROWS:
                        puzzle_offset += 1
                        while is_cursor_blocked(cursor_x, cursor_y, puzzle, puzzle_offset) and cursor_y < GRID_ROWS - 1:
                            cursor_y += 1

        screen.fill(WHITE)
        draw_grid_with_puzzle(screen, puzzle, puzzle_offset, CELL_SIZE, GRID_MARGIN_X, GRID_MARGIN_Y, marked_tile)
        draw_cursor(screen, cursor_x, cursor_y, CELL_SIZE, GRID_MARGIN_X, GRID_MARGIN_Y)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
