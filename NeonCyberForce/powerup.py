# powerup.py
# Định nghĩa các vật phẩm nâng cấp (Power-ups) rơi ra khi tiêu diệt tàu địch

import pygame
import random
import math
import config

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.kind = kind  # "heal", "shield", "upgrade"
        self.width = 24
        self.height = 24
        self.x_float = float(x)
        self.y_float = float(y)
        self.wave_timer = random.uniform(0, 100)
        self.speed = 1.8
        
        # Chọn màu sắc theo loại vật phẩm
        if self.kind == "heal":
            self.color = config.COLOR_GREEN
        elif self.kind == "shield":
            self.color = config.COLOR_CYAN
        else: # upgrade
            self.color = config.COLOR_YELLOW
            
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        
        # Vẽ biểu tượng sắc nét trên ô vuông Neon
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), 2)
        
        # Vẽ ký hiệu đặc trưng ở tâm
        if self.kind == "heal":
            # Vẽ dấu thập hồi máu (+)
            pygame.draw.line(self.image, self.color, (self.width // 2, 5), (self.width // 2, self.height - 5), 2)
            pygame.draw.line(self.image, self.color, (5, self.height // 2), (self.width - 5, self.height // 2), 2)
        elif self.kind == "shield":
            # Vẽ hình khiên tam giác bảo vệ
            points = [(self.width // 2, 4), (self.width - 4, 8), (self.width // 2, self.height - 4), (4, 8)]
            pygame.draw.polygon(self.image, self.color, points, 2)
        else: # upgrade
            # Vẽ mũi tên hướng lên biểu thị nâng cấp vũ khí (^)
            pygame.draw.line(self.image, self.color, (self.width // 2, 5), (4, 13), 2)
            pygame.draw.line(self.image, self.color, (self.width // 2, 5), (self.width - 4, 13), 2)
            pygame.draw.line(self.image, self.color, (self.width // 2, 5), (self.width // 2, self.height - 5), 2)
            
        self.rect = self.image.get_rect(center=(int(self.x_float), int(self.y_float)))

    def update(self):
        # Trôi xuống dưới và lắc lư ngang nhẹ nhàng
        self.y_float += self.speed
        self.wave_timer += 0.04
        current_x = self.x_float + math.sin(self.wave_timer) * 20
        
        self.rect.center = (int(current_x), int(self.y_float))
        
        # Tự động hủy nếu trôi quá biên dưới
        if self.rect.top > config.SCREEN_HEIGHT + 20:
            self.kill()

    def draw(self, surface):
        # Tạo quầng sáng phát xạ của vật phẩm
        glow_surf = config.get_glow_surf(self.color, 16)
        surface.blit(glow_surf, glow_surf.get_rect(center=self.rect.center), special_flags=pygame.BLEND_RGB_ADD)
        
        # Vẽ biểu tượng vật phẩm lên trên
        surface.blit(self.image, self.rect)
