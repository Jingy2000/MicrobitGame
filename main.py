class bullet():
    pass

class player():
    def __init__(self):
        self.hp = 100
        self.energy = 0
        self.skillReady = False
        self.pos = 0

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
        bullet1 = bullet(type=bulletType, angle=-25, pos=self.pos)
        bullet2 = bullet(type=bulletType, angle=0, pos=self.pos)
        bullet3 = bullet(type=bulletType, angle=25, pos=self.pos)
        return bullet1, bullet2, bullet3

