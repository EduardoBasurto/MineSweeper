import random, pygame, cell, util, sys

class Board():
    def __init__(self, grid_size, number_of_mines):
        self.grid_size = grid_size
        self.number_of_mines = number_of_mines
        self.mines_loc = []
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
        self.flags = number_of_mines
        self.square_size = 50
        self.font_size = 30
        self.done = False
        self.game_over = False
        self.win = False
        self.generate_mines()
        self.create_board()
        self.set_neighbors()
        self.__init_pygame__()

    
    def __init_pygame__(self):
        pygame.init()
        # Set the width and height of the screen
        self.screen = pygame.display.set_mode(self.size)
        # Set the caption of the window
        pygame.display.set_caption("Minesweeper")
        # Set the size of each square on the grid
        self.font = pygame.font.SysFont('Arial', self.font_size)

    def __game_lost__(self):
        pygame.init()
        # Set the width and height of the screen
        self.screen = pygame.display.set_mode((400,300))
        # Set the caption of the window
        pygame.display.set_caption("GAME OVER")
        # Set the size of each square on the grid
        self.font = pygame.font.SysFont('Arial', self.font_size)
        text = self.font.render('GAME OVER!', True, self.colors.get('WHITE'))
        self.screen.blit(text, (0, 0))

    def __event_hanlder__(self, event):
        try:
            pos = pygame.mouse.get_pos()
            column = pos[0] // self.square_size
            row = pos[1] // self.square_size
            # left click
            if event.button == 1:
                self.graphic_board[row][column].clicked_cell()
                if self.graphic_board[row][column].bombed:
                    self.screen.blit(util.Bomb(self.square_size).bomb, (column * self.square_size, row * self.square_size))
                    raise util.GameOver()
                if self.graphic_board[row][column].content == 0:
                    self.collapse_neighbors(self.graphic_board[row][column])
            elif event.button == 3 and (not self.graphic_board[row][column].clicked) and self.flags>0:
                self.graphic_board[row][column].saved_cell()
                self.flags -= 1
            elif event.button == 3 and self.graphic_board[row][column].flagged and self.flags<=self.number_of_mines:
                self.graphic_board[row][column].unclicked_cell()
                self.flags += 1
            self.has_game_been_won()
        except IndexError:
            pass
        except util.GameOver:
            self.game_over = True

    def generate_mines(self):
        while len(self.mines_loc) < self.number_of_mines:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if (x,y) not in self.mines_loc:
                self.mines_loc.append((x,y))

    def create_board(self,):
        self.graphic_board = [[cell.Cell(row, column) for row in range(self.grid_size)] for column in range(self.grid_size)]
        for mine in self.mines_loc:
            x = mine[0]
            y = mine[1]
            self.graphic_board[y][x].bombed_cell()
            if (x >=0 and x <= self.grid_size-2) and (y >= 0 and y <= self.grid_size-1):
                if self.graphic_board[y][x+1].content != 'X':
                    self.graphic_board[y][x+1].add_one() # center right
            if (x >=1 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-1):
                if self.graphic_board[y][x-1].content != 'X':
                    self.graphic_board[y][x-1].add_one() # center left
            if (x >= 1 and x <= self.grid_size-1) and (y >= 1 and y <= self.grid_size-1):
                if self.graphic_board[y-1][x-1].content != 'X':
                    self.graphic_board[y-1][x-1].add_one() # top left
            if (x >= 0 and x <= self.grid_size-2) and (y >= 1 and y <= self.grid_size-1):
                if self.graphic_board[y-1][x+1].content != 'X':
                    self.graphic_board[y-1][x+1].add_one() # top right
            if (x >= 0 and x <= self.grid_size-1) and (y >= 1 and y <= self.grid_size-1):
                if self.graphic_board[y-1][x].content != 'X':
                    self.graphic_board[y-1][x].add_one() # top center
            if (x >=0 and x <= self.grid_size-2) and (y >= 0 and y <= self.grid_size-2):
                if self.graphic_board[y+1][x+1].content != 'X':
                    self.graphic_board[y+1][x+1].add_one() # bottom right
            if (x >= 1 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-2):
                if self.graphic_board[y+1][x-1].content != 'X':
                    self.graphic_board[y+1][x-1].add_one() # bottom left
            if (x >= 0 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-2):
                if self.graphic_board[y+1][x].content != 'X':
                    self.graphic_board[y+1][x].add_one() # bottom center


    def draw_grid(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                # Calculate the position of the square on the screen
                x = column * self.square_size
                y = row * self.square_size
                # Draw the square
                pygame.draw.rect(self.screen, self.colors.get('GREY'), [x, y, self.square_size, self.square_size], 1)
                if not self.graphic_board[row][column].clicked:
                    pygame.draw.rect(self.screen, self.colors.get('GREY'), [x+5, y+5, self.square_size-6, self.square_size-6], 0)
                elif self.graphic_board[row][column].clicked and not self.graphic_board[row][column].flagged:
                    if self.graphic_board[row][column].content == 0:
                        pygame.draw.rect(self.screen, self.colors.get('WHITE'), [x, y, self.square_size, self.square_size], 0)
                    if self.graphic_board[row][column].content in [1,2,3,4]:
                        #cell_color = self.color_numbers.get(self.graphic_board[row][column].content)
                        number = self.font.render(str(self.graphic_board[row][column].content), True, self.graphic_board[row][column].get_color())
                        self.screen.blit(number, (x + self.square_size/2 - number.get_width()/2, y + self.square_size/2 - number.get_height()/2))
                elif self.graphic_board[row][column].clicked and self.graphic_board[row][column].flagged:
                    self.screen.blit(util.Flag(self.square_size).flag, (x, y))   

        # --- Update the screen ---
        pygame.display.flip()

    def set_neighbors(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                neighbors = [
                    (row-1, column-1), (row-1, column), (row-1, column+1),
                    (row, column-1),             (row, column+1),
                    (row+1, column-1), (row+1, column), (row+1, column+1),
                ]
                # filter out-of-bounds neighbors
                neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.grid_size and 0 <= y < self.grid_size]
                self.graphic_board[row][column].set_neighbors(neighbors)


    def collapse_neighbors(self, cell):
        for neighbor in cell.neighbors:
            x,y = neighbor
            if not self.graphic_board[x][y].clicked:
                if self.graphic_board[x][y].content == 0 :
                    self.graphic_board[x][y].clicked_cell()
                    self.collapse_neighbors(self.graphic_board[x][y])
                elif self.graphic_board[x][y].content in [1,2,3,4]:
                    self.graphic_board[x][y].clicked_cell()
        return

    def run_game(self):
        self.draw_grid()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.__event_hanlder__(event)
                    self.draw_grid()
            if self.game_over:
                self.show_game_over_screen()

        # Close the window and quit.
        pygame.quit()

    def has_game_been_won(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                if not self.graphic_board[row][column].clicked:
                    return
        self.game_over = True
        self.win = True

    def show_game_over_screen(self):
        # Initialize pygame and create the screen
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Over")

        # Define the font and text to display based on whether the player won or lost
        font = pygame.font.SysFont(None, 48)
        ending_text = 'You win!' if self.win else 'Game over!'
        text = font.render(ending_text, True, (255, 255, 255))

        # Display the text in the center of the screen
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        # Update the screen and wait for the player to click a button
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    return
                elif event.type == pygame.KEYDOWN:
                    waiting = False
