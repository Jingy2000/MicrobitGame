from math import sin, cos, sqrt


class Bullet:
    def __init__(self, type, pos, angle, v, size=(1, 1), rebound=False, damage=10):
        self.type = type
        self.pos = pos
        self.angle = angle
        self.v = v
        self.size = size
        self.rebound = rebound
        self.damage = damage

    def move(self):
        self.pos = (self.pos[0] + self.v * cos(self.angle),
                    self.pos[1] + self.v * sin(self.angle))
        # 判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2)
        if distance < (self.hit_radius + player.hit_radius):
            player.subhp(self.damage)


class Player:
    def __init__(self):
        self.hp = 100
        self.energy = 0
        self.skillReady = False
        self.pos = 0
        self.hit_radius = 3
        self.state = 's'  # 静止
        self.v = 1

    def updatePos(self):
        if self.state == 'l':
            self.pos -= self.v
        elif self.state == 'r':
            self.pos += self.v

    def subhp(self, n=1):
        self.hp -= n

    def is_alive(self):
        return self.hp > 0

    def updateEnergy(self):
        self.energy += 1
        return self.energy

    # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成
    def attack(self, bulletType):
        # waittime = 10  # 前摇，到时候调整,需要时间等待
        bullet1 = Bullet(type=bulletType, angle=-25, pos=self.pos)
        bullet2 = Bullet(type=bulletType, angle=0, pos=self.pos)
        bullet3 = Bullet(type=bulletType, angle=25, pos=self.pos)
        return bullet1, bullet2, bullet3
