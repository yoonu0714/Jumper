import arcade
import json
from functools import singledispatchmethod as mdp
from types import *

import Menu
from GlobalConsts import *

class GameView(arcade.View):
    # Main application class.
    def __init__(self):
        # call the parent class and set up the window
        super().__init__()

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.coin_list = None
        self.restart_coin_list = None
        self.wall_list = None
        self.player_list = None
        self.object_list = None
        self.spring_list = None
        self.flag_list = None
        self.portal_list = None
        self.player_sprite = arcade.Sprite("pic/default/char.png", char_scaling)

        # Our physics engine
        self.physics_engine = None
        self.spring_engine = None

        # physics engine
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # variables for map reading
        self.map_title = None
        self.map_author = None
        self.char_x = None
        self.char_y = None
        self.save_char_x = None  # 플레이어 위치저장 변수
        self.save_char_y = None  # 플레이어 위치저장 변수
        self.map_string_list = {"walls", "thorns", "coins", "flags", "spring", "portal"}

        self.cur_m = 0
        self.window.set_mouse_visible(True)

    @mdp
    def map_read(self, map_file):
        with open(map_file, encoding='utf-8') as f_r:
            # load file
            data = json.load(f_r)
            print(data)

            # load variables
            # location
            location_x = data["char"][0]
            location_y = data["char"][1]

            # setting user position
            self.user_pos(location_x, location_y)

            # draw
            for i in self.map_string_list:
                print(i)
                #for a in range(len(data[i])):
                for k in data[i]:
                    if i == "walls": self.wall_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "thorns": self.object_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "coins": self.coin_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "flags": self.flag_line(k["pos"][0], k["pos"][1], k["tex"])
                    elif i == "spring": self.spring_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "portal": self.portal_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])

    @map_read.register(dict)
    def _(self, map_file):
        data = map_file

        # load variables
        # location
        location_x = data["char"][0]
        location_y = data["char"][1]

        self.user_pos(location_x, location_y)

        # draw
        for i in self.map_string_list:
            print(i)
            # for a in range(len(data[i])):
            for k in data[i]:
                if i == "walls":
                    self.wall_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                elif i == "thorns":
                    self.object_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                elif i == "coins":
                    self.coin_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                elif i == "flags":
                    self.flag_line(k["pos"][0], k["pos"][1], k["tex"])
                elif i == "spring":
                    self.spring_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                elif i == "portal":
                    self.portal_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])

    @map_read.register(str)
    def _(self, map_file):
        with open(map_file, encoding='utf-8') as f_r:
            # load file
            data = json.load(f_r)
            print(data)

            # load variables
            # location
            location_x = data["char"][0]
            location_y = data["char"][1]

            # setting user position
            self.user_pos(location_x, location_y)

            # draw
            for i in self.map_string_list:
                print(i)
                #for a in range(len(data[i])):
                for k in data[i]:
                    if i == "walls": self.wall_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "thorns": self.object_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "coins": self.coin_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "flags": self.flag_line(k["pos"][0], k["pos"][1], k["tex"])
                    elif i == "spring": self.spring_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])
                    elif i == "portal": self.portal_line(k["pos"][0], k["pos"][1], k["pos"][2], k["tex"])


    def user_pos(self, u_x, u_y):
        self.char_x = u_x
        self.char_y = u_y
        print("user_pos runs")

    def head_map(self, cur_m, connector, p_m):
        if cur_m == 0:
            self.initialize(1)
        elif cur_m > 0:
            self.initialize(0)
            self.player_restart()
        with open(connector, encoding='utf-8') as c_r:
            j_con = json.load(c_r)
        if p_m == -1:
            self.map_read(j_con["cur_dir"][0] + j_con["map_con"][cur_m]) #j_con["cur_dir"][0] +
        self.cur_m = cur_m

    def flag_save(self, flag, num):
        if num == 1:
            self.save_char_x = flag.center_x
            self.save_char_y = flag.center_y
        else:
            self.save_char_x = self.char_x
            self.save_char_y = self.char_y

    def portal_line(self, start, end, height, img):
        for x in range(start, end, 32):
            portal = arcade.Sprite(img, char_scaling)
            portal.center_x = x
            portal.center_y = height
            self.portal_list.append(portal)

    def wall_line(self, start, end, height, img):
        for u in range(start, end, 32):
            wall = arcade.Sprite(img, char_scaling)
            wall.center_x = u
            wall.center_y = height
            self.wall_list.append(wall)

    def spring_line(self, start, end, height, img):
        for x in range(start, end, 32):
            spring = arcade.Sprite(img, char_scaling)
            spring.center_x = x
            spring.center_y = height
            self.spring_list.append(spring)

    # 스프링에 닿았을 경우 캐릭터가 점프를 2배높이
    def spring_act(self):
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = player_jump_speed * 2
            self.physics_engine.increment_jump_counter()

    def flag_line(self, x, y, img):
        flag = arcade.Sprite(img, char_scaling)
        flag.center_x = x
        flag.center_y = y
        self.flag_save(flag, 0)  # flag가 생성될때 마다, save
        self.flag_list.append(flag)

    # 임시 장애물 나타내기 - 가시, 레이저, 레이저 박스
    def object_line(self, start, end, height, img):
        for x in range(start, end, 32):
            object_f = arcade.Sprite(img, char_scaling)
            object_f.center_x = x
            object_f.center_y = height
            self.object_list.append(object_f)

    # 임시 코인 나타내기
    def coin_line(self, start, end, height, img):
        for u in range(start, end, 32):
            coin = arcade.Sprite(img, char_scaling)
            coin.center_x = u
            coin.center_y = height
            self.coin_list.append(coin)

    # player 스프라이트 처음위치에서 재시작, 코인도 재생성 - 현재 코인 재생성 안됨.
    def player_restart(self):
        # 전체 스프라이트 제거 후 map read 필요.
        self.player_list = arcade.SpriteList()
        self.player_sprite.center_x = self.save_char_x
        self.player_sprite.center_y = self.save_char_y
        self.player_list.append(self.player_sprite)

    def initialize(self, case_c):
        if case_c == 0:
            self.coin_list = None
            self.restart_coin_list = None
            self.wall_list = None
            self.player_list = None
            self.object_list = None
            self.spring_list = None
            self.flag_list = None
            self.portal_list = None
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        self.flag_list = arcade.SpriteList(use_spatial_hash=True)
        self.spring_list = arcade.SpriteList(use_spatial_hash=True)
        self.portal_list = arcade.SpriteList(use_spatial_hash=True)

    def setup(self):
        # sprite lists
        self.initialize(1)
        self.head_map(0, "map/test/maincon.json", -1)

        # player_sprite attributes
        self.player_sprite.center_x = self.char_x  # 플레이어 시작 위치인 char_x 를 넣어줌
        self.player_sprite.center_y = self.char_y
        self.player_list.append(self.player_sprite)
        print("this code works")
        print(self.char_x)
        print()
        print(self.player_list)

        # call this function to restart the game.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        self.spring_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.spring_list, GRAVITY)
        self.physics_engine.enable_multi_jump(2)

    def on_key_press(self, key, modifiers):
        # called whenever a key is pressed
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = player_jump_speed
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        # called when the user releases a key
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        # movement & game logic

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + screen_w - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + screen_h - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                screen_w + self.view_left,
                                self.view_bottom,
                                screen_h + self.view_bottom)

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # object랑 player랑 충돌 시
        object_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.object_list)

        # spring 과 player가 충돌시.
        spring_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.spring_list)

        # flag 과 player가 충돌시.
        flag_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.flag_list)

        # portal 과 player가 충돌시.
        portal_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.portal_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()

        # player스프라이트 삭제후 재생성
        for object_f in object_hit_list:
            self.player_sprite.remove_from_sprite_lists()
            self.player_restart()

        for portal in portal_hit_list:
            self.player_sprite.remove_from_sprite_lists()
            self.cur_m = self.cur_m + 1
            self.head_map(self.cur_m, "map/test/maincon.json", -1)

        # flag 에 닿았을 경우 조건
        for flag in flag_hit_list:
            self.flag_save(flag, 1)  # 1은 깃발에 닿았을때 실행하는 if문을 위한 값

        # 스프링에 닿았을 경우
        for spring in spring_hit_list:
            self.spring_act()

        if self.player_sprite.center_y <= -128:
            self.player_sprite.remove_from_sprite_lists()
            self.player_restart()

    def on_draw(self):
        # render the screen.
        arcade.start_render()
        # code to draw the screen goes here
        self.wall_list.draw()
        self.coin_list.draw()
        self.object_list.draw()
        self.player_list.draw()
        self.spring_list.draw()
        self.flag_list.draw()
        self.portal_list.draw()

class PauseView(arcade.View):       #pause
    def __init__(self, game_veiw):
        super().__init__()
        self.gameveiw = game_veiw

    def on_draw(self):
        arcade.start_render()

        player_sprite = self.gameveiw.player_sprite
        player_sprite.draw()

        arcade.draw_lrtb_rectangle_filled(left= player_sprite.left, right= player_sprite.right, top= player_sprite.top,
                                          bottom= player_sprite.bottom, color=arcade.color.WHITE)

        arcade.draw_text("PAUSED",screen_w / 2, screen_h / 2 + 50, arcade.color.WHITE, font_size= 50, anchor_x="center")
        arcade.draw_text("Press Esc to return",screen_w / 2, screen_h / 2 - 30, arcade.color.WHITE, font_size= 20, anchor_x="center")
        arcade.draw_text("Press M to Menu",screen_w / 2, screen_h / 2 - 50, arcade.color.WHITE, font_size= 20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.gameveiw)
        elif key == arcade.key.M:
            menu_view = Menu.MainView()
            menu_view.setup()
            self.window.show_view(menu_view)
