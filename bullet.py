import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理所有子弹"""
    def __init__(self, ai_settings, window, ship):
        """在飞船位置创建子弹"""
        super(Bullet, self).__init__()
        self.window = window

        # 创建子弹、设置位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 子弹动态位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 计算子弹位置
        self.y -= self.speed_factor
        # 更新子弹位置
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.window, self.color, self.rect)