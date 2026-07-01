# particle.py
# Hệ thống hạt phát sáng (Glow Particles) tối ưu hóa hiệu năng

import random
import pygame
import config

class Particle:
    def __init__(self, x, y, vx, vy, color, radius, life):
        self.x = x
        self.x_float = float(x)
        self.y = y
        self.y_float = float(y)
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.initial_radius = radius
        self.max_life = life
        self.life = life

    def update(self):
        # Cập nhật tọa độ thực
        self.x_float += self.vx
        self.y_float += self.vy
        self.x = int(self.x_float)
        self.y = int(self.y_float)
        
        # Giảm tuổi thọ của hạt
        self.life -= 1
        
        # Tính tỷ lệ tuổi thọ còn lại
        life_ratio = self.life / self.max_life
        
        # Hạt thu nhỏ và mờ dần theo thời gian
        self.radius = max(1, int(self.initial_radius * life_ratio))
        
    def is_dead(self):
        return self.life <= 0

    def draw(self, surface):
        if self.radius <= 0:
            return
            
        # Lấy hình tròn phát sáng từ cache
        # Chúng ta dùng bán kính hạt làm bán kính quầng sáng
        glow_surf = config.get_glow_surf(self.color, self.radius * 2)
        glow_rect = glow_surf.get_rect(center=(self.x, self.y))
        
        # Vẽ cộng màu lên màn hình (BLEND_RGB_ADD)
        surface.blit(glow_surf, glow_rect, special_flags=pygame.BLEND_RGB_ADD)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, vx, vy, color, radius, life):
        # Xác định giới hạn hạt dựa trên chế độ máy yếu
        limit = config.PARTICLE_LIMIT_LOW if config.LOW_SPEC_MODE else config.PARTICLE_LIMIT_NORMAL
        
        if len(self.particles) < limit:
            self.particles.append(Particle(x, y, vx, vy, color, radius, life))

    def update(self):
        # Cập nhật từng hạt và loại bỏ hạt đã chết
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

    def explode(self, x, y, color, speed_mult=1.0):
        """Tạo vụ nổ tia lửa phát sáng tại tọa độ (x, y)"""
        # Giảm số hạt tạo ra nếu cấu hình máy yếu
        num_particles = 12 if config.LOW_SPEC_MODE else 35
        
        for _ in range(num_particles):
            angle = random.uniform(0, 6.28) # 2 * pi
            speed = random.uniform(2.0, 7.0) * speed_mult
            vx = random.uniform(-1.0, 1.0) * speed
            vy = random.uniform(-1.0, 1.0) * speed
            
            radius = random.randint(3, 7)
            life = random.randint(15, 30)
            
            self.add_particle(x, y, vx, vy, color, radius, life)

    def spawn_trail(self, x, y, color, size=2):
        """Tạo hạt khói động cơ/đường đạn phía sau vật thể"""
        # Với máy yếu, thỉnh thoảng mới sinh hạt khói để tiết kiệm tài nguyên
        if config.LOW_SPEC_MODE and random.random() > 0.4:
            return
            
        vx = random.uniform(-0.5, 0.5)
        # Khói bay ngược lên trên (đối với tàu địch bay xuống) hoặc rơi nhẹ xuống
        vy = random.uniform(0.5, 1.5)
        
        radius = random.randint(1, size)
        life = random.randint(10, 20)
        
        self.add_particle(x, y, vx, vy, color, radius, life)
