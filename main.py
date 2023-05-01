from board import Board

if __name__ == "__main__":
    grid_size = 5
    difficulty = {'easy':5, 'medium':10, 'hard': 15, 'expert':20}
    selected_difficulty = 'expert'
    board = Board(10,difficulty.get(selected_difficulty))
    board.generate_mines()
    board.create_board()
