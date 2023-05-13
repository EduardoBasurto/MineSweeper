import pygame
import board
import numpy as np
import cell

class GUI(board.Board):
    def __init__(self, size, mines):
        super().__init__(size, mines)
        self.size = (800, 600)
        self.colors = {
            'BLACK' : (0, 0, 0),
            'WHITE' : (255, 255, 255),
            'GREY' : (192, 192, 192),
            'RED' : (255, 0, 0),
            'GREEN' : (0, 255, 0),
            'BLUE' : (0, 0, 255),
            'YELLOW' : (250, 253, 15)
        }
        self.flags = mines
        self.bomb_img = r'img\bomb.png'
        self.flag_img = r'img\flag.png'
        self.square_size = 50
        self.font_size = 30
        self.graphic_board = np.empty((self.grid_size, self.grid_size), dtype=object)
        self.generate_mines()
        self.create_board()
        self.create_graphic_board()
        self.__init_pygame__()

    def create_graphic_board(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                self.graphic_board[row][column] = cell.Cell(row, column, self.grid[row][column])
    
    def __init_pygame__(self):
        pygame.init()
        # Set the width and height of the screen
        self.screen = pygame.display.set_mode(self.size)
        bomb = pygame.image.load(self.bomb_img)
        self.bomb = pygame.transform.scale(bomb, (self.square_size,self.square_size))
        flag = pygame.image.load(self.flag_img)
        self.flag = pygame.transform.scale(flag, (self.square_size,self.square_size))
        # Set the caption of the window
        pygame.display.set_caption("Minesweeper")
        # Set the size of each square on the grid
        self.font = pygame.font.SysFont('Arial', self.font_size)

    def start_gui(self):
        # Loop until the user clicks the close button
        done = False
        game_over = False

        while not done:
            # --- Event Processing ---
            for event in pygame.event.get():
                done = self.__event_hanlder__(event)

            # --- Draw the grid ---
            for row in range(self.grid_size):
                for column in range(self.grid_size):
                    # Calculate the position of the square on the screen
                    x = column * self.square_size
                    y = row * self.square_size

                    # Draw the square
                    pygame.draw.rect(self.screen, self.colors.get('GREY'), [x, y, self.square_size, self.square_size], 1)

                    cell_color = self.colors.get('BLACK')
                    if self.graphic_board[row][column].state == 'UNCLICKED':
                        pygame.draw.rect(self.screen, self.colors.get('GREY'), [x+5, y+5, self.square_size-6, self.square_size-6], 0)
                    elif self.graphic_board[row][column].state == 'CLICKED':
                        if self.grid[row][column] == 0:
                            pygame.draw.rect(self.screen, self.colors.get('WHITE'), [x, y, self.square_size, self.square_size], 0)
                        if self.grid[row][column] == 1:
                            cell_color = self.colors.get('BLUE')
                            number = self.font.render(str(self.grid[row][column]), True, cell_color)
                            self.screen.blit(number, (x + self.square_size/2 - number.get_width()/2, y + self.square_size/2 - number.get_height()/2))
                        elif self.grid[row][column] == 2:
                            cell_color = self.colors.get('GREEN')
                            number = self.font.render(str(self.grid[row][column]), True, cell_color)
                            self.screen.blit(number, (x + self.square_size/2 - number.get_width()/2, y + self.square_size/2 - number.get_height()/2))
                        elif self.grid[row][column] == 3:
                            cell_color = self.colors.get('YELLOW')
                            number = self.font.render(str(self.grid[row][column]), True, cell_color)
                            self.screen.blit(number, (x + self.square_size/2 - number.get_width()/2, y + self.square_size/2 - number.get_height()/2))
                        elif self.grid[row][column] == 4:
                            cell_color = self.colors.get('RED')
                            number = self.font.render(str(self.grid[row][column]), True, cell_color)
                            self.screen.blit(number, (x + self.square_size/2 - number.get_width()/2, y + self.square_size/2 - number.get_height()/2))
                    elif self.graphic_board[row][column].state == 'SAVED':
                        self.screen.blit(self.flag, (x, y))
            # --- Update the screen ---
            pygame.display.flip()

        # Close the window and quit.
        pygame.quit()


    def __event_hanlder__(self, event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            column = pos[0] // self.square_size
            row = pos[1] // self.square_size

            # left click
            if event.button == 1:
                self.graphic_board[row][column].click_cell()
                if self.grid[row][column] == 'X':
                    self.screen.blit(self.bomb, (column * self.square_size, row * self.square_size))
                    game_over = True
                    print('You clicked on a mine!')
                else:
                    print('You clicked on an empty square.')
            elif event.button == 3 and self.graphic_board[row][column].state == 'UNCLICKED' and self.flags>0:
                self.graphic_board[row][column].save_cell()
                self.flags -= 1
            elif event.button == 3 and self.graphic_board[row][column].state == 'SAVED' and self.flags<=self.number_of_mines:
                self.graphic_board[row][column].unclick_cell()
                self.flags += 1
        return False
