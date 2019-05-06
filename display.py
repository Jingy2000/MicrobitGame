import pygame
from pygame.locals import *


def do_exit():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()  # 为了防止死循环而写的退出函数，可以在主循环里调用


def display(player1, player2, bulletList1, bulletList2):
    screen = pygame.display.set_mode((800, 600), 0, 0)  # 屏幕长宽

    background = pygame.image.load("./image source/background.jpg")  # 背景图片
    p1_img = pygame.image.load("./image source/player1.jpg")  # 人物1，之后可以加判断type来选择图标素材
    p1_img = pygame.transform.scale(p1_img, (30, 30))  # 后面那个tuple是像素大小
    p2_img = pygame.image.load("./image source/player2.jpg")  # 同上
    p2_img = pygame.transform.scale(p2_img, (30, 30))

    p1_pos = (player1.getPos()[0] - 15, player1.getPos()[1] - 15)
    p2_pos = (player2.getPos()[0] - 15, player2.getPos()[1] - 15)
    p1_oppos = (785 - player1.getPos()[0], 585 - player1.getPos()[1])  # 镜像位置
    p2_oppos = (785 - player2.getPos()[0], 585 - player2.getPos()[1])

    hp_img = pygame.image.load("./image source/hpc.jpg")
    hp_img = pygame.transform.scale(hp_img, (202, 27))
    hp1_img = pygame.image.load("./image source/hp1.jpg")
    hp1_img = pygame.transform.scale(hp1_img, (2 * player1.hp, 25))
    hp2_img = pygame.image.load("./image source/hp2.jpg")
    hp2_img = pygame.transform.scale(hp2_img, (2 * player2.hp, 25))

    screen.blit(background, (0, 0))  # 绘制背景

    screen.blit(hp_img, (10, 10))
    screen.blit(hp1_img, (11, 11))
    screen.blit(hp_img, (10, 563))
    screen.blit(hp2_img, (11, 564))
    screen.blit(hp_img, (574, 10))
    screen.blit(hp2_img, (575, 11))
    screen.blit(hp_img, (574, 563))
    screen.blit(hp1_img, (575, 564))


    screen.blit(p1_img, p1_pos)  # p1
    screen.blit(p1_img, p1_oppos)  # p1镜像
    screen.blit(p2_img, p2_pos)
    screen.blit(p2_img, p2_oppos)



    for bullet in bulletList1:
        blt_pos = (bullet.getPos()[0] - 10, bullet.getPos()[1] - 10)
        blt_oppos = (790 - bullet.getPos()[0], 590 - bullet.getPos()[1])  # 子弹的镜像位置
        blt_img = pygame.image.load("./image source/bullet22.jpg")  # 之后可以加子弹类型判断图片
        blt_img = pygame.transform.scale(blt_img, (20, 20))  # 大小
        # blt_img = pygame.transform.rotate(blt_img, -bullet.angle)  # 旋转
        screen.blit(blt_img, blt_pos)
        # blt_img = pygame.transform.rotate(blt_img, 180)  # 比刚才那个再转180°
        screen.blit(blt_img, blt_oppos)
    for bullet in bulletList2:
        blt_pos = (bullet.getPos()[0] - 10, bullet.getPos()[1] - 10)
        blt_oppos = (790 - bullet.getPos()[0], 590 - bullet.getPos()[1])  # 子弹的镜像位置
        blt_img = pygame.image.load("./image source/bullet11.jpg")
        blt_img = pygame.transform.scale(blt_img, (20, 20))
        # blt_img = pygame.transform.rotate(blt_img, - bullet.angle)
        screen.blit(blt_img, blt_pos)
        # blt_img = pygame.transform.rotate(blt_img, 180)
        screen.blit(blt_img, blt_oppos)

    pygame.display.update()
