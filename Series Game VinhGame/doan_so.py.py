import random

so_bi_mat = random.randint(1, 100)
so_lan_doan = 0

print("GAME ĐOÁN SỐ (VinhGame.Inc)")
print("Máy đã nghĩ ra 1 số từ 1 đến 100. Hãy đoán xem!")

while True:
    doan = int(input("Nhập số bạn đoán: "))
    so_lan_doan += 1

    if doan < so_bi_mat:
        print("Nhỏ quá!")
    elif doan > so_bi_mat:
        print("Lớn quá!")
    else:
        print("🎉 Chính xác!")
        print("Bạn đã đoán đúng sau", so_lan_doan, "lần.")
        break
