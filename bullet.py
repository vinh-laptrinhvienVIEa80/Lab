# bullet.py
# Định nghĩa các loại đạn laser phát sáng (Glow Bullets) trong game

import pygame
import config

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, color, is_enemy=False, radius=8, damage=10):
        super().__init__()
        self.x_float = float(x)
        self.y_float = float(y)
        self.dx = dx
        self.dy = dy
        self.color = color
        self.is_enemy = is_enemy
        self.radius = radius
        self.damage = damage
        
        # Tạo quầng sáng phát quang dùng cache
        self.image = config.get_glow_surf(self.color, self.radius * 2)
        self.rect = self.image.get_rect(center=(int(self.x_float), int(self.y_float)))

    def update(self):
        # Di chuyển đạn
        self.x_float += self.dx
        self.y_float += self.dy
        
        # Cập nhật rect va chạm
        self.rect.center = (int(self.x_float), int(self.y_float))
        
        # Xóa đạn nếu bay ra ngoài màn hình
        if (self.rect.bottom < -20 or 
            self.rect.top > config.SCREEN_HEIGHT + 20 or 
            self.rect.right < -20 or 
            self.rect.left > config.SCREEN_WIDTH + 20):
            self.kill()

    def draw(self, surface):
        # Vẽ đạn lên màn hình sử dụng cơ chế cộng màu sáng
        surface.blit(self.image, self.rect, special_flags=pygame.BLEND_RGB_ADD)
