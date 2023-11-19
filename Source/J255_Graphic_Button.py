import pygame
import time

from J255_Variable import (DeclaredVariable,
                           SetVariableValue)

class Button:
    def __init__(self, screen, color, x: int, y: int, width: int, height: int, flagVariable: str):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(screen, color, (x, y, width, height))

        if x <= mouse[0] <= x + width and y <= mouse[1] <= y + height and click[0] and DeclaredVariable(flagVariable):
            time.sleep(0.1)

            SetVariableValue(flagVariable, True)