import pygame
from game_sprites import *

class GameMain:
    """ main class"""
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        self.enemies_group = pygame.sprite.Group()
        # 设置定时器-创建敌机
        pygame.time.set_timer(CREATE_ENEMIES_EVENT, 1000)
        # 设置定时器-发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):

        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)  # 滚动背景精灵组

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemies_group.update()
        self.enemies_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == CREATE_ENEMIES_EVENT:
                self.enemies_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = HERO_CONSTANT_SPEED
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -HERO_CONSTANT_SPEED
        else:
            self.hero.speed = 0

    def __check_collide(self):
        """ 碰撞检测 """
        pygame.sprite.groupcollide(self.hero.bullets, self.enemies_group, True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemies_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            GameMain.__game_over()

    def start_game(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)

            self.__update_sprites()
            self.__event_handler()
            self.__check_collide()
            pygame.display.update()

    def __game_over(self):
        pygame.quit()  # uninstall pygame modules
        exit()  # exit python


if __name__ == '__main__':
    game_obj = GameMain()
    game_obj.start_game()
