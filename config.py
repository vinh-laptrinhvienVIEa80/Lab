# config.py
# Cấu hình và hằng số toàn cục cho game Neon Cyberpunk Space Shooter

import pygame

# Thiết lập cửa sổ game
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Chế độ máy cấu hình yếu (Low-Spec Mode)
# Nếu đặt thành True, game sẽ:
# 1. Giảm số lượng hạt tối đa (Particle cap)
# 2. Đơn giản hóa cơ chế tạo bóng sáng (Glow) động
# 3. Loại bỏ một số hiệu ứng nền phức tạp
LOW_SPEC_MODE = False

# Bảng màu Neon phong cách Cyberpunk (RGB)
COLOR_BG = (10, 10, 18)           # Màu nền tối sâu thẳm
COLOR_GRID = (25, 25, 45)         # Màu lưới nền
COLOR_CYAN = (0, 255, 240)        # Neon Cyan (Người chơi, Khiên, Đạn người chơi)
COLOR_MAGENTA = (255, 0, 180)     # Neon Magenta (Đạn địch, Boss)
COLOR_YELLOW = (255, 240, 0)      # Neon Yellow (Vật phẩm nâng cấp, Điểm số)
COLOR_GREEN = (50, 255, 50)       # Neon Green (Hồi máu, Hạt năng lượng)
COLOR_RED = (255, 50, 50)         # Neon Red (Tàu địch tự sát, Cảnh báo)
COLOR_WHITE = (255, 255, 255)     # Trắng (Tâm sáng rực)

# Cấu hình hạt (Particles)
PARTICLE_LIMIT_NORMAL = 500
PARTICLE_LIMIT_LOW = 150

# Hàm tiện ích tạo quầng sáng (Glow Surface) được vẽ sẵn (Pre-rendered)
# Đây là chìa khóa giúp game chạy siêu mượt trên cả máy yếu!
_glow_cache = {}

def get_glow_surf(color, radius, glow_intensity=3):
    """
    Tạo hoặc lấy từ cache một Surface hình tròn phát sáng (glow) 
    dùng blending cộng màu (blend_rgb_add).
    """
    key = (color, radius, glow_intensity)
    if key in _glow_cache:
        return _glow_cache[key]
    
    # Tạo Surface hỗ trợ kênh Alpha
    size = radius * 2
    glow_surf = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
    
    # Vẽ các lớp đồng tâm mờ dần từ trong ra ngoài
    # Với máy cấu hình yếu, giảm số lớp vẽ để tối ưu hóa bộ nhớ
    step = 3 if LOW_SPEC_MODE else 1
    
    for r in range(radius, 0, -step):
        # Alpha giảm dần khi bán kính tăng lên
        alpha_ratio = 1.0 - (r / radius)
        alpha = int((1.0 - alpha_ratio ** 2) * 80)  # Tạo độ mờ dịu
        
        # Vẽ vòng tròn mờ chồng lên
        pygame.draw.circle(glow_surf, (*color, alpha), (radius, radius), r)
        
    # Vẽ tâm sáng màu trắng để tạo hiệu ứng phát quang mạnh
    pygame.draw.circle(glow_surf, COLOR_WHITE, (radius, radius), max(2, int(radius * 0.2)))
    
    _glow_cache[key] = glow_surf
    return glow_surf
