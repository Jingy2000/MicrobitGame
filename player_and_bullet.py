from math import sin, cos, sqrt, pi, radians, atan
from image_type import *


class Bullet:
    def __init__(self, type, pos, angle, v=10, size=(1, 1), rebound=False, damage=10):
        self.type = type
        self.__pos = pos
        self.angle = angle
        self.v = v
        self.size = size
        self.rebound = rebound
        self.damage = damage

        self.hit_radius = 5

        self.alive = True
        # self.visible=100 # 透明度，不知道要不要加

    def getPos(self):
        return self.__pos

    def move(self, ):
        self.__pos = (self.__pos[0] + self.v * cos(radians(self.angle)),
                      self.__pos[1] + self.v * sin(radians(self.angle)))
        # 这里还可以判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.__pos[0] - player.getPos()[0]) ** 2 + (self.__pos[1] - player.getPos()[1]) ** 2)
        eff_radius = (self.hit_radius * sqrt(self.size[0] ** 2 + self.size[1] ** 2) + player.hit_radius)
        if distance < eff_radius:
            player.subHp(self.damage)
            return True
        return False

    def is_alive(self):
        return self.alive


class Power:
    def __init__(self, max):
        self.length = 0
        self.max = max
        self.v = 1  # 自动回复的速度
        self.is_ready = False

    def update(self):
        if self.length < self.max:
            self.length += self.v
        else:
            self.is_ready = True
        return self.length / self.max  # 返回一个比值，用来显示在microbit上

    def clear(self):
        self.length = 0
        self.is_ready = False


class Player:

    def __init__(self, y, angle):
        self.hp = 100
        self.energy = Power(100)
        self.power = Power(10)
        self.vmax = 10
        self.__direction = (0, 0)  # 方向是手柄给出的方向，上-，左-
        self.__pos = (200, y)
        self.angle = angle  # 0-360,90是向上
        self.hit_radius = 3
        self.type = 'bullet_round'
        self.enemy = None

    def move(self):
        if self.__direction == (0, 0):
            pass
        else:
            current = self.__pos
            direction = self.__direction
            x, y = direction[0], direction[1]
            rmax = 2048
            pos_x, pos_y = current[0] - self.vmax * x / rmax * sin(radians(self.angle)), current[
                1] - self.vmax * y / rmax * sin(radians(self.angle))
            # 人物出屏幕(考虑两个玩家角度不一样，对应范围也不一样）
            if pos_x < 0:
                pos_x = 0
            if pos_x > 400:
                pos_x = 400
            if pos_y < 0 - 150 * (sin(radians(self.angle)) - 1):
                pos_y = 0 - 150 * (sin(radians(self.angle)) - 1)
            if pos_y > 300 - 150 * (sin(radians(self.angle)) - 1):
                pos_y = 300 - 150 * (sin(radians(self.angle)) - 1)
            self.__pos = (pos_x, pos_y)

    def getPos(self):
        return self.__pos

    def setDir(self, dir):
        self.__direction = dir

    def subHp(self, n=1):
        self.hp -= n

    def is_alive(self):
        return self.hp > 0

    def set_enemy(self, enemy):
        self.enemy = enemy

    def aim(self, another=None):
        if another == None:
            another = self.enemy
        e_pos = another.getPos()
        if self.__pos[0] == e_pos[0]:
            if self.__pos[1] > e_pos[1]:
                ang = 270
            elif self.__pos[1] < e_pos[1]:
                ang = 90
            else:
                ang = 0
        else:
            ang = atan((e_pos[1] - self.__pos[1]) / (e_pos[0] - self.__pos[0]))*180/pi
        return ang

        # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成

    def attack(self):
        if self.power.is_ready:
            # 蓄力技能
            self.power.clear()
            return self.powerAttack()
        else:
            self.power.clear()
            return self.baseAttack()

    def baseAttack(self):
        bullet1 = Bullet(type=self.type, angle=245, pos=self.__pos)
        bullet2 = Bullet(type=self.type, angle=270, pos=self.__pos)
        bullet3 = Bullet(type=self.type, angle=295, pos=self.__pos)
        return bullet1, bullet2, bullet3

    def powerAttack(self):
        bullet1 = Bullet(type=self.type, angle=245, pos=self.__pos, v=3, size=(3, 3))
        bullet2 = Bullet(type=self.type, angle=270, pos=self.__pos, v=3, size=(3, 3))
        bullet3 = Bullet(type=self.type, angle=295, pos=self.__pos, v=3, size=(3, 3))
        return bullet1, bullet2, bullet3

    def superAttack(self):
        # 这里写大招
        self.energy.clear()
        pass


class P_Round(Player):
    def baseAttack(self):
        b_lst = []
        for i in range(5):
            b_lst.append(Bullet(type=bullet_round, pos=self.__pos, angle=self.aim(), v=(i + 1) * 2))
        return b_lst

    def powerAttack(self):
        b_lst = []
        for i in range(8):
            b_lst.append(Bullet(type=bullet_round,
                                pos=(self.__pos[0] + 10 * cos(pi * i / 8), self.__pos[1] + 10 * sin(pi * i / 8)),
                                angle=self.aim() + 5, v=5))
            b_lst.append(Bullet(type=bullet_round,
                                pos=(self.__pos[0] + 10 * cos(pi * i / 8), self.__pos[1] + 10 * sin(pi * i / 8)),
                                angle=self.aim() - 5, v=5))
        return b_lst

    def superAttack(self):
        pass


class P_Delta(Player):
    def baseAttack(self):
        b_lst = []
        for i in range(3):
            b_lst.append(Bullet(type=bullet_round, pos=self.__pos, angle=self.angle + (i - 1) * 5, v=10))
        return b_lst

    def powerAttack(self):
        pass

    def superAttack(self):
        pass


class P_Square(Player):
    def baseAttack(self):
        b_lst=[]
        for i in range(3):
            b_lst.append(
                Bullet(type=bullet_round, pos=(self.__pos[0] + (i - 1) * 5, self.__pos[1]), angle=self.angle, v=10))
        return b_lst

    def powerAttack(self):
        pass

    def superAttack(self):
        pass
