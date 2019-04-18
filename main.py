from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d

r_A = K_w
r_B = K_s
r_L = K_a
r_R = K_d


# ----------------------------MAIN--------------------------------
def main():
    player_red = Player(0)
    player_blue = Player(100)  # 地图高度这个参数
    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    while True:
        # 接受指令
        key_pressed = pygame.key.get_pressed()
        if key_pressed[r_A]:
            r_A_down=True
            player_red.power_up()
        else:
            if r_A_down:
                player_red.attack()
            r_A_down=False

        # 人物移动和射击


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


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
