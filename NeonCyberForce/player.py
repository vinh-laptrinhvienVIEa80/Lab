# player.py
# Định nghĩa phi thuyền người chơi với các hiệu ứng hạt động cơ, khiên neon, và nâng cấp vũ khí

import pygame
import config
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 40
        
        # Vị trí thực tế (dạng số thực)
        self.x_float = float(x)
        self.y_float = float(y)
        
        # Tạo ảnh phi thuyền (hình đa giác Neon Cyan vẽ sắc nét)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        
        # Vẽ thân tàu đa giác nét mảnh (Cyberpunk style)
        points = [(self.width // 2, 0), (0, self.height - 10), (self.width // 2, self.height - 18), (self.width, self.height - 10)]
        pygame.draw.polygon(self.image, config.COLOR_CYAN, points, 2)
        # Nối thêm cánh phụ
        pygame.draw.line(self.image, config.COLOR_WHITE, (self.width // 2, 4), (self.width // 2, self.height - 18), 2)
        
        self.rect = self.image.get_rect(center=(int(self.x_float), int(self.y_float)))
        
        # Chỉ số cơ bản
        self.speed = 6.0
        self.max_health = 100
        self.health = 100
        self.max_shield = 100
        self.shield = 100
        
        # Thời gian hồi khiên & đạn
        self.shoot_cooldown = 12  # số frame giữa mỗi lần bắn
        self.shoot_timer = 0
        self.shield_recharge_timer = 0
        
        # Cấp độ vũ khí (1: Đơn, 2: Đôi, 3: Ba tia, 4: Siêu cấp)
        self.weapon_level = 1
        
        # Quầng sáng bao quanh khiên (Pre-rendered)
        self.shield_glow_radius = 35
        self.shield_glow = config.get_glow_surf(config.COLOR_CYAN, self.shield_glow_radius * 2)

    def move(self, keys):
        # Tính toán vector di chuyển từ bàn phím
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
            
        # Chuẩn hóa vector di chuyển chéo để tốc độ luôn ổn định
        if dx != 0 and dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length
            
        # Di chuyển và giữ tàu trong màn hình
        self.x_float += dx * self.speed
        self.y_float += dy * self.speed
        
        # Khóa biên giới hạn
        self.x_float = max(self.width // 2, min(config.SCREEN_WIDTH - self.width // 2, self.x_float))
        self.y_float = max(self.height // 2, min(config.SCREEN_HEIGHT - self.height // 2, self.y_float))
        
        self.rect.center = (int(self.x_float), int(self.y_float))

    def update(self, keys, particle_system):
        # Cập nhật di chuyển
        self.move(keys)
        
        # Đếm ngược thời gian bắn
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            
        # Tự động hồi phục khiên từ từ nếu không nhận sát thương gần đây
        if self.shield_recharge_timer > 0:
            self.shield_recharge_timer -= 1
        elif self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + 0.15)
            
        # Tạo khói/hạt động cơ phía sau đuôi tàu
        engine_x = self.rect.centerx
        engine_y = self.rect.bottom - 10
        particle_system.spawn_trail(engine_x, engine_y, config.COLOR_CYAN, size=3)

    def shoot(self):
        """Bắn đạn dựa trên cấp độ vũ khí hiện tại"""
        if self.shoot_timer > 0:
            return []
            
        self.shoot_timer = self.shoot_cooldown
        bullets = []
        
        x = self.rect.centerx
        y = self.rect.top
        
        if self.weapon_level == 1:
            # 1 tia thẳng đứng
            bullets.append(Bullet(x, y, 0, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
        elif self.weapon_level == 2:
            # 2 tia song song từ 2 bên cánh
            bullets.append(Bullet(x - 12, y + 10, 0, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
            bullets.append(Bullet(x + 12, y + 10, 0, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
        elif self.weapon_level == 3:
            # 3 tia tỏa hình quạt
            bullets.append(Bullet(x, y, 0, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
            bullets.append(Bullet(x, y, -3, -11.5, config.COLOR_CYAN, is_enemy=False, radius=7, damage=10))
            bullets.append(Bullet(x, y, 3, -11.5, config.COLOR_CYAN, is_enemy=False, radius=7, damage=10))
        else:
            # Siêu vũ khí: 3 tia quạt + 2 tên lửa plasma nổ lớn bên cạnh
            bullets.append(Bullet(x, y, 0, -13, config.COLOR_CYAN, is_enemy=False, radius=7, damage=14))
            bullets.append(Bullet(x, y, -3, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
            bullets.append(Bullet(x, y, 3, -12, config.COLOR_CYAN, is_enemy=False, radius=7, damage=12))
            # Quả cầu plasma chậm nhưng cực mạnh ở rìa
            bullets.append(Bullet(x - 22, y + 15, -1, -9, config.COLOR_YELLOW, is_enemy=False, radius=12, damage=25))
            bullets.append(Bullet(x + 22, y + 15, 1, -9, config.COLOR_YELLOW, is_enemy=False, radius=12, damage=25))
            
        return bullets

    def take_damage(self, amount):
        """Giảm khiên trước, sau đó mới giảm vào máu"""
        # Đặt lại bộ đếm thời gian hồi khiên
        self.shield_recharge_timer = 180  # 3 giây không bị bắn mới hồi khiên
        
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                # Sát thương dư tràn vào máu
                self.health += self.shield
                self.shield = 0
        else:
            self.health -= amount
            
        return self.health <= 0

    def draw(self, surface):
        # 1. Vẽ quầng sáng khiên phát quang (Glow Shield)
        if self.shield > 0:
            # Độ mờ của khiên tỷ lệ với lượng khiên còn lại
            alpha_mult = self.shield / self.max_shield
            shield_surf = self.shield_glow.copy()
            
            # Làm nhạt bớt quầng sáng khiên nếu khiên gần hết
            if alpha_mult < 1.0:
                shield_surf.fill((255, 255, 255, int(255 * alpha_mult)), special_flags=pygame.BLEND_RGBA_MULT)
                
            shield_rect = shield_surf.get_rect(center=self.rect.center)
            surface.blit(shield_surf, shield_rect, special_flags=pygame.BLEND_RGB_ADD)
            
            # Vẽ viền ngoài mỏng của vòng tròn khiên
            pygame.draw.circle(surface, config.COLOR_CYAN, self.rect.center, self.shield_glow_radius - 2, 1)

        # 2. Vẽ phi thuyền (Emissive render - Blit phi thuyền vẽ đa giác)
        # Tạo quầng sáng nhỏ cho thân phi thuyền
        ship_glow = config.get_glow_surf(config.COLOR_CYAN, 20)
        surface.blit(ship_glow, ship_glow.get_rect(center=self.rect.center), special_flags=pygame.BLEND_RGB_ADD)
        
        # Vẽ thân phi thuyền sắc nét lên trên
        surface.blit(self.image, self.rect)
