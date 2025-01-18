import pygame
from pygame.locals import *


width = 600
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height))
square_size = (25, 25)
square_color = (0, 200, 255)
squares = [pygame.Rect(40, 40, *square_size), pygame.Rect(40, 530, *square_size),
           pygame.Rect(500, 40, *square_size), pygame.Rect(500, 530, *square_size)]


gameOn = True

while gameOn:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                gameOn = False

        elif event.type == QUIT:
            gameOn = False

    screen.fill((0, 0, 0))
    for square in squares:
        pygame.draw.rect(screen, square_color, square)
    pygame.display.flip()
