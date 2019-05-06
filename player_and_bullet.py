from math import sin, cos, sqrt, pi, radians, atan
from image_type import *
import random


class Bullet:
    def __init__(self, type, pos, angle, v=10.0, size=(1, 1), rebound=False, damage=10):
        self.type = type
        self.pos = pos
        self.angle = angle
        self.v = v
        self.size = size
        self.rebound = rebound
        self.damage = damage

        self.hit_radius = 5

        self.alive = True
        # self.visible=100 # 透明度，不知道要不要加

    def getPos(self):
        return self.pos

    def move(self):
        self.pos = (self.pos[0] + self.v * cos(radians(self.angle)),
                    self.pos[1] + self.v * sin(radians(self.angle)))
        # 这里还可以判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.pos[0] - player.getPos()[0]) ** 2 + (self.pos[1] - player.getPos()[1]) ** 2)
        eff_radius = (self.hit_radius * sqrt(self.size[0] ** 2 + self.size[1] ** 2) + player.hit_radius)
        if distance < eff_radius:
            player.subHp(self.damage)
            return True
        return False

    def is_alive(self):
        return self.alive


class B_trap(Bullet):
    def move(self):
        self.v = self.v * 0.97
        self.pos = (self.getPos()[0] + self.v * cos(radians(self.angle)),
                      self.getPos()[1] + self.v * sin(radians(self.angle)))
        if self.v < 0.1:
            self.alive = False
        # 这里还可以判断出屏反弹


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
        self.power = Power(30)
        self.vmax = 5
        self.__direction = (0, 0)  # 方向是手柄给出的方向，上-，左-
        self.pos = (200, y)
        self.angle = angle  # 0-360,90是向上
        self.hit_radius = 3
        self.type = 'bullet_round'
        self.enemy = None
        self.cd = 0
        self.card_on = 0
        self.cards = []

    def move(self):
        if self.cd > 0:
            self.cd -= 1

        for card in self.cards:
            if not card.ready():
                card.cold_down()

        if self.__direction == (0, 0):
            pass
        else:
            current = self.pos
            direction = self.__direction
            x, y = direction[0], direction[1]
            rmax = 8
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
            self.pos = (pos_x, pos_y)

    def getPos(self):
        return self.pos

    def setDir(self, dir):
        self.__direction = tuple(dir)

    def subHp(self, n=1):
        self.hp -= n

    def power_up(self):
        if self.cd > 0:
            return

        if self.power.is_ready:
            # 蓄力技能
            self.power.clear()
            return self.powerAttack()
        else:
            self.power.update()

    def is_alive(self):
        return self.hp > 0

    def set_enemy(self, enemy):
        self.enemy = enemy

    def aim(self, another=None):
        if another == None:
            another = self.enemy
        e_pos = another.getPos()
        if self.pos[0] == e_pos[0]:
            if self.pos[1] > e_pos[1]:
                ang = 270
            elif self.pos[1] < e_pos[1]:
                ang = 90
            else:
                ang = 0
        else:
            ang = atan((e_pos[1] - self.pos[1]) / (e_pos[0] - self.pos[0])) * 180 / pi
            if e_pos[0] - self.pos[0] < 0:
                ang += 180
        return ang

        # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成

    def attack(self):
        if self.cd > 0:
            return

        if self.power.is_ready:
            # 蓄力技能
            self.power.clear()
            return self.powerAttack()
        else:
            self.power.clear()
            return self.baseAttack()

    def baseAttack(self):
        bullet1 = Bullet(type=self.type, angle=245, pos=self.pos)
        bullet2 = Bullet(type=self.type, angle=270, pos=self.pos)
        bullet3 = Bullet(type=self.type, angle=295, pos=self.pos)
        return bullet1, bullet2, bullet3

    def powerAttack(self):
        bullet1 = Bullet(type=self.type, angle=245, pos=self.pos, v=3, size=(3, 3))
        bullet2 = Bullet(type=self.type, angle=270, pos=self.pos, v=3, size=(3, 3))
        bullet3 = Bullet(type=self.type, angle=295, pos=self.pos, v=3, size=(3, 3))
        return bullet1, bullet2, bullet3

    def superAttack(self):
        # 这里写大招
        self.energy.clear()
        pass

    def use_card(self, i):
        if (self.cd == 0) and self.cards[i].ready():
            self.cards[self.card_on].run()
            self.cd = self.cards[i].silent

    def run_card(self):
        b_lst = []
        for card in self.cards:
            if card.on:
                b_lst += card.run()
        return b_lst


class P_Round(Player):
    def baseAttack(self):
        b_lst = []
        self.cd = 10
        for i in range(2, 5):
            b_lst.append(Bullet(type=bullet_round, pos=self.getPos(), angle=self.aim(), v=(i + 1) * 2))
            b_lst.append(Bullet(type=bullet_round, pos=self.getPos(), angle=self.aim() + 15, v=(i + 1) * 2))
            b_lst.append(Bullet(type=bullet_round, pos=self.getPos(), angle=self.aim() - 15, v=(i + 1) * 2))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = 5
        for i in range(8):
            b_lst.append(Bullet(type=bullet_round,
                                pos=(self.getPos()[0] + 20 * cos(2 * pi * i / 8),
                                     self.getPos()[1] + 20 * sin(2 * pi * i / 8)),
                                angle=self.aim() + 20, v=10))
            b_lst.append(Bullet(type=bullet_round,
                                pos=(self.getPos()[0] + 20 * cos(2 * pi * i / 8),
                                     self.getPos()[1] + 20 * sin(2 * pi * i / 8)),
                                angle=self.aim(), v=5))
            b_lst.append(Bullet(type=bullet_round,
                                pos=(self.getPos()[0] + 20 * cos(2 * pi * i / 8),
                                     self.getPos()[1] + 20 * sin(2 * pi * i / 8)),
                                angle=self.aim() - 20, v=10))
        return b_lst

    def superAttack(self):
        pass


class P_Delta(Player):
    def baseAttack(self):
        b_lst = []
        self.cd = 7
        for i in range(7):
            b_lst.append(Bullet(type=bullet_round, pos=self.getPos(), angle=self.angle + (i - 3) * 10, v=10))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = 15
        for i in range(15):
            b_lst.append(Bullet(type=bullet_round, pos=self.getPos(), angle=self.angle + random.uniform(-60, 60),
                                v=random.uniform(5, 15)))
        return b_lst

    def superAttack(self):
        pass


class P_Square(Player):
    def baseAttack(self):
        b_lst = []
        self.cd = 5
        for i in range(5):
            b_lst.append(
                Bullet(type=bullet_round, pos=(self.getPos()[0] + (i - 1) * 10, self.getPos()[1]), angle=self.angle,
                       v=20))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = 15
        for i in range(10):
            b_lst.append(Bullet(type=bullet_round, pos=(self.getPos()[0] + i * 10, self.getPos()[1]), angle=self.angle,
                                v=(16 - i) * 1))
            b_lst.append(Bullet(type=bullet_round, pos=(self.getPos()[0] - i * 10, self.getPos()[1]), angle=self.angle,
                                v=(16 - i) * 1))
        return b_lst

    def superAttack(self):
        pass


class Card:
    def __init__(self, master):
        self.time = 0
        self.cd = 0
        self.on = False
        self.master = master

    def ready(self):
        return self.cd == 0

    def cold_down(self):
        self.cd -= 1

    def run(self):
        pass


class C_flower(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60

    def run(self):
        if self.cd == 0:
            self.cd = 225
            self.on = True
            self.time = 1
            return

        if self.time == 16:
            self.on = False

        self.time += 1
        b_lst = []
        if (self.time % 15 == 0):
            for i in range(6):
                for j in range(8):
                    b_lst.append(
                        Bullet(type=bullet_round, pos=self.master.getPos(), angle=self.master.angle + i * 9 + j * 45,
                               v=5 + i * 3))
                    b_lst.append(
                        Bullet(type=bullet_round, pos=self.master.getPos(), angle=self.master.angle - i * 9 + j * 45,
                               v=5 + i * 3))
        return b_lst


class C_trap(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 10

    def run(self):
        if self.cd == 0:
            self.cd = 150
            self.on = True
            return

        if self.time == 11:
            self.on = False

        self.time += 1
        b_lst = []
        if self.time % 5 == 0:
            for i in range(10):
                b_lst.append(
                    B_trap(type=bullet_round, pos=self.master.getPos(),
                           angle=self.master.angle + random.uniform(-60, 60),
                           v=random.uniform(8, 15)))
        return b_lst


class C_spark(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 10

    def run(self):
        if self.cd == 0:
            self.cd = 150
            self.on = True
            return

        if self.time == 11:
            self.on = False

        self.time += 1
        b_lst = []
        if (self.time % 5 == 0):
            for i in range(10):
                b_lst.append(
                    B_trap(type=bullet_round, pos=self.master.getPos(),
                           angle=self.master.angle + random.uniform(-60, 60),
                           v=random.uniform(3, 5)))
        return b_lst


class C_chain(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60

    def run(self):
        if self.cd == 0:
            self.cd = 200
            self.on = True
            return

        if self.time == 46:
            self.on = False

        self.time += 1
        b_lst = []
        if (self.time % 10 == 0):
            for i in range(10):
                b_lst.append(
                    Bullet(type=bullet_round,
                           pos=(self.master.getPos()[0] + ((self.time // 10) - 1) * 10, self.master.getPos()[1]),
                           angle=self.master.angle,
                           v=20))
        return b_lst
