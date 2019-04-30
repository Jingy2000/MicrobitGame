from math import sin, cos, sqrt, pi


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

    def move(self):
        self.__pos = (self.__pos[0] + self.v * cos(self.angle * pi / 180),
                      self.__pos[1] + self.v * sin(self.angle * pi / 180))
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
        self.angle = angle
        self.hit_radius = 3
        self.type = 'bullet_round'

    def move(self):
        if self.__direction == (0, 0):
            pass
        else:
            current = self.__pos
            direction = self.__direction
            x, y = direction[0], direction[1]
            rmax = 2048
            pos_x, pos_y = current[0] - self.vmax * x / rmax, current[1] - self.vmax * y / rmax
            # 人物出屏幕
            if pos_x < 0:
                pos_x = 0
            if pos_x > 400:
                pos_x = 400
            if pos_y < 0:
                pos_y = 0
            if pos_y > 300:
                pos_y = 300
            self.__pos = (pos_x, pos_y)

    def getPos(self):
        return self.__pos

    def setDir(self, dir):
        self.__direction = dir

    def subHp(self, n=1):
        self.hp -= n

    def is_alive(self):
        return self.hp > 0

    # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成
    def attack(self):
        if self.power.is_ready:
            # 蓄力技能
            bullet1 = Bullet(type=self.type, angle=self.angle - 25, pos=self.__pos, v=3, size=(3, 3))
            bullet2 = Bullet(type=self.type, angle=self.angle, pos=self.__pos, v=3, size=(3, 3))
            bullet3 = Bullet(type=self.type, angle=self.angle + 25, pos=self.__pos, v=3, size=(3, 3))
            self.power.clear()
            return bullet1, bullet2, bullet3
        else:
            bullet1 = Bullet(type=self.type, angle=self.angle - 25, pos=self.__pos)
            bullet2 = Bullet(type=self.type, angle=self.angle, pos=self.__pos)
            bullet3 = Bullet(type=self.type, angle=self.angle + 25, pos=self.__pos)
            self.power.clear()
            return bullet1, bullet2, bullet3

    def superAttack(self):
        # 这里写大招
        self.energy.clear()
        pass
