import pygame
from pygame.sprite import Sprite
from bullet import Bullet

class Ship(Sprite):
    def __init__(self, ai_settings, window):
        """初始化飞船并设置初始位置"""
        super(Ship, self).__init__()

        self.window = window
        self.ai_settings = ai_settings
        
        # 加载飞船图像、获取外接矩形
        self.image = pygame.image.load('images/ship.png')
        # rect: center\centerx\centery\top\bottom\left\right
        self.rect = self.image.get_rect()
        self.win_rect = window.get_rect()

        # 设置飞船初始位置
        self.rect.centerx = self.win_rect.centerx
        self.rect.bottom = self.win_rect.bottom

        # 在center中存储浮点数值
        self.centerx = float(self.rect.centerx)

        # 移动控制
        self.moving_right = False
        self.moving_left = False

        # 火炮控制
        self.fire = False
        self.fire_time = ai_settings.fire_time # 炮弹装填时间

    def blitme(self):
        """在指定位置绘制飞船"""
        self.window.blit(self.image, self.rect)
    
    def fire_bullet(self, bullets):
        # 创建子弹、加入子弹组
        if len(bullets)  < self.ai_settings.bullet_allowed:
            new_bullet = Bullet(self.ai_settings, self.window, self)
            bullets.add(new_bullet)

    def update(self, bullets):
        """根据控制参数移动飞船"""
        # 计算飞船位置
        if self.moving_right and self.rect.right < self.win_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        
        # 更新飞船位置
        self.rect.centerx = self.centerx

        # 开炮
        if self.fire:
            if self.fire_time > 0:
                self.fire_time -= 1
            else:
                self.fire_bullet(bullets)
                self.fire_time = self.ai_settings.fire_time

    def center_ship(self):
        """飞船居中"""
        self.centerx = self.win_rect.centerx

