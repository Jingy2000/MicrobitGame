import pygame
from pygame.locals import *


def do_exit():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()  # 为了防止死循环而写的退出函数，可以在主循环里调用


def display(player1, player2, bulletList1, bulletList2):
    screen = pygame.display.set_mode((800, 600), 0, 0)  # 屏幕长宽

    background = pygame.image.load("./image source/background.png")  # 背景图片
    p1_img = pygame.image.load("./image source/0.jpg")  # 人物1，之后可以加判断type来选择图标素材
    p1_img = pygame.transform.scale(p1_img, (30, 40))  # 后面那个tuple是像素大小
    p2_img = pygame.image.load("./image source/1.jpg")  # 同上
    p2_img = pygame.transform.scale(p2_img, (30, 40))

    p1_oppos = (770 - player1.getPos()[0], 560 - player1.getPos()[1])  # 镜像位置
    p2_oppos = (770 - player2.getPos()[0], 560 - player2.getPos()[1])

    screen.blit(background, (0, 0))  # 绘制背景
    screen.blit(p1_img, player1.getPos())  # p1
    screen.blit(p1_img, p1_oppos)  # p1镜像
    screen.blit(p2_img, player2.getPos())
    screen.blit(p2_img, p2_oppos)

    for bullet in bulletList1:
        blt_oppos = (800 - bullet.getPos()[0], 600 - bullet.getPos()[1])  # 子弹的镜像位置（未考虑子弹图片大小）
        blt_img = pygame.image.load("./image source/bullet.jpg")  # 之后可以加子弹类型判断图片
        blt_img = pygame.transform.scale(blt_img, (32, 8))  # 大小
        blt_img = pygame.transform.rotate(blt_img, -bullet.angle)  # 旋转
        screen.blit(blt_img, bullet.getPos())
        blt_img = pygame.transform.rotate(blt_img, 180)  # 比刚才那个再转180°
        screen.blit(blt_img, blt_oppos)
    for bullet in bulletList2:
        blt_oppos = (800 - bullet.getPos()[0], 600 - bullet.getPos()[1])
        blt_img = pygame.image.load("./image source/bullet.jpg")
        blt_img = pygame.transform.scale(blt_img, (32, 8))
        blt_img = pygame.transform.rotate(blt_img, - bullet.angle)
        screen.blit(blt_img, bullet.getPos())
        blt_img = pygame.transform.rotate(blt_img, 180)
        screen.blit(blt_img, blt_oppos)

    pygame.display.update()
