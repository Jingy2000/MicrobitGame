from math import sin, cos, sqrt


class Bullet():
    def __init__(self, type, pos, angle, v, size=(1, 1), rebound=False, damage=10):
        self.type = type
        self.pos = pos
        self.angle = angle
        self.v = v
        self.size = size
        self.rebound = rebound
        self.damage = damage

        self.alive = True
        # self.visible=100 # 透明度，不知道要不要加

    def move(self):
        self.pos = (self.pos[0] + self.v * cos(self.angle),
                    self.pos[1] + self.v * sin(self.angle))
        # 这里还可以判断出屏反弹

    def hit(self, player):
        distance = sqrt((self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2)
        if distance < (self.hit_radius + player.hit_radius):
            player.subhp(self.damage)
            return True
        else:
            return False

    def is_alive(self):
        return self.alive


class Player():
    def __init__(self):
        self.hp = 100
        self.energy = 0
        self.skillReady = False
        self.pos = 0
        self.hit_radius = 3

    def left(self):
        self.pos -= 1

    def right(self):
        self.pos += 1

    def subhp(self, n=1):
        self.hp -= n

    def is_alive(self):
        return self.hp > 0

    def increaseEnergy(self):
        self.energy += 1

    # 返回三个子弹，分别朝三个方向发射/跟多攻击模式等着子弹来完成
    def attack(self, bulletType):
        # waittime = 10  # 前摇，到时候调整,需要时间等待
        bullet1 = Bullet(type=bulletType, angle=-25, pos=self.pos)
        bullet2 = Bullet(type=bulletType, angle=0, pos=self.pos)
        bullet3 = Bullet(type=bulletType, angle=25, pos=self.pos)
        return bullet1, bullet2, bullet3


# ----------------------------MAIN--------------------------------

player_red = Player()
player_blue = Player()
bullet_list_red = []
bullet_list_blue = []

while True:
    # 接受指令
    pass

    # 人物移动和射击
    pass

    # 子弹的运动
    for bullet in bullet_list_red:
        bullet.move()
    for bullet in bullet_list_blue:
        bullet.move()

    # 子弹出屏判定
    pass

    # *子弹之间的碰撞判定
    pass

    # *子弹存活判定(?)
    pass

    # 子弹与人物的碰撞判定
    for bullet in bullet_list_red:
        if bullet.hit(player_blue):
            bullet_list_red.remove(bullet)
    for bullet in bullet_list_blue:
        if bullet.hit(player_red):
            bullet_list_blue.remove(bullet)

    # 调用绘图
    pass
