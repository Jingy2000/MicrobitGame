from player_and_bullet import *


# ----------------------------MAIN--------------------------------
def main():
    player_red = Player(0)
    player_blue = Player(100)  # 地图高度这个参数
    bullet_list_red = []
    bullet_list_blue = []

    while True:
        # 接受指令
        pass

    # 人物移动和射击
    if red_L:
        player_red.left()
    if red_R:
        player_red.right()
    if red_click:
        player_red.attack()


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
