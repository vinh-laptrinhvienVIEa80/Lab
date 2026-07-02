# ui.py
# Quản lý giao diện người dùng HUD, màn hình Menu/GameOver và hiệu ứng rung lắc màn hình (Screen Shake)

import pygame
import random
import config

class ScreenShake:
    def __init__(self):
        self.duration = 0
        self.intensity = 0

    def trigger(self, intensity, duration):
        self.intensity = intensity
        self.duration = duration

    def update(self):
        if self.duration > 0:
            self.duration -= 1
            # Rung lắc ngẫu nhiên
            dx = random.randint(-self.intensity, self.intensity)
            dy = random.randint(-self.intensity, self.intensity)
            return dx, dy
        return 0, 0


class UI:
    def __init__(self):
        # Khởi tạo font hệ thống (Consolas rất hợp với phong cách Cyberpunk)
        pygame.font.init()
        self.title_font = pygame.font.SysFont("consolas", 48, bold=True)
        self.hud_font = pygame.font.SysFont("consolas", 18, bold=True)
        self.prompt_font = pygame.font.SysFont("consolas", 20)
        self.small_font = pygame.font.SysFont("consolas", 14)

    def draw_bar(self, surface, x, y, width, height, val, max_val, color_bar, label):
        """Vẽ thanh chỉ số (Máu, Khiên) phong cách Neon mảnh"""
        # Thể hiện phần trăm còn lại
        ratio = max(0.0, min(1.0, val / max_val))
        
        # Vẽ viền ngoài phát sáng nhẹ
        pygame.draw.rect(surface, (40, 40, 60), (x, y, width, height), 1)
        
        # Vẽ thanh đầy bên trong
        fill_width = int((width - 4) * ratio)
        if fill_width > 0:
            # Lớp nền thanh màu tối
            pygame.draw.rect(surface, (20, 20, 30), (x + 2, y + 2, width - 4, height - 4))
            # Lớp chính phát sáng màu Neon
            pygame.draw.rect(surface, color_bar, (x + 2, y + 2, fill_width, height - 4))
            
            # Tạo quầng sáng dọc theo thanh (nếu không ở chế độ máy yếu)
            if not config.LOW_SPEC_MODE:
                glow_surf = pygame.Surface((fill_width + 10, height + 6), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*color_bar, 60), (5, 3, fill_width, height - 4), border_radius=2)
                surface.blit(glow_surf, (x - 3, y - 3), special_flags=pygame.BLEND_RGB_ADD)
                
        # Hiển thị nhãn text
        text_surf = self.hud_font.render(f"{label}: {int(val)}/{int(max_val)}", True, config.COLOR_WHITE)
        surface.blit(text_surf, (x + 5, y - 18))

    def draw_hud(self, surface, player, score):
        # 1. Vẽ thanh máu (Green)
        self.draw_bar(surface, 20, 30, 220, 14, player.health, player.max_health, config.COLOR_GREEN, "HP")
        
        # 2. Vẽ thanh khiên (Cyan)
        self.draw_bar(surface, 20, 75, 220, 14, player.shield, player.max_shield, config.COLOR_CYAN, "SHIELD")
        
        # 3. Vẽ điểm số (Yellow) phát sáng góc phải
        score_str = f"SCORE: {score:06d}"
        score_surf = self.title_font.render(score_str, True, config.COLOR_YELLOW)
        score_rect = score_surf.get_rect(topright=(config.SCREEN_WIDTH - 20, 15))
        
        # Vẽ glow cho chữ điểm số
        if not config.LOW_SPEC_MODE:
            glow_surf = pygame.font.SysFont("consolas", 48, bold=True).render(score_str, True, (150, 140, 0))
            surface.blit(glow_surf, (score_rect.x - 2, score_rect.y - 2), special_flags=pygame.BLEND_RGB_ADD)
            
        surface.blit(score_surf, score_rect)
        
        # 4. Hiển thị cấp độ vũ khí
        weapon_surf = self.hud_font.render(f"WEAPON LVL: {player.weapon_level}", True, config.COLOR_CYAN)
        surface.blit(weapon_surf, (20, 105))
        
        # 5. Hiển thị thông tin nút bấm hướng dẫn nhỏ ở góc dưới trái
        spec_status = "LOW-SPEC: ON (Nổ nhẹ, ít hạt)" if config.LOW_SPEC_MODE else "LOW-SPEC: OFF (Mượt & RTX Glow)"
        spec_surf = self.small_font.render(f"F1: Đổi cấu hình | {spec_status}", True, (100, 100, 150))
        surface.blit(spec_surf, (20, config.SCREEN_HEIGHT - 30))

    def draw_boss_bar(self, surface, boss):
        """Hiển thị thanh máu khổng lồ của Boss ở trên cùng màn hình"""
        x = config.SCREEN_WIDTH // 2 - 250
        y = 40
        width = 500
        height = 16
        
        self.draw_bar(surface, x, y, width, height, boss.health, boss.max_health, config.COLOR_RED, "BOSS CORE")

    def draw_menu(self, surface):
        """Vẽ màn hình chờ khởi động game"""
        # Làm tối màn hình
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.fill((5, 5, 10))
        surface.blit(overlay, (0, 0))
        
        # Vẽ các khối ô lưới Cyberpunk nền mờ
        grid_size = 60
        for i in range(0, config.SCREEN_WIDTH, grid_size):
            pygame.draw.line(surface, (15, 15, 30), (i, 0), (i, config.SCREEN_HEIGHT))
        for j in range(0, config.SCREEN_HEIGHT, grid_size):
            pygame.draw.line(surface, (15, 15, 30), (0, j), (config.SCREEN_WIDTH, j))
            
        # Vẽ Tiêu đề phát sáng Neon
        title_str = "NEON CYBER-FORCE"
        title_surf = self.title_font.render(title_str, True, config.COLOR_CYAN)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3 - 30))
        
        # Glow tiêu đề
        title_glow = self.title_font.render(title_str, True, (0, 180, 200))
        surface.blit(title_glow, (title_rect.x - 4, title_rect.y - 4), special_flags=pygame.BLEND_RGB_ADD)
        surface.blit(title_surf, title_rect)
        
        # Hướng dẫn nút chơi
        prompt_surf = self.prompt_font.render("ẤN ENTER ĐỂ BẮT ĐẦU CHIẾN ĐẤU", True, config.COLOR_WHITE)
        prompt_rect = prompt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 30))
        surface.blit(prompt_surf, prompt_rect)
        
        # Hướng dẫn cách chơi
        inst_lines = [
            "Cách chơi:",
            " - Phím W, A, S, D hoặc Mũi tên: Di chuyển phi thuyền",
            " - Phím SPACE (Dấu cách): Bắn đạn laser",
            " - Phím F1: Bật / Tắt chế độ máy yếu (Low-Spec Mode)"
        ]
        
        start_y = config.SCREEN_HEIGHT // 2 + 100
        for line in inst_lines:
            line_surf = self.hud_font.render(line, True, (150, 150, 200))
            line_rect = line_surf.get_rect(center=(config.SCREEN_WIDTH // 2, start_y))
            surface.blit(line_surf, line_rect)
            start_y += 30

    def draw_game_over(self, surface, final_score):
        """Vẽ màn hình kết thúc game"""
        # Phủ bóng tối mờ đè lên game
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 0, 10, 180)) # Có độ trong suốt nhẹ
        surface.blit(overlay, (0, 0))
        
        # Chữ GAME OVER phát đỏ rực
        go_str = "DỰ ÁN ANH KEM BỊ TIÊU DIỆT"
        go_surf = self.title_font.render(go_str, True, config.COLOR_RED)
        go_rect = go_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3 - 30))
        
        go_glow = self.title_font.render(go_str, True, (200, 0, 0))
        surface.blit(go_glow, (go_rect.x - 4, go_rect.y - 4), special_flags=pygame.BLEND_RGB_ADD)
        surface.blit(go_surf, go_rect)
        
        # Điểm số cuối cùng
        score_str = f"TỔNG ĐIỂM ĐẠT ĐƯỢC: {final_score}"
        score_surf = self.prompt_font.render(score_str, True, config.COLOR_YELLOW)
        score_rect = score_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        surface.blit(score_surf, score_rect)
        
        # Khuyên khích chơi lại
        retry_surf = self.prompt_font.render("ẤN ENTER ĐỂ TÁI SINH TRẬN ĐẤU MỚI", True, config.COLOR_WHITE)
        retry_rect = retry_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 80))
        surface.blit(retry_surf, retry_rect)
