# enemy.py
# Định nghĩa các loại kẻ địch (Tàu do thám, Tàu bắn tỉa, Tàu cảm tử và Boss siêu cấp)

import pygame
import random
import math
import config
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, health, points, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.x_float = float(x)
        self.y_float = float(y)
        self.color = color
        self.health = health
        self.max_health = health
        self.points = points
        self.speed = speed
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(center=(int(self.x_float), int(self.y_float)))
        
        self.shoot_timer = random.randint(30, 90)

    def update(self, player_pos, particle_system):
        # Di chuyển cơ bản đi xuống dưới
        self.y_float += self.speed
        self.rect.center = (int(self.x_float), int(self.y_float))
        
        # Tạo hiệu ứng hạt động cơ phía sau (bay lên trên vì tàu bay xuống)
        particle_system.spawn_trail(self.rect.centerx, self.rect.top, self.color, size=2)
        
        # Hủy nếu bay ra ngoài cạnh dưới màn hình
        if self.rect.top > config.SCREEN_HEIGHT + 20:
            self.kill()

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def shoot(self):
        # Trả về danh sách đạn (mặc định lớp cha không bắn)
        return []

    def draw(self, surface):
        # Vẽ quầng sáng Neon bao quanh tàu địch
        glow_size = max(self.width, self.height)
        glow_surf = config.get_glow_surf(self.color, int(glow_size * 0.75))
        surface.blit(glow_surf, glow_surf.get_rect(center=self.rect.center), special_flags=pygame.BLEND_RGB_ADD)
        
        # Vẽ thân tàu sắc nét
        surface.blit(self.image, self.rect)


class ScoutEnemy(Enemy):
    """Kẻ địch do thám: Di chuyển nhanh theo đường zic-zac gợn sóng, máu giấy"""
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, config.COLOR_MAGENTA, health=12, points=100, speed=3.5)
        self.spawn_x = x
        self.wave_timer = random.uniform(0, 100)
        
        # Vẽ tàu hình tam giác ngược hướng xuống dưới
        points = [(self.width // 2, self.height), (0, 0), (self.width // 2, 8), (self.width, 0)]
        pygame.draw.polygon(self.image, self.color, points, 2)

    def update(self, player_pos, particle_system):
        self.y_float += self.speed
        
        # Di chuyển dạng hình sin (zic-zac)
        self.wave_timer += 0.05
        self.x_float = self.spawn_x + math.sin(self.wave_timer) * 80
        
        self.rect.center = (int(self.x_float), int(self.y_float))
        particle_system.spawn_trail(self.rect.centerx, self.rect.top, self.color, size=2)
        
        if self.rect.top > config.SCREEN_HEIGHT + 20:
            self.kill()


class ShooterEnemy(Enemy):
    """Kẻ địch tầm xa: Đi xuống một khoảng, dừng lại bắn đạn laser rồi di chuyển tiếp"""
    def __init__(self, x, y):
        super().__init__(x, y, 36, 36, config.COLOR_MAGENTA, health=25, points=200, speed=2.0)
        self.stop_y = random.randint(100, 350)
        self.state = "moving_to_stop"  # moving_to_stop, shooting, leaving
        self.state_timer = 180  # dừng bắn trong 3 giây (180 frame)
        
        # Vẽ tàu hình lục giác sắc cạnh
        points = [(self.width // 2, self.height), (0, self.height // 3), (self.width // 4, 0), 
                  (self.width * 3 // 4, 0), (self.width, self.height // 3)]
        pygame.draw.polygon(self.image, self.color, points, 2)
        # Lõi phát sáng trắng ở giữa
        pygame.draw.circle(self.image, config.COLOR_WHITE, (self.width // 2, self.height // 2), 4)

    def update(self, player_pos, particle_system):
        if self.state == "moving_to_stop":
            self.y_float += self.speed
            if self.y_float >= self.stop_y:
                self.y_float = self.stop_y
                self.state = "shooting"
        elif self.state == "shooting":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "leaving"
        elif self.state == "leaving":
            self.y_float += self.speed * 1.5
            
        self.rect.center = (int(self.x_float), int(self.y_float))
        particle_system.spawn_trail(self.rect.centerx, self.rect.top, self.color, size=2)
        
        # Xóa nếu thoát khỏi màn hình
        if self.rect.top > config.SCREEN_HEIGHT + 20:
            self.kill()

    def shoot(self):
        if self.state == "shooting":
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(60, 100) # giãn cách bắn
                # Bắn đạn thẳng xuống
                return [Bullet(self.rect.centerx, self.rect.bottom, 0, 7, config.COLOR_MAGENTA, is_enemy=True, radius=6, damage=15)]
        return []


class KamikazeEnemy(Enemy):
    """Kẻ địch cảm tử: Phát sáng đỏ, lao nhanh trực diện vào vị trí phi thuyền người chơi"""
    def __init__(self, x, y):
        super().__init__(x, y, 26, 26, config.COLOR_RED, health=15, points=150, speed=4.5)
        self.dx = 0
        self.dy = 1
        self.targeted = False
        
        # Vẽ tàu dạng chữ X hoặc hình kim cương nhọn
        points = [(self.width // 2, 0), (self.width, self.height // 2), (self.width // 2, self.height), (0, self.height // 2)]
        pygame.draw.polygon(self.image, self.color, points, 2)
        # Nét gạch chéo hầm hố
        pygame.draw.line(self.image, config.COLOR_RED, (0, 0), (self.width, self.height), 1)

    def update(self, player_pos, particle_system):
        # Khóa mục tiêu hướng về người chơi khi bay tới cự ly y = 150
        if not self.targeted and self.y_float > 100:
            px, py = player_pos
            angle = math.atan2(py - self.y_float, px - self.x_float)
            # Tăng tốc lao thẳng
            self.dx = math.cos(angle)
            self.dy = math.sin(angle)
            self.speed = 6.5
            self.targeted = True
            
        if not self.targeted:
            self.y_float += self.speed
        else:
            self.x_float += self.dx * self.speed
            self.y_float += self.dy * self.speed
            
        self.rect.center = (int(self.x_float), int(self.y_float))
        particle_system.spawn_trail(self.rect.centerx, self.rect.top, self.color, size=3)
        
        if (self.rect.top > config.SCREEN_HEIGHT + 20 or 
            self.rect.right < -20 or 
            self.rect.left > config.SCREEN_WIDTH + 20):
            self.kill()


class BossEnemy(Enemy):
    """Boss khổng lồ: Xuất hiện ở trung tâm, di chuyển qua lại, bắn đạn liên tục vòng tròn"""
    def __init__(self, x, y):
        super().__init__(x, y, 160, 80, config.COLOR_MAGENTA, health=600, points=2000, speed=1.2)
        self.dir = 1  # hướng di chuyển ngang (1: phải, -1: trái)
        self.bullet_angle = 0
        self.shoot_timer = 40
        self.attack_pattern = 0 # 0: đạn tròn, 1: chùm laser tập trung
        self.pattern_timer = 300 # 5 giây chuyển đòn bắn 1 lần
        
        # Vẽ cấu trúc tàu Boss hầm hố nhiều chi tiết Neon
        pygame.draw.polygon(self.image, config.COLOR_MAGENTA, 
                            [(self.width // 2, self.height), (0, self.height // 2), 
                             (30, 0), (self.width - 30, 0), (self.width, self.height // 2)], 3)
        
        # Vẽ đôi mắt phát sáng đỏ
        pygame.draw.circle(self.image, config.COLOR_RED, (self.width // 3, self.height // 2), 6)
        pygame.draw.circle(self.image, config.COLOR_RED, (self.width * 2 // 3, self.height // 2), 6)
        # Lõi động cơ phát sáng lớn ở tâm
        pygame.draw.circle(self.image, config.COLOR_WHITE, (self.width // 2, 15), 12, 3)

    def update(self, player_pos, particle_system):
        # Boss từ trên bay xuống dừng lại ở y = 120
        if self.y_float < 120:
            self.y_float += self.speed
        else:
            self.y_float = 120
            # Di chuyển qua lại theo chiều ngang màn hình
            self.x_float += self.speed * self.dir
            if self.x_float > config.SCREEN_WIDTH - 120:
                self.dir = -1
            elif self.x_float < 120:
                self.dir = 1
                
        self.rect.center = (int(self.x_float), int(self.y_float))
        
        # Sinh khói động cơ cực lớn phía sau Boss
        particle_system.spawn_trail(self.rect.centerx - 40, self.rect.top, config.COLOR_MAGENTA, size=4)
        particle_system.spawn_trail(self.rect.centerx + 40, self.rect.top, config.COLOR_MAGENTA, size=4)
        
        # Chuyển đổi đòn tấn công
        self.pattern_timer -= 1
        if self.pattern_timer <= 0:
            self.pattern_timer = 300
            self.attack_pattern = (self.attack_pattern + 1) % 2

    def shoot(self):
        # Boss không bắn khi chưa vào vị trí chiến đấu
        if self.y_float < 120:
            return []
            
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            bullets = []
            if self.attack_pattern == 0:
                # KIỂU 1: Bắn đạn tròn tỏa ra 12 hướng xung quanh Boss
                self.shoot_timer = 70  # thời gian nạp lại
                num_bullets = 12
                for i in range(num_bullets):
                    angle = (i * (2 * math.pi / num_bullets)) + self.bullet_angle
                    bullets.append(Bullet(
                        self.rect.centerx, self.rect.bottom - 10,
                        math.cos(angle) * 5.0, math.sin(angle) * 5.0,
                        config.COLOR_MAGENTA, is_enemy=True, radius=6, damage=10
                    ))
                self.bullet_angle += 0.2  # xoay nhẹ góc ở đợt bắn sau
            else:
                # KIỂU 2: Bắn chùm 3 đạn lớn dồn dập đuổi theo người chơi
                self.shoot_timer = 25  # nạp đạn nhanh hơn
                # Bắn lệch góc sang trái, phải và thẳng hướng
                bullets.append(Bullet(self.rect.centerx, self.rect.bottom, -1.5, 6, config.COLOR_RED, is_enemy=True, radius=8, damage=15))
                bullets.append(Bullet(self.rect.centerx, self.rect.bottom, 0, 7, config.COLOR_RED, is_enemy=True, radius=9, damage=18))
                bullets.append(Bullet(self.rect.centerx, self.rect.bottom, 1.5, 6, config.COLOR_RED, is_enemy=True, radius=8, damage=15))
            return bullets
        return []
