import random

class Board():

    def __init__(self, grid_size, number_of_mines):
        self.grid_size = grid_size
        self.number_of_mines = number_of_mines

    def generate_mines(self,):
        self.mines_loc = []
        while len(self.mines_loc) < self.number_of_mines:
            x = random.randint(0,self.grid_size-1)
            y = random.randint(0,self.grid_size-1)
            if (x,y) not in self.mines_loc:
                self.mines_loc.append((x,y))
                print("Mine generated in location: {0},{1}".format(x,y))

    def create_board(self,):
        arr = [[0 for row in range(self.grid_size)] for column in range(self.grid_size)]
        for mine in self.mines_loc:
            x = mine[0]
            y = mine[1]
            arr[y][x] = 'X'

            if (x >=0 and x <= self.grid_size-2) and (y >= 0 and y <= self.grid_size-1):
                if arr[y][x+1] != 'X':
                    arr[y][x+1] += 1 # center right
            if (x >=1 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-1):
                if arr[y][x-1] != 'X':
                    arr[y][x-1] += 1 # center left
            if (x >= 1 and x <= self.grid_size-1) and (y >= 1 and y <= self.grid_size-1):
                if arr[y-1][x-1] != 'X':
                    arr[y-1][x-1] += 1 # top left

            if (x >= 0 and x <= self.grid_size-2) and (y >= 1 and y <= self.grid_size-1):
                if arr[y-1][x+1] != 'X':
                    arr[y-1][x+1] += 1 # top right
            if (x >= 0 and x <= self.grid_size-1) and (y >= 1 and y <= self.grid_size-1):
                if arr[y-1][x] != 'X':
                    arr[y-1][x] += 1 # top center

            if (x >=0 and x <= self.grid_size-2) and (y >= 0 and y <= self.grid_size-2):
                if arr[y+1][x+1] != 'X':
                    arr[y+1][x+1] += 1 # bottom right
            if (x >= 1 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-2):
                if arr[y+1][x-1] != 'X':
                    arr[y+1][x-1] += 1 # bottom left
            if (x >= 0 and x <= self.grid_size-1) and (y >= 0 and y <= self.grid_size-2):
                if arr[y+1][x] != 'X':
                    arr[y+1][x] += 1 # bottom center

        for row in arr:
            print(" ".join(str(cell) for cell in row))
