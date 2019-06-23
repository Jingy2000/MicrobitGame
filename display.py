import pygame
from pygame.locals import *
from image_type import MAX_BULLET_TYPE


def do_exit():
    pass  # 为了防止死循环而写的退出函数，可以在主循环里调用


def display_init():
    global screen, p1_img, p2_img, background, hp1_img, hp2_img, mp1_img, mp2_img, blt_imgs
    screen = pygame.display.set_mode((800, 600), 0, 0)  # 屏幕长宽
    p1_img = pygame.image.load("./image source/player1.png")  # 人物1，之后可以加判断type来选择图标素材
    p2_img = pygame.image.load("./image source/player2.png")  # 同上
    p1_img = pygame.transform.scale(p1_img, (30, 30))  # 后面那个tuple是像素大小
    p2_img = pygame.transform.scale(p2_img, (30, 30))
    background = pygame.image.load("./image source/background.png")  # 背景图片
    hp1_img = pygame.image.load("./image source/hp1.jpg")
    hp2_img = pygame.image.load("./image source/hp2.jpg")
    mp1_img = pygame.image.load("./image source/mp1.jpg")
    mp2_img = pygame.image.load("./image source/mp2.jpg")
    hp1_img = pygame.transform.scale(hp1_img, (8, 590))
    hp2_img = pygame.transform.scale(hp2_img, (8, 590))

    mp1_img = pygame.transform.scale(mp1_img, (8, 590))
    mp2_img = pygame.transform.scale(mp2_img, (8, 590))

    blt_imgs = []

    for i in range(MAX_BULLET_TYPE):
        blt_imgs.append(pygame.image.load("./image source/bullet{}.jpg".format(str(i))))  # 之后可以加子弹类型判断图片
        blt_imgs[i] = pygame.transform.scale(blt_imgs[i], (20, 20))


def display(player1, player2, bulletList1, bulletList2):
    global screen, p1_img, p2_img, background, hp1_img, hp2_img, mp1_img, mp2_img, blt_imgs

    p1_pos = (player1.getPos()[0] - 15, player1.getPos()[1] - 15)
    p2_pos = (player2.getPos()[0] - 15, player2.getPos()[1] - 15)
    p1_oppos = (785 - player1.getPos()[0], 585 - player1.getPos()[1])  # 镜像位置
    p2_oppos = (785 - player2.getPos()[0], 585 - player2.getPos()[1])
    #
    # hp1_img = pygame.transform.scale(hp1_img, (8, int(590 * player1.hp / 100)))
    # hp2_img = pygame.transform.scale(hp2_img, (8, int(590 * player2.hp / 100)))
    #
    # mp1_img = pygame.transform.scale(mp1_img, (8, int(590 * player1.energy.ratio())))
    # mp2_img = pygame.transform.scale(mp2_img, (8, int(590 * player2.energy.ratio())))

    screen.blit(background, (0, 0))  # 绘制背景

    screen.blit(hp1_img, (403, 595 - int(590 * player1.hp.ratio())))
    screen.blit(hp2_img, (390, 595 - int(590 * player2.hp.ratio())))

    screen.blit(mp1_img, (793, 595 - int(590 * player1.power.ratio())))
    screen.blit(mp2_img, (0, 595 - int(590 * player2.power.ratio())))

    screen.blit(p1_img, p1_pos)  # p1
    screen.blit(p1_img, p1_oppos)  # p1镜像
    screen.blit(p2_img, p2_pos)
    screen.blit(p2_img, p2_oppos)

    for bullet in bulletList1:
        blt_pos = (bullet.getPos()[0] - 10, bullet.getPos()[1] - 10)
        blt_oppos = (790 - bullet.getPos()[0], 590 - bullet.getPos()[1])  # 子弹的镜像位置
        # blt_img = pygame.transform.rotate(blt_img, -bullet.angle)  # 旋转
        screen.blit(blt_imgs[bullet.type], blt_pos)
        # blt_img = pygame.transform.rotate(blt_img, 180)  # 比刚才那个再转180°
        screen.blit(blt_imgs[bullet.type], blt_oppos)
    for bullet in bulletList2:
        blt_pos = (bullet.getPos()[0] - 10, bullet.getPos()[1] - 10)
        blt_oppos = (790 - bullet.getPos()[0], 590 - bullet.getPos()[1])  # 子弹的镜像位置
        # blt_img = pygame.transform.rotate(blt_img, - bullet.angle)
        screen.blit(blt_imgs[bullet.type], blt_pos)
        # blt_img = pygame.transform.rotate(blt_img, 180)
        screen.blit(blt_imgs[bullet.type], blt_oppos)

    pygame.display.update()
