import sys
import os
from unittest.mock import patch, Mock
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from mem_679_minesweeper_jo_2.game import Game, Cell, Board

def test_cell_reveal():
    # Test revealing a cell
    cell = Cell(0, 0)
    assert not cell.is_revealed
    cell.reveal()
    assert cell.is_revealed

def test_flag_toggle():
    # Test flagging and unflagging a cell
    cell = Cell(0, 0)
    assert not cell.is_flagged
    cell.toggle_flag()
    assert cell.is_flagged
    cell.toggle_flag()
    assert not cell.is_flagged

def test_place_mines():
    # Test placing the correct number of mines
    board = Board(5, 5, 5)  # Create a 5x5 board with 5 mines
    mine_count = sum(1 for x in range(5) for y in range(5) if board.grid[x][y].is_mine)
    assert mine_count == 5

def test_adjacent_mine_count():
    # Test correct calculation of adjacent mines
    board = Board(3, 3, 0)  # Create a 3x3 board with 0 mines
    board.grid[1][1].is_mine = True  # Place a mine manually in the center
    board._calculate_adjacency()
    assert board.grid[0][0].adjacent_mines == 1  # The corner should have 1 adjacent mine
    assert board.grid[1][1].adjacent_mines == 0  # The mine itself should have 0 adjacent mines
    assert board.grid[0][1].adjacent_mines == 1  # Adjacent cells should reflect mine count

# Mock Pygame's display and surface to avoid graphical operations
@patch('mem_679_minesweeper_jo_2.game.pygame.display.set_mode')
@patch('mem_679_minesweeper_jo_2.game.Game._run')  # Prevent the game loop from running
def test_game_over_on_mine_click(mock_run, mock_set_mode):
    # Mock set_mode to return a real Pygame surface (not a mock)
    mock_set_mode.return_value = pygame.Surface((300, 300))  # Create a fake 300x300 surface

    print("Creating game...")
    game = Game(width=3, height=3, mines=1)

    # Manually place a mine in a known location
    game.board.grid[0][0].is_mine = True
    print("Placed mine at (0, 0).")

    # Log the initial state of the board
    print(f"Initial game_over state: {game.game_over}")

    # Simulate a click event
    print("Simulating click event at (0, 0)...")
    game._handle_click(event=type('obj', (object,), {'pos': (0, 0), 'button': 1}))  # Simulate left-click

    # Log the state after the click
    print(f"Game over state after click: {game.game_over}")

    assert game.game_over

# Patch the game loop for this test as well
@patch('mem_679_minesweeper_jo_2.game.pygame.display.set_mode')
@patch('mem_679_minesweeper_jo_2.game.Game._run')  # Prevent the game loop from running
def test_flagging_a_mine(mock_run, mock_set_mode):
    # Mock set_mode to return a real Pygame surface (not a mock)
    mock_set_mode.return_value = pygame.Surface((300, 300))  # Create a fake 300x300 surface

    # Test that flagging a mine correctly works
    game = Game(width=3, height=3, mines=1)
    game.board.grid[0][0].is_mine = True
    game.board.toggle_flag(0, 0)  # Simulate flagging the mine
    print(f"Cell is_flagged after flagging: {game.board.grid[0][0].is_flagged}")  # Add this print statement
    assert game.board.grid[0][0].is_flagged  # Check if the flagging worked

# Patch the game loop for this test as well
@patch('mem_679_minesweeper_jo_2.game.pygame.display.set_mode')
@patch('mem_679_minesweeper_jo_2.game.Game._run')  # Prevent the game loop from running
def test_win_condition(mock_run, mock_set_mode):
    # Mock set_mode to return a real Pygame surface (not a mock)
    mock_set_mode.return_value = pygame.Surface((300, 300))  # Create a fake 300x300 surface

    # Test winning the game by flagging all mines
    game = Game(width=3, height=3, mines=1)
    game.board.grid[0][0].is_mine = True

    # Flag the mine
    game.board.toggle_flag(0, 0)  # Flag the only mine
    print(f"Flagged mine: {game.board.grid[0][0].is_flagged}")

    # Reveal all non-mine cells
    for x in range(1, 3):
        for y in range(3):
            game._handle_click(event=type('obj', (object,), {'pos': (x, y), 'button': 1}))  # Simulate click
    
    # Log the revealed cells for verification
    revealed_cells = [(x, y) for x in range(3) for y in range(3) if game.board.grid[x][y].is_revealed]
    print(f"Revealed cells: {revealed_cells}")
    
    # Check if the win condition is met
    print(f"Game won: {game.game_won}")
    assert game.game_won
