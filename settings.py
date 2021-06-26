class Settings():
    """存储游戏的所有设置"""
    def __init__(self):
        """初始化游戏的设置"""
        # 游戏设置
        self.name = "Alien Invasion"
        self.win_width = 1200
        self.win_height = 800
        self.bg_color = (200, 200, 200)
        # 飞船设置
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3
        self.fire_time = 10
        # 子弹设置
        # self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (50, 50, 50)
        self.bullet_allowed = 100
        # 外星人设置
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # self.fleet_direction = 1 # 1 右 -1 左

        # 增速比例
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """动态设置"""
        # 速度设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # 移动方向
        self.fleet_direction = 1

        # 得分值
        self.alien_points = 50
    
    def increase_speed(self):
        """增速"""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

