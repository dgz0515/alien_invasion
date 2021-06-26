import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def create_alien(ai_settings, window, aliens, alien_number, row):
    # 创建一个外星人
    alien = Alien(ai_settings, window)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row
    aliens.add(alien)

def get_number_aliens_cols(ai_settings, window):
    # 创建一个外星人、用来计算一行可显示多少外星人
    alien = Alien(ai_settings, window)
    alien_width = alien.rect.width
    available_space_x = ai_settings.win_width - 2*alien_width
    number_aliens_cols = int(available_space_x/(2*alien_width))
    return number_aliens_cols

def get_number_alien_rows(ai_settings, window, ship):
    """计算可显示的行数"""
    alien = Alien(ai_settings, window)
    alien_height = alien.rect.height
    available_space_y = ai_settings.win_height - 3 * alien_height - ship.rect.height
    number_aliens_rows = int(available_space_y / (2*alien_height))
    return number_aliens_rows

def create_fleet(ai_settings, window, aliens, ship):
    """创建外星人群"""
    number_aliens_cols = get_number_aliens_cols(ai_settings, window)
    number_aliens_rows = get_number_alien_rows(ai_settings, window, ship)
    
    # 创建一行外星人
    for row in range(number_aliens_rows):
        for alien_number in range(number_aliens_cols):
            create_alien(ai_settings, window, aliens, alien_number, row)

def check_keydown_events(event, ai_settings, window, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ship.fire = True
    elif event.key == pygame.K_e:
        ai_settings.bullet_width = 800
    elif event.key == pygame.K_r:
        ai_settings.bullet_width = 3

def check_keyup_events(event, ship):
    """响应松键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        ship.fire = False

def check_play_button(ai_settings, window, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, score):
    """点击playbutton开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.init_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()
        # 清空子弹和外星人
        aliens.empty()
        bullets.empty()
        # 创建新的外星人
        create_fleet(ai_settings, window, aliens, ship)
        ship.center_ship()


def check_events(ai_settings, window, ship, aliens, bullets, stats, play_button, score):
    """检测鼠标和键盘事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, window, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, window, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, score)

def update_window(ai_settings, window, ship, bullets, aliens, stats, play_button, score):
    """更新窗口"""
    window.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(window)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    score.show_score()
    
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def check_bullet_alien_collision(ai_settings, window, ship, aliens, bullets, stats, score):
    """处理子弹与外星人的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien_s in collisions.values():
            stats.score += ai_settings.alien_points * len(alien_s)
            score.prep_score()
        check_high_score(stats, score)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        score.prep_level()
        create_fleet(ai_settings, window, aliens, ship)
    

def update_bullets(ai_settings, window, ship, aliens, bullets, stats, score):
    """更新子弹"""
    # 位置
    bullets.update()
    # 删除不可见的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, window, ship, aliens, bullets, stats, score)

def check_fleet_edges(ai_settings, aliens):
    """检测所有外星人是否触及边缘"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将外星人下移、改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, window, aliens, ship, bullets, score):
    """更新外星人"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, window, ship, aliens, bullets, score)
    
    check_aliens_bottom(ai_settings, stats, window, ship, aliens, bullets, score)

def ship_hit(ai_settings, stats, window, ship, aliens, bullets, score):
    """飞船碰撞处理"""
    if stats.ship_left > 0:
        # 飞船数量-1
        stats.ship_left -= 1
        score.prep_ships()
        # 清空子弹和外星人
        aliens.empty()
        bullets.empty()
        # 创建新的外星人
        create_fleet(ai_settings, window, aliens, ship)
        ship.center_ship()
        # 暂停半秒
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, window, ship, aliens, bullets, score):
    """检测是否有外星人入侵到了底部"""
    win_rect = window.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= win_rect.bottom:
            ship_hit(ai_settings, stats, window, ship, aliens, bullets, score)

def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()