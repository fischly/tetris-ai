import os.path as path
import pygame


class Background():
    def __init__(self, window_size):
        self.image = pygame.image.load(path.join('gui', 'sprites', 'background-2.jpg'))
        self.image = pygame.transform.scale(self.image, window_size)
        
        
    def draw(self, win):
        # blit(source, dest, area=None, special_flags=0) -> Rect
        win.blit(self.image, (0, 0))