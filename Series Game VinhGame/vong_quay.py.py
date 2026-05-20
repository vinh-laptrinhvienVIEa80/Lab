import random

diem = 0
tien = 0
luot = 0

print("🎡 GAME VÒNG QUAY THƯỞNG (VinhGame.Inc)")
print("Mỗi lượt quay sẽ nhận phần thưởng ngẫu nhiên!\n")

phan_thuong = [
    ("💰 +10 tiền", 10, 0),
    ("💰 +20 tiền", 20, 0),
    ("⭐ +1 điểm", 0, 1),
    ("⭐ +2 điểm", 0, 2),
    ("🎁 TRÚNG LỚN +50 tiền", 50, 0),
    ("😢 Không trúng gì", 0, 0)
]

while True:
    print("📊 Tiền:", tien, "| ⭐ Điểm:", diem)
    lua_chon = input("Nhấn Enter để quay (hoặc nhập 'thoat' để dừng): ")

    if lua_chon.lower() == "thoat":
        break

    ket_qua = random.choice(phan_thuong)
    print("\n🎯 Kết quả:", ket_qua[0])

    tien += ket_qua[1]
    diem += ket_qua[2]
    luot += 1

    print("Bạn đã quay", luot, "lượt")
    print("-" * 30)

print("\n🏁 Kết thúc game!")
print("Tổng lượt quay:", luot)
print("Tổng tiền:", tien)
print("Tổng điểm:", diem)
print("Cảm ơn bạn đã chơi Game Vòng Quay Thưởng!")
