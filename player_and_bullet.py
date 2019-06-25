from math import sin, cos, sqrt, pi, radians, atan
from main import Smooth_Multi
from image_type import *
import random


class Bullet:
    def __init__(self, type, pos, angle, v=10.0, size=(1, 1), rebound=0, damage=10, life=300):
        self.type = type
        self.pos = pos
        self.angle = angle
        self.v = v / Smooth_Multi
        self.size = size
        self.rebound = rebound
        self.damage = damage
        self.life = life

        self.hit_radius = 5

        self.alive = True
        # self.visible=100 # 透明度，不知道要不要加

    def getPos(self):
        return self.pos

    def move(self):
        self.life -= 1
        if self.life <= 0:
            self.alive = False
        self.pos = (self.pos[0] + self.v * cos(radians(self.angle)),
                    self.pos[1] + self.v * sin(radians(self.angle)))
        if self.rebound > 0:
            x, y = self.pos
            if x > 400:
                x = 800 - x
                self.angle = 180 - self.angle
                self.rebound -= 1
            if x < 0:
                x = -x
                self.angle = 180 - self.angle
                self.rebound -= 1
            if y > 600:
                y = 1200 - y
                self.angle = -self.angle
                self.rebound -= 1
            if y < 0:
                y = -y
                self.angle = -self.angle
                self.rebound -= 1
            self.pos = (x, y)
        # 这里还可以判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.pos[0] - player.getPos()[0]) ** 2 + (self.pos[1] - player.getPos()[1]) ** 2)
        eff_radius = (self.hit_radius * sqrt(self.size[0] ** 2 + self.size[1] ** 2) + player.hit_radius)
        if distance < eff_radius:
            player.subHp(self.damage)
            return True
        if distance < eff_radius * 3:
            player.energy.update(10)  # graze
        return False

    def is_alive(self):
        return self.alive


class B_trap(Bullet):
    def __init__(self, type, pos, angle, v=10.0, size=(1, 1), rebound=False, damage=10, decay=0.97):
        Bullet.__init__(self, type, pos, angle, v, size, rebound, damage)
        self.decay = decay

    def move(self):
        self.v = self.v * self.decay
        self.pos = (self.getPos()[0] + self.v * cos(radians(self.angle)),
                    self.getPos()[1] + self.v * sin(radians(self.angle)))
        if self.v < 0.01:
            self.alive = False
        # 这里还可以判断出屏反弹


class B_curve(Bullet):
    def __init__(self):
        pass


class Gauge:
    def __init__(self, max, init=0, v=1):
        self.init = init
        self.length = init
        self.max = max
        self.v = v  # 自动回复的速度

    def update(self, n=1):
        self.length += self.v * n
        if self.length > self.max:
            self.length = self.max
        if self.length < 0:
            self.length = 0

    def ratio(self) -> float:
        return self.length / self.max

    def clear(self):
        self.length = self.init

    def is_ready(self):
        return self.length == self.max

    def is_empty(self):
        return self.length == 0


class Player:
    def __init__(self, y, angle):
        self.hp = Gauge(100, v=-1, init=100)
        self.energy = Gauge(1000)
        self.power = Gauge(30)
        self.vmax = 5
        self.__direction = (0, 0)  # 方向是手柄给出的方向，上-，左-
        self.pos = (200, y)
        self.angle = angle  # 0-360,90是向上
        self.hit_radius = 1
        self.type = 'bullet_round_blue'
        self.enemy = None
        self.cd = 0
        self.card_on = 0
        self.cards = []

    def move(self):
        if self.cd > 0:
            self.cd -= 1

        self.energy.update()

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
        for i in range(n):
            self.hp.update()

    def power_up(self):
        if self.cd > 0:
            return

        if self.power.is_ready():
            # 蓄力技能
            self.power.clear()
            return self.powerAttack()
        else:
            self.power.update()

    def is_alive(self):
        return not self.hp.is_empty()

    def set_enemy(self, enemy):
        self.enemy = enemy

    def aim(self, another=None):
        if another == None:
            another = self.enemy.getPos()
        e_pos = another
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

        if self.power.is_ready():
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
        if (self.energy.length >= self.cards[i].cost) and (self.cards[i].ready()):
            self.energy.update(-self.cards[i].cost)
        else:
            return
        if (self.cd == 0) and self.cards[i].ready():
            self.cards[i].run()
            self.cd = self.cards[i].silent

    def run_card(self):
        b_lst = []
        for card in self.cards:
            if card.on:
                b_lst += card.run()
        return b_lst


class P_Round(Player):
    def __init__(self, y, angle):
        self.base_cd = 15
        self.power_cd = 15
        Player.__init__(self, y, angle)

    def baseAttack(self):
        b_lst = []
        self.cd = self.base_cd * Smooth_Multi
        for i in range(2, 5):
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim(), v=(i + 1) * 2))
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim() + 45, v=(i + 1) * 2))
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim() - 45
                                , v=(i + 1) * 2))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = self.power_cd * Smooth_Multi
        for i in range(8):
            b_lst.append(Bullet(type=bullet_round_blue,
                                pos=(self.getPos()),
                                angle=self.aim() + 20, v=5 + i))
            b_lst.append(Bullet(type=bullet_round_blue,
                                pos=(self.getPos()[0] + 20 * cos(2 * pi * i / 8),
                                     self.getPos()[1] + 20 * sin(2 * pi * i / 8)),
                                angle=self.aim(), v=5))
            b_lst.append(Bullet(type=bullet_round_blue,
                                pos=(self.getPos()),
                                angle=self.aim() - 20, v=5 + i))
        return b_lst

    def superAttack(self):
        pass


class P_Delta(Player):
    def __init__(self, y, angle):
        self.base_cd = 10
        self.power_cd = 15
        Player.__init__(self, y, angle)

    def baseAttack(self):
        b_lst = []
        self.cd = self.base_cd * Smooth_Multi
        for i in range(7):
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.angle + (i - 3) * 12, v=10))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = self.power_cd * Smooth_Multi
        for i in range(30):
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.angle + random.uniform(-60, 60),
                                v=random.uniform(5, 15)))
        return b_lst

    def superAttack(self):
        pass


class P_Square(Player):
    def __init__(self, y, angle):
        self.base_cd = 5
        self.power_cd = 15
        Player.__init__(self, y, angle)

    def baseAttack(self):
        b_lst = []
        self.cd = self.base_cd * Smooth_Multi
        for i in range(3):
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] + (i - 1) * 10, self.getPos()[1]),
                       angle=self.angle,
                       v=20))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = self.power_cd * Smooth_Multi
        for i in range(10):
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] + i * 10, self.getPos()[1]), angle=self.angle,
                       v=(16 - i) * 1))
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] - i * 10, self.getPos()[1]), angle=self.angle,
                       v=(16 - i) * 1))
        return b_lst

    def superAttack(self):
        pass


class P_Re(Player):
    def __init__(self, y, angle):
        self.base_cd = 5
        self.power_cd = 15
        Player.__init__(self, y, angle)

    def move(self):
        self.energy.update(20)
        Player.move(self)

    def baseAttack(self):
        b_lst = []
        self.cd = self.base_cd * Smooth_Multi
        for i in range(3):
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] + (i - 1) * 10, self.getPos()[1]),
                       angle=self.angle,
                       v=20))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = self.power_cd * Smooth_Multi
        for i in range(10):
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] + i * 10, self.getPos()[1]), angle=self.angle,
                       v=(16 - i) * 1))
            b_lst.append(
                Bullet(type=bullet_round_blue, pos=(self.getPos()[0] - i * 10, self.getPos()[1]), angle=self.angle,
                       v=(16 - i) * 1))
        return b_lst

    def superAttack(self):
        pass


class P_Shield(Player):
    def __init__(self, y, angle):
        self.base_cd = 0
        self.power_cd = 75
        Player.__init__(self, y, angle)

    def baseAttack(self):
        b_lst = []
        self.cd = self.base_cd * Smooth_Multi
        th0 = random.random() * 360
        for i in range(60):
            b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.angle + i * 6 + th0, v=5))
        return b_lst

    def powerAttack(self):
        b_lst = []
        self.cd = self.power_cd * Smooth_Multi
        b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim(), v=10, rebound=100, life=10000))
        b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim() + 15, rebound=100, life=10000))
        b_lst.append(Bullet(type=bullet_round_blue, pos=self.getPos(), angle=self.aim() - 15, rebound=100, life=10000))
        return b_lst


class Card:
    def __init__(self, master):
        self.time = 0
        self.max_cd = 0
        self.duration = 0
        self.cd = 0
        self.cost = 500
        self.on = False
        self.master = master

    def ready(self):
        return self.cd == 0

    def cold_down(self):
        self.cd -= 1

    def run(self):
        if self.cd == 0:
            self.cd = self.max_cd
            self.on = True
            self.time = 1
            return []

        if self.time == self.duration + 1:
            self.on = False
            return []

        self.time += 1
        return self.shoot()

    def shoot(self):
        pass


class C_flower(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 30 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if self.time % (15 * Smooth_Multi) == 0:
            for i in range(6):
                for j in range(8):
                    b_lst.append(
                        Bullet(type=bullet_round_blue, pos=self.master.getPos(),
                               angle=self.master.angle + i * 9 + j * 45,
                               v=5 + i * 3))
                    b_lst.append(
                        Bullet(type=bullet_round_blue, pos=self.master.getPos(),
                               angle=self.master.angle - i * 9 + j * 45,
                               v=5 + i * 3))
        return b_lst


class C_trap(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 0 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 30 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if self.time % (10 * Smooth_Multi) == 0:
            for i in range(12):
                b_lst.append(
                    B_trap(type=bullet_round_blue, pos=self.master.getPos(),
                           angle=self.master.angle + random.uniform(-60, 60),
                           v=random.uniform(5, 15)))
        return b_lst


class C_spark(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 30 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if (self.time < 10 * Smooth_Multi) and (self.time % (2 * Smooth_Multi) == 0):
            for i in range(8):
                b_lst.append(B_trap(type=bullet_round_blue, pos=self.master.getPos(),
                                    angle=self.master.angle + i * 45 + self.time * 10,
                                    v=15, decay=0.8))
        if self.time == 20 * Smooth_Multi:
            for i in range(5):
                for j in range(15):
                    b_lst.append(
                        Bullet(type=bullet_round_blue,
                               pos=(self.master.getPos()[0] + (i - 2) * 5, self.master.getPos()[1]),
                               angle=self.master.angle,
                               v=j * 3 + 10))
        return b_lst


class C_spark_aim(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 40 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if (self.time < 10 * Smooth_Multi) and (self.time % (2 * Smooth_Multi) == 0):
            for i in range(8):
                b_lst.append(B_trap(type=bullet_round_blue, pos=self.master.getPos(),
                                    angle=self.master.angle + i * 45 + self.time * 10,
                                    v=15, decay=0.8))
        if (self.time > 19 * Smooth_Multi) and (self.time % (10 * Smooth_Multi) == 0):
            for j in range(15):
                b_lst.append(
                    Bullet(type=bullet_round_blue, pos=self.master.getPos(),
                           angle=self.master.aim(),
                           v=j * 3 + 5))
        return b_lst


class C_spark_focus(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 50 * Smooth_Multi
        self.f_point = (0, 0)

    def shoot(self):
        b_lst = []
        if self.time == 2:
            self.f_point = self.master.getPos()
        if self.time < 5:
            for i in range(4):
                b_lst.append(
                    Bullet(type=bullet_round_blue, pos=(self.f_point[0] + 10 * (self.time - 2) * cos(i * pi / 2),
                                                        self.f_point[1] + 10 * (self.time - 2) * sin(i * pi / 2)),
                           angle=0,
                           v=0, life=60))
        if self.time == 5:
            for i in range(16):
                b_lst.append(
                    Bullet(type=bullet_round_blue, pos=(self.f_point[0] + 10 * (self.time - 2) * cos(i * pi / 8),
                                                        self.f_point[1] + 10 * (self.time - 2) * sin(i * pi / 8)),
                           angle=0,
                           v=0, life=60))
        if (self.time < 30 * Smooth_Multi) and (self.time > 19 * Smooth_Multi) and (
                self.time % (2 * Smooth_Multi) == 0):
            for i in range(8):
                b_lst.append(B_trap(type=bullet_round_blue, pos=self.master.getPos(),
                                    angle=self.master.angle + i * 45 + self.time * 10,
                                    v=15, decay=0.8))
        if (self.time > 39 * Smooth_Multi) and (self.time % (2 * Smooth_Multi) == 0):
            for j in range(8):
                b_lst.append(
                    Bullet(type=bullet_round_blue, pos=self.master.getPos(),
                           angle=self.master.aim(self.f_point),
                           v=j * 5 + 10))
        return b_lst


class C_chain(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 30 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if self.time % (10 * Smooth_Multi) == 0:
            for i in range(10):
                b_lst.append(
                    Bullet(type=bullet_round_blue,
                           pos=(self.master.getPos()[0] + ((self.time // 10) - 1) * 60, self.master.getPos()[1]),
                           angle=self.master.angle,
                           v=(i + 3) * 1.5))
                b_lst.append(
                    Bullet(type=bullet_round_blue,
                           pos=(self.master.getPos()[0] - ((self.time // 10) - 1) * 60, self.master.getPos()[1]),
                           angle=self.master.angle,
                           v=(i + 3) * 1.5))
        return b_lst


class C_lock(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 10 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if self.time % (10 * Smooth_Multi) == 0:
            for i in range(20):
                b_lst.append(
                    Bullet(type=bullet_round_blue,
                           pos=(self.master.getPos()[0], self.master.getPos()[1]),
                           angle=self.master.angle,
                           v=(i + 5) * 0.75, rebound=5, life=1000))
        return b_lst


class C_reflect(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 60 * Smooth_Multi
        self.max_cd = 180 * Smooth_Multi
        self.duration = 30 * Smooth_Multi

    def shoot(self):
        b_lst = []
        if self.time % (10 * Smooth_Multi) == 0:
            th0 = random.random() * 360
            for i in range(20):
                b_lst.append(
                    Bullet(type=bullet_round_blue, pos=self.master.getPos(), angle=self.master.angle + i * 18 + th0,
                           v=8, rebound=1))
        return b_lst


class C_heal(Card):
    def __init__(self, master):
        Card.__init__(self, master)
        self.silent = 0 * Smooth_Multi
        self.max_cd = 300 * Smooth_Multi
        self.duration = 20 * Smooth_Multi
        self.cost = 200

    def shoot(self):
        if (self.time % 2 == 0) and (self.time > 10):
            self.master.hp.update(-1)
        return []
