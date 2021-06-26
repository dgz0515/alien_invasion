import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
    # 初始化游戏、创建窗口
    pygame.init()
    ai_settings = Settings()
    window = pygame.display.set_mode((ai_settings.win_width, ai_settings.win_height))
    pygame.display.set_caption(ai_settings.name)
    
    play_button = Button(ai_settings, window, "Play")

    # 创建一艘飞船
    ship = Ship(ai_settings, window)
    # 有效子弹组
    bullets = Group()
    # 外星人
    aliens = Group()
    gf.create_fleet(ai_settings, window, aliens, ship)

    # 游戏进度信息
    stats = GameStats(ai_settings)
    score = ScoreBoard(ai_settings, window, stats)

    # 游戏主循环
    while True:
        # 事件监听循环
        gf.check_events(ai_settings, window, ship, aliens, bullets, stats, play_button, score)
        
        if stats.game_active:
            # 飞船更新
            ship.update(bullets)

            # 子弹更新
            gf.update_bullets(ai_settings, window, ship, aliens, bullets, stats, score)

            # 外星人更新
            gf.update_aliens(ai_settings, stats, window, aliens, ship, bullets, score)

        # 重新绘制
        gf.update_window(ai_settings, window, ship, bullets, aliens, stats, play_button, score)

if __name__=="__main__":
    run_game()