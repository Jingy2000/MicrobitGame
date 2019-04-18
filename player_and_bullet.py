from math import sin, cos, sqrt
import pygame


class Bullet:
    def __init__(self, type, pos, angle, v, size=(1, 1), rebound=False, damage=10):
        self.type = type
        self.__pos = pos
        self.angle = angle
        self.v = v
        self.size = size
        self.rebound = rebound
        self.damage = damage

        self.alive = True
        # self.visible=100 # 透明度，不知道要不要加

    def getPos(self):
        return self.__pos

    def move(self):
        self.__pos = (self.__pos[0] + self.v * cos(self.angle),
                      self.__pos[1] + self.v * sin(self.angle))
        # 这里还可以判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.__pos[0] - player.pos[0]) ** 2 + (self.__pos[1] - player.pos[1]) ** 2)
        if distance < (self.hit_radius + player.hit_radius):
            player.subHp(self.damage)
            return True
        return False

    def is_alive(self):
        return self.alive


class Player:

    def __init__(self, y):
        self.hp = 100
        self.energy = 0
        self.skillReady = False
        self.__pos = (0, y)
        self.hit_radius = 3
        self.state = 's'  # 静止
        self.v = 1

    def updatePos(self):
        if self.state == 'l':
            self.__pos -= self.v
        elif self.state == 'r':
            self.__pos += self.v

    def getPos(self):
        return self.__pos

    def subHp(self, n=1):
        self.hp -= n

    def is_alive(self):
        return self.hp > 0

    def updateEnergy(self):
        self.energy += 1
        return self.energy

    # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成
    def attack(self, bulletType):
        # waittime = 10  # 前摇，到时候调整,需要时间等待
        bullet1 = Bullet(type=bulletType, angle=-25, pos=self.__pos)
        bullet2 = Bullet(type=bulletType, angle=0, pos=self.__pos)
        bullet3 = Bullet(type=bulletType, angle=25, pos=self.__pos)
        return bullet1, bullet2, bullet3

