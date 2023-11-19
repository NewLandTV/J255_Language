import pygame

from J255_Graphic_Button import Button
from J255_Variable import (GetVariableValue,
                           SetVariableValue,
                           DeclaredVariable)

screen: pygame.Surface = None

clock = pygame.time.Clock()

# Execute graphic(pygame) function with arguments
def ExecuteG(args: list[str]):
    global screen

    args = args[1].split(" ", 1)
    
    if args[0] == "init":
        pygame.init()
        pygame.display.set_icon(pygame.image.load("./DefaultIcon.png"))
    elif args[0] == "display":
        datas = args[1].split(", ", 1)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        screen = pygame.display.set_mode([float(datas[0]), float(datas[1])])
    elif args[0] == "title":
        pygame.display.set_caption(args[1])
    elif args[0] == "tick":
        clock.tick(GetVariableValue(args[1]) if DeclaredVariable(args[1]) else int(args[1]))
    elif args[0] == "eventloop":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SetVariableValue(args[1], bool(False))
    elif args[0] == "background":
        datas = args[1].split(", ", 2)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        screen.fill((int(datas[0]), int(datas[1]), int(datas[2])))
    elif args[0] == "flip":
        pygame.display.flip()

    elif args[0] == "line":
        datas = args[1].split(", ", 7)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        pygame.draw.line(screen, (int(datas[0]), int(datas[1]), int(datas[2])), [int(datas[3]), int(datas[4])], [int(datas[5]), int(datas[6])], int(datas[7]))
    elif args[0] == "image":
        datas = args[1].split(", ", 4)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        image = pygame.image.load(datas[0])

        image = pygame.transform.scale(image, (int(datas[3]), int(datas[4])))

        screen.blit(image, (int(datas[1]), int(datas[2])))
    elif args[0] == "text":
        datas = args[1].split(", ", 6)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        font = pygame.font.SysFont("Liberation Sans", int(datas[6]), False, False)

        text = font.render(str(datas[0]), True, (int(datas[1]), int(datas[2]), int(datas[3])))

        screen.blit(text, (int(datas[4]), int(datas[5])))
    elif args[0] == "button":
        datas = args[1].split(", ", 7)

        for i in range(0, len(datas) - 1):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        Button(screen, (int(datas[0]), int(datas[1]), int(datas[2])), int(datas[3]), int(datas[4]), int(datas[5]), int(datas[6]), datas[7])