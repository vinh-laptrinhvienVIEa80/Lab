import random

hp = 100
vang = 0
level = 1

print("🏰 GAME DUNGEON PHIÊU LƯU (VinhGame.Inc)")
print("Bạn là chiến binh bước vào hầm ngục bí ẩn!\n")

while True:
    print("\n===== TẦNG DUNGEON", level, "=====")
    print("❤️ Máu:", hp, "| 💰 Vàng:", vang)
    print("1. Đi tiếp")
    print("2. Nghỉ ngơi")
    print("3. Thoát game")

    chon = input("Chọn hành động: ")

    if chon == "1":
        su_kien = random.randint(1, 3)

        if su_kien == 1:
            print("👹 Bạn gặp quái vật!")
            mat_mau = random.randint(10, 25)
            hp -= mat_mau
            vang += 30
            print("Bạn đánh bại quái vật nhưng mất", mat_mau, "máu.")
            print("Bạn nhận được 30 vàng!")

        elif su_kien == 2:
            tim_duoc = random.randint(20, 50)
            vang += tim_duoc
            print("💎 Bạn tìm thấy kho báu:", tim_duoc, "vàng!")

        else:
            print("Bạn đi qua một hành lang trống.")

        level += 1

    elif chon == "2":
        hoi = random.randint(15, 30)
        hp += hoi
        if hp > 100:
            hp = 100
        print("😴 Bạn nghỉ ngơi và hồi", hoi, "máu.")

    elif chon == "3":
        print("Tạm biệt chiến binh!")
        break

    else:
        print("Lựa chọn không hợp lệ!")

    if hp <= 0:
        print("\n💀 Bạn đã gục ngã trong hầm ngục...")
        break
