

import time
import random

print("⚡ GAME PHẢN XẠ (VinhGame.Inc)")
print("Khi thấy dòng 'NHẤN ENTER NGAY!' thì hãy nhấn Enter thật nhanh!")
print("Chuẩn bị nhé...\n")

input("Nhấn Enter để bắt đầu...")

cho = random.randint(2, 5)
print("Đang chờ tín hiệu...")
time.sleep(cho)

print("\n🔥 NHẤN ENTER NGAY !!! 🔥")
bat_dau = time.time()
input()
ket_thuc = time.time()

phan_xa = ket_thuc - bat_dau

print("\n⏱ Thời gian phản xạ của bạn:", round(phan_xa, 3), "giây")

if phan_xa < 0.3:
    print("🚀 Phản xạ siêu nhân!")
elif phan_xa < 0.6:
    print("😎 Phản xạ rất tốt!")
elif phan_xa < 1:
    print("🙂 Phản xạ ổn!")
else:
    print("😅 Cần luyện thêm nhé!")
