import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """外星人"""
    def __init__(self, ai_settings, window):
        """初始化外星人"""
        super(Alien, self).__init__()
        self.window = window
        self.ai_settings = ai_settings

        # 加载图像、设置rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # 初始位置在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 位置
        self.x = float(self.rect.x)

    def blitme(self):
        """绘制"""
        self.window.blit(self.image, self.rect)

    def update(self):
        """向右移动"""
        self.x += self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """到达边缘，return True"""
        win_rect = self.window.get_rect()
        if self.rect.right >= win_rect.right or self.rect.left <= 0:
            return True
    