import pygame 

class Bomb():
    def __init__(self):
        self.url = r'img\bomb.png' 
        pygame.init()
        self.bomb =  pygame.image.load(self.url)

class Flag():
    def __init__(self):
        self.url = r'img\flag.png'
        pygame.init()
        self.flag =  pygame.image.load(self.url)


class Cell():

    def __init__(self, row, column, content):
        self.row = row
        self.column = column
        self.content = Bomb().bomb if content == 'X' else content
        self.state = 'UNCLICKED'

    def click_cell(self):
        self.state = 'CLICKED'

    def bombed(self):
        self.state = 'CLICKED'
        self.content = Bomb().bomb

    def unclick_cell(self):
        self.state = 'UNCLICKED'

    def save_cell(self):
        self.state = 'SAVED'
        self.content = Flag().flag