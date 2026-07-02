# main.py
# File chạy chính của game Bắn Tàu Vũ Trụ Neon Cyberpunk (RTX-Style)
# Tích hợp toàn bộ hệ thống hạt, đạn, kẻ địch, vật phẩm nâng cấp và tối ưu hóa hiệu năng

import pygame
import sys
import random
import config
from player import Player
from enemy import ScoutEnemy, ShooterEnemy, KamikazeEnemy, BossEnemy
from particle import ParticleSystem
from powerup import PowerUp
from ui import UI, ScreenShake

def main():
    # Khởi tạo Pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Neon Cyber-Force (RTX-Style Pygame)")
    clock = pygame.time.Clock()

    # Khởi tạo các hệ thống dùng chung
    particle_system = ParticleSystem()
    ui = UI()
    shake_system = ScreenShake()

    # Các nhóm Sprite quản lý va chạm
    player_group = pygame.sprite.GroupSingle()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Biến trạng thái trò chơi
    game_state = "MENU" # MENU, PLAYING, GAME_OVER
    score = 0
    
    # Cấu hình chuyển động nền lưới (Cyberpunk Grid Background)
    grid_y = 0.0
    grid_speed = 1.0
    grid_size = 60

    # Các mốc tính thời gian sinh quái
    spawn_timer = 0
    spawn_cooldown = 70  # số frame giữa các lần sinh quái nhỏ

    # Quản lý sự kiện Boss xuất hiện
    boss_spawned = False
    boss_active = False
    boss_ref = None

    def reset_game():
        nonlocal score, spawn_timer, boss_spawned, boss_active, boss_ref
        score = 0
        spawn_timer = 0
        boss_spawned = False
        boss_active = False
        boss_ref = None
        
        # Làm sạch các nhóm Sprite cũ
        player_bullets.empty()
        enemy_bullets.empty()
        enemies.empty()
        powerups.empty()
        particle_system.particles.clear()
        
        # Khởi tạo người chơi ở vị trí trung tâm phía dưới
        player = Player(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100)
        player_group.add(player)
        return player

    player = reset_game()

    # Vòng lặp chính của Game
    while True:
        # 1. XỬ LÝ SỰ KIỆN (Events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    # Phím tắt F1: Bật/Tắt chế độ máy cấu hình yếu
                    config.LOW_SPEC_MODE = not config.LOW_SPEC_MODE
                    # Xóa bộ đệm quầng sáng cũ để tạo lại theo cấu hình mới
                    config._glow_cache.clear()
                    
                if game_state == "MENU":
                    if event.key == pygame.K_RETURN:
                        player = reset_game()
                        game_state = "PLAYING"
                elif game_state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        player = reset_game()
                        game_state = "PLAYING"

        # 2. CẬP NHẬT LOGIC GAME (Trạng thái PLAYING)
        if game_state == "PLAYING":
            # Đọc phím bấm liên tục (để di chuyển và giữ phím Space bắn đạn liên tục)
            keys = pygame.key.get_pressed()
            
            # Cập nhật người chơi
            player.update(keys, particle_system)
            
            # Bắn đạn nếu nhấn SPACE
            if keys[pygame.K_SPACE]:
                new_bullets = player.shoot()
                for b in new_bullets:
                    player_bullets.add(b)
                    
            # Cập nhật các viên đạn
            player_bullets.update()
            enemy_bullets.update()
            
            # Cập nhật vật phẩm nâng cấp
            powerups.update()

            # Quản lý sinh Kẻ địch (Enemy Spawning)
            if not boss_active:
                spawn_timer += 1
                if spawn_timer >= spawn_cooldown:
                    spawn_timer = 0
                    # Tăng độ khó theo điểm số (giảm thời gian cooldown)
                    spawn_cooldown = max(25, 70 - int(score / 300))
                    
                    # Tỉ lệ sinh các loại quái khác nhau dựa trên điểm số
                    x_pos = random.randint(40, config.SCREEN_WIDTH - 40)
                    r = random.random()
                    
                    if score < 600:
                        # Chỉ sinh Tàu do thám hoặc Cảm tử
                        if r < 0.65:
                            enemies.add(ScoutEnemy(x_pos, -20))
                        else:
                            enemies.add(KamikazeEnemy(x_pos, -20))
                    else:
                        # Điểm cao: Sinh thêm Tàu bắn tỉa (Shooter)
                        if r < 0.4:
                            enemies.add(ScoutEnemy(x_pos, -20))
                        elif r < 0.75:
                            enemies.add(ShooterEnemy(x_pos, -20))
                        else:
                            enemies.add(KamikazeEnemy(x_pos, -20))
                            
                # Sự kiện triệu hồi Boss khi người chơi đạt mốc 2500 điểm
                if score >= 2500 and not boss_spawned:
                    boss_active = True
                    boss_spawned = True
                    boss_ref = BossEnemy(config.SCREEN_WIDTH // 2, -100)
                    enemies.add(boss_ref)

            # Cập nhật kẻ địch và xử lý đạn địch bắn ra
            for enemy in enemies:
                # Cập nhật chuyển động tàu địch
                enemy.update(player.rect.center, particle_system)
                # Tàu địch bắn đạn
                eb = enemy.shoot()
                for b in eb:
                    enemy_bullets.add(b)

            # Cập nhật các hạt nổ
            particle_system.update()

            # 3. XỬ LÝ VA CHẠM (Collision System)
            
            # A. Đạn người chơi bắn trúng Kẻ địch
            for bullet in player_bullets:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
                for enemy in hit_enemies:
                    bullet.kill() # Tiêu hủy viên đạn
                    
                    # Kẻ địch nhận sát thương
                    is_dead = enemy.take_damage(bullet.damage)
                    # Tạo hạt lửa phát sáng nhỏ tại điểm va chạm
                    particle_system.explode(bullet.rect.centerx, bullet.rect.centery, enemy.color, speed_mult=0.6)
                    
                    if is_dead:
                        # Kẻ địch bị nổ tung hoàn toàn
                        particle_system.explode(enemy.rect.centerx, enemy.rect.centery, enemy.color, speed_mult=1.3)
                        shake_system.trigger(intensity=4, duration=8)
                        score += enemy.points
                        enemy.kill() # Xóa kẻ địch khỏi nhóm
                        
                        # Boss chết
                        if enemy == boss_ref:
                            boss_active = False
                            boss_ref = None
                            # Rung màn hình cực mạnh
                            shake_system.trigger(intensity=12, duration=35)
                            # Rơi ra 4 vật phẩm nâng cấp làm phần thưởng
                            for _ in range(4):
                                px = enemy.rect.centerx + random.randint(-40, 40)
                                py = enemy.rect.centery + random.randint(-20, 20)
                                powerups.add(PowerUp(px, py, random.choice(["heal", "shield", "upgrade"])))
                        else:
                            # 15% Tỷ lệ rơi vật phẩm khi quái thường chết
                            if random.random() < 0.15:
                                p_type = random.choice(["heal", "shield", "upgrade"])
                                powerups.add(PowerUp(enemy.rect.centerx, enemy.rect.centery, p_type))

            # B. Đạn kẻ địch bắn trúng Người chơi
            hit_player_bullets = pygame.sprite.spritecollide(player, enemy_bullets, True)
            for bullet in hit_player_bullets:
                # Người chơi nhận sát thương
                player_dead = player.take_damage(bullet.damage)
                # Tạo hạt nổ tại điểm va chạm
                particle_system.explode(bullet.rect.centerx, bullet.rect.centery, config.COLOR_CYAN, speed_mult=0.8)
                # Rung màn hình vừa
                shake_system.trigger(intensity=5, duration=10)
                
                if player_dead:
                    # Người chơi chết -> Game Over
                    particle_system.explode(player.rect.centerx, player.rect.centery, config.COLOR_WHITE, speed_mult=2.0)
                    shake_system.trigger(intensity=15, duration=40)
                    game_state = "GAME_OVER"

            # C. Người chơi va chạm trực tiếp thân tàu Kẻ địch (Đâm va)
            crashed_enemies = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in crashed_enemies:
                if enemy == boss_ref:
                    # Đâm vào Boss: Trừ 40 máu ngay lập tức
                    player_dead = player.take_damage(40)
                else:
                    # Đâm vào quái nhỏ: Quái chết, người chơi mất 20 máu
                    player_dead = player.take_damage(20)
                    particle_system.explode(enemy.rect.centerx, enemy.rect.centery, enemy.color, speed_mult=1.2)
                    enemy.kill()
                    
                shake_system.trigger(intensity=8, duration=15)
                
                if player_dead:
                    particle_system.explode(player.rect.centerx, player.rect.centery, config.COLOR_WHITE, speed_mult=2.0)
                    game_state = "GAME_OVER"

            # D. Người chơi thu thập Vật phẩm nâng cấp
            hit_powerups = pygame.sprite.spritecollide(player, powerups, True)
            for power in hit_powerups:
                # Tạo hiệu ứng hạt hút vào phi thuyền khi ăn vật phẩm
                for _ in range(12):
                    particle_system.add_particle(
                        power.rect.centerx, power.rect.centery,
                        random.uniform(-3, 3), random.uniform(-3, 3),
                        power.color, random.randint(2, 4), random.randint(10, 20)
                    )
                    
                # Áp dụng tính năng vật phẩm
                if power.kind == "heal":
                    player.health = min(player.max_health, player.health + 30)
                elif power.kind == "shield":
                    player.shield = min(player.max_shield, player.shield + 50)
                elif power.kind == "upgrade":
                    player.weapon_level = min(4, player.weapon_level + 1)

        # 4. THỰC HIỆN VẼ LÊN MÀN HÌNH (Rendering)
        # Làm sạch màn hình với màu nền tối
        screen.fill(config.COLOR_BG)
        
        # Áp dụng rung lắc màn hình (Screen Shake)
        offset_x, offset_y = shake_system.update()
        
        # Vẽ lưới tọa độ di chuyển Cyberpunk Grid (Cuộn xuống dưới)
        # Tạo hiệu ứng phi thuyền đang bay nhanh qua không gian
        if game_state == "PLAYING":
            grid_y += grid_speed
            if grid_y >= grid_size:
                grid_y = 0.0
                
        # Với máy yếu, vẽ thưa lưới hơn để tiết kiệm CPU
        step_grid = grid_size * 2 if config.LOW_SPEC_MODE else grid_size
        
        # Tạo bản vẽ phụ hỗ trợ rung lắc màn hình
        game_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        game_surf.fill(config.COLOR_BG)
        
        # Vẽ các đường lưới dọc cố định
        for x in range(0, config.SCREEN_WIDTH, step_grid):
            pygame.draw.line(game_surf, config.COLOR_GRID, (x, 0), (x, config.SCREEN_HEIGHT), 1)
            
        # Vẽ các đường lưới ngang di động cuộn xuống
        for y in range(int(grid_y) - grid_size, config.SCREEN_HEIGHT + grid_size, step_grid):
            pygame.draw.line(game_surf, config.COLOR_GRID, (0, y), (config.SCREEN_WIDTH, y), 1)

        # Vẽ vật phẩm nâng cấp
        for p in powerups:
            p.draw(game_surf)

        # Vẽ đạn người chơi và kẻ địch bằng blend cộng màu phát sáng
        for b in player_bullets:
            b.draw(game_surf)
        for b in enemy_bullets:
            b.draw(game_surf)

        # Vẽ kẻ địch
        for enemy in enemies:
            enemy.draw(game_surf)

        # Vẽ hệ thống hạt lửa nổ & khói đuôi
        particle_system.draw(game_surf)

        # Vẽ phi thuyền người chơi
        if game_state == "PLAYING":
            player.draw(game_surf)

        # Blit màn hình game lên cửa sổ chính kèm tọa độ dịch chuyển rung lắc
        screen.blit(game_surf, (offset_x, offset_y))

        # 5. VẼ GIAO DIỆN (UI Overlays)
        if game_state == "PLAYING":
            # Vẽ các thanh máu, khiên, điểm số và thông tin hướng dẫn
            ui.draw_hud(screen, player, score)
            
            # Vẽ thanh máu của Boss nếu Boss đang xuất hiện
            if boss_active and boss_ref:
                ui.draw_boss_bar(screen, boss_ref)
                
        elif game_state == "MENU":
            ui.draw_menu(screen)
            
        elif game_state == "GAME_OVER":
            ui.draw_game_over(screen, score)

        # Cập nhật toàn bộ màn hình
        pygame.display.flip()
        
        # Giới hạn khung hình chuẩn 60 FPS
        clock.tick(config.FPS)

if __name__ == "__main__":
    main()
