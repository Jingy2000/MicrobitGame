import pygame
from pygame.locals import *
import time


def do_exit():
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit()")
            exit()


def display(player1, player2, bulletList1, bullestList2):
    screen = pygame.display.set_mode((800, 600), 0, 0)
    background = pygame.image.load("./image source/background.png")
    p1_img = pygame.image.load("./image source/0.jpg")
    p2_img = pygame.image.load("./image source/1.jpg")
    screen.blit(background, (0, 0))
    screen.blit(p1_img, (140, 400))
    screen.blit(p2_img, (440, 400))

    while True:  # 这个循环体和后面的sleep之后要删掉，这里是我为了保留窗口看效果用的
        do_exit()
        pygame.display.update()
        time.sleep(0.033)


display(1, 1, 1, 1)
