import pygame 

class Bomb():
    def __init__(self, square_size):
        self.url = r'img\bomb.png' 
        pygame.init()
        bomb =  pygame.image.load(self.url)
        self.bomb = pygame.transform.scale(bomb, (square_size,square_size))

class Flag():
    def __init__(self, square_size):
        self.url = r'img\flag.png'
        pygame.init()
        flag =  pygame.image.load(self.url)
        self.flag = pygame.transform.scale(flag, (square_size,square_size))

class GameOver(Exception):

    def __init__(self, message='You lost!'):
        self.message = message
        super().__init__(self.message)