import pygame  # Import the pygame library for graphical functions
import random  # Import random to place mines randomly

# Class representing each cell in the grid
class Cell:
    """
    Represents a single cell on the Minesweeper board.

    Attributes:
        x (int): The X-coordinate of the cell.
        y (int): The Y-coordinate of the cell.
        is_mine (bool): Whether the cell contains a mine.
        is_revealed (bool): Whether the cell has been revealed.
        is_flagged (bool): Whether the cell has been flagged by the player.
        adjacent_mines (int): The number of mines adjacent to the cell.
    """
    
    def __init__(self, x, y):
        """
        Initializes a new Cell.

        Args:
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.
        """
        self.x = x  # X coordinate of the cell
        self.y = y  # Y coordinate of the cell
        self.is_mine = False  # Boolean to check if this cell is a mine
        self.is_revealed = False  # Boolean to check if this cell has been revealed
        self.is_flagged = False  # Boolean to check if this cell has been flagged
        self.adjacent_mines = 0  # Number of mines surrounding this cell

    def reveal(self):
        """
        Reveals the cell if it is not flagged.
        """
        if not self.is_flagged:
            self.is_revealed = True

    def toggle_flag(self):
        """
        Toggles the flag status of the cell. Can only flag cells that are not revealed.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged


# Class representing the Minesweeper board
class Board:
    """
    Represents the Minesweeper game board, which is a grid of Cell objects.

    Attributes:
        width (int): The number of cells horizontally.
        height (int): The number of cells vertically.
        num_mines (int): The total number of mines on the board.
        grid (list): A 2D list representing the board, containing Cell objects.
    """

    def __init__(self, width, height, num_mines):
        """
        Initializes the board with a given size and number of mines.

        Args:
            width (int): The number of cells horizontally.
            height (int): The number of cells vertically.
            num_mines (int): The total number of mines on the board.
        """
        self.width = width  # Number of cells horizontally
        self.height = height  # Number of cells vertically
        self.num_mines = num_mines  # Total number of mines
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]  # Create a 2D grid of Cell objects
        self._place_mines()  # Place mines randomly on the grid
        self._calculate_adjacency()  # Calculate number of adjacent mines for each cell

    def _place_mines(self):
        """
        Randomly places mines on the board.
        """
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)  # Random X position
            y = random.randint(0, self.height - 1)  # Random Y position
            if not self.grid[x][y].is_mine:  # If the cell is not already a mine
                self.grid[x][y].is_mine = True  # Place a mine
                mines_placed += 1

    def _calculate_adjacency(self):
        """
        Calculates the number of adjacent mines for each cell on the board.
        """
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = self._count_adjacent_mines(x, y)

    def _count_adjacent_mines(self, x, y):
        """
        Counts the number of mines adjacent to a given cell.

        Args:
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.

        Returns:
            int: The number of adjacent mines.
        """
        mine_count = 0
        for i in range(max(0, x - 1), min(self.width, x + 2)):  # Check cells around (x, y)
            for j in range(max(0, y - 1), min(self.height, y + 2)):
                if self.grid[i][j].is_mine:
                    mine_count += 1
        return mine_count

    def reveal_cell(self, x, y):
        """
        Reveals a specific cell on the board.

        Args:
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.
        """
        cell = self.grid[x][y]
        if not cell.is_revealed and not cell.is_flagged:
            cell.reveal()
            # If the cell has no adjacent mines, reveal surrounding cells
            if cell.adjacent_mines == 0 and not cell.is_mine:
                self._reveal_adjacent_cells(x, y)

    def _reveal_adjacent_cells(self, x, y):
        """
        Reveals all cells adjacent to a given cell that have no adjacent mines.

        Args:
            x (int): The X-coordinate of the starting cell.
            y (int): The Y-coordinate of the starting cell.
        """
        for i in range(max(0, x - 1), min(self.width, x + 2)):
            for j in range(max(0, y - 1), min(self.height, y + 2)):
                if not self.grid[i][j].is_revealed:
                    self.reveal_cell(i, j)

    def toggle_flag(self, x, y):
        """
        Toggles the flag status of a specific cell.

        Args:
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.
        """
        self.grid[x][y].toggle_flag()

    def check_win(self):
        """
        Checks if the player has won the game by flagging all mines and revealing all non-mine cells.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                if (cell.is_mine and not cell.is_flagged) or (not cell.is_mine and not cell.is_revealed):
                    return False
        return True


# Class representing the overall game
class Game:
    """
    Represents the main Minesweeper game, handling input, drawing, and game logic.

    Attributes:
        width (int): The number of cells horizontally.
        height (int): The number of cells vertically.
        cell_size (int): The size of each cell in pixels.
        mines (int): The total number of mines.
        board (Board): The game board containing all the cells.
        window (Surface): The Pygame window where the game is drawn.
        running (bool): Whether the game is currently running.
        game_over (bool): Whether the game has ended in a loss.
        game_won (bool): Whether the game has ended in a win.
    """
    
    def __init__(self, width=10, height=10, mines=10):
        """
        Initializes the game with a given width, height, and number of mines.

        Args:
            width (int): The number of cells horizontally. Defaults to 10.
            height (int): The number of cells vertically. Defaults to 10.
            mines (int): The number of mines. Defaults to 10.
        """
        pygame.init()  # Initialize pygame
        self.width = width  # Number of cells horizontally
        self.height = height  # Number of cells vertically
        self.cell_size = 40  # Size of each cell in pixels
        self.mines = mines  # Total number of mines
        self.board = Board(width, height, mines)  # Create a board
        # Create a window for the game
        self.window = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        self.running = True  # Game running flag
        self.font = pygame.font.SysFont("Arial", 24)  # Font for displaying text
        self.game_over = False  # Game over flag
        self.game_won = False  # Game won flag
        self._run()  # Start the game loop

    def _run(self):
        """
        Main game loop that handles events and updates the game state.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the user closes the window
                    self.running = False
                # Handle mouse clicks only if the game is not over
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and not self.game_won:
                    self._handle_click(event)

            self._draw()  # Draw the grid and other elements
            pygame.display.flip()  # Update the display

    def _handle_click(self, event):
        """
        Handles mouse clicks, either revealing a cell or flagging it.

        Args:
            event (Event): The Pygame event triggered by a mouse click.
        """
        # Calculate which cell was clicked
        x, y = event.pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size

        if event.button == 1:  # Left-click to reveal
            cell = self.board.grid[grid_x][grid_y]
            if cell.is_mine:
                self.game_over = True  # Game over if clicked on a mine
            else:
                self.board.reveal_cell(grid_x, grid_y)
        elif event.button == 3:  # Right-click to flag
            self.board.toggle_flag(grid_x, grid_y)

        # After each move, check if the player has won
        if self.board.check_win():
            self.game_won = True

    def _draw(self):
        """
        Draws the game elements (grid, cells, flags, etc.) on the Pygame window.
        """
        self.window.fill((255, 255, 255))  # White background

        for x in range(self.width):
            for y in range(self.height):
                cell = self.board.grid[x][y]
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(self.window, (255, 0, 0), rect)  # Red for mines
                    else:
                        pygame.draw.rect(self.window, (200, 200, 200), rect)  # Light gray for revealed cells
                        # Display adjacent mine count if greater than 0
                        if cell.adjacent_mines > 0:
                            text = self.font.render(str(cell.adjacent_mines), True, (0, 0, 0))
                            self.window.blit(text, (x * self.cell_size + 10, y * self.cell_size + 5))
                else:
                    pygame.draw.rect(self.window, (150, 150, 150), rect)  # Dark gray for hidden cells

                if cell.is_flagged:
                    pygame.draw.rect(self.window, (0, 255, 0), rect)  # Green for flagged cells

                pygame.draw.rect(self.window, (0, 0, 0), rect, 1)  # Black border for each cell

        if self.game_over:
            self._draw_game_over()  # Draw game over message if game is over

        if self.game_won:
            self._draw_game_won()  # Draw "YOU WIN!" message if player wins

    def _draw_game_over(self):
        """
        Displays the "Game Over" message when the game is lost.
        """
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width * self.cell_size // 2, self.height * self.cell_size // 2))
        pygame.draw.rect(self.window, (0, 0, 0), text_rect.inflate(10, 10))  # Black background with padding
        self.window.blit(text, text_rect)

    def _draw_game_won(self):
        """
        Displays the "YOU WIN!" message when the game is won.
        """
        text = self.font.render("YOU WIN!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.width * self.cell_size // 2, self.height * self.cell_size // 2))
        pygame.draw.rect(self.window, (0, 0, 0), text_rect.inflate(10, 10))  # Black background with padding
        self.window.blit(text, text_rect)


# Start the game
if __name__ == "__main__":
    Game()
