import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)  # 屏幕Rect对象
FRAME_PER_SEC = 60  # FPS屏幕刷新率
CREATE_ENEMIES_EVENT = pygame.USEREVENT  # 创建敌机定时器对象
HERO_FIRE_EVENT = pygame.USEREVENT + 1  # 英雄发射子弹的定时器对象
HERO_CONSTANT_SPEED = 3  # 英雄移动速度
BULLET_SPEED = -2  # 子弹速度

class GameBasic(pygame.sprite.Sprite):
    """ common sprite"""
    def __init__(self, image_url, speed = 1):
        super().__init__()
        self.image = pygame.image.load(image_url)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameBasic):
    """ moving background """
    def __init__(self, is_alt = False):
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.bottom = 0

    def update(self):
        super().update()
        if self.rect.y > self.rect.height:
            self.rect.bottom = 0


class Enemy(GameBasic):
    """ enery planes"""
    def __init__(self):
        super().__init__('./images/enemy1.png')
        self.rect.bottom = 0
        self.rect.x = random.randint(1, SCREEN_RECT.width - self.rect.width)
        self.speed = random.randint(1, 3)


    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()


class Bullet(GameBasic):
    """ 子弹精灵 """
    def __init__(self):
        super().__init__('./images/bullet1.png', BULLET_SPEED)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Hero(GameBasic):
    """ 英雄精灵 """
    def __init__(self):
        super().__init__('./images/me1.png', 0)
        self.rect.bottom = SCREEN_RECT.height - 120
        self.rect.centerx = SCREEN_RECT.width / 2
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

    def fire(self):
        for i in (0, 1, 2):
            bullet = Bullet()
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.bottom = self.rect.y - 20 * i
            self.bullets.add(bullet)


