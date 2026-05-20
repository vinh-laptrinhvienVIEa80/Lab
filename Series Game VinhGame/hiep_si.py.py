import random

hp = 100
vang = 0

print("⚔️ GAME HIỆP SĨ PHIÊU LƯU ⚔️")
print("Bạn là một hiệp sĩ đi tìm kho báu trong khu rừng.\n")

while True:
    print("\nBạn đang ở trong rừng.")
    print("1. Đi tiếp")
    print("2. Nghỉ ngơi")
    print("3. Thoát game")

    chon = input("Bạn chọn gì? ")

    if chon == "1":
        su_kien = random.randint(1, 3)

        if su_kien == 1:
            print("🐺 Bạn gặp một con sói!")
            print("1. Đánh nhau")
            print("2. Bỏ chạy")

            hanh_dong = input("Chọn: ")

            if hanh_dong == "1":
                mat_mau = random.randint(10, 30)
                hp -= mat_mau
                vang += 20
                print("Bạn thắng! Nhưng mất", mat_mau, "máu.")
                print("Bạn nhặt được 20 vàng.")
            else:
                print("Bạn chạy thoát an toàn.")

        elif su_kien == 2:
            tim_duoc_vang = random.randint(10, 50)
            vang += tim_duoc_vang
            print("💰 Bạn nhặt được", tim_duoc_vang, "vàng!")

        else:
            print("Không có chuyện gì xảy ra. Bạn tiếp tục đi.")

    elif chon == "2":
        hoi = random.randint(10, 30)
        hp += hoi
        if hp > 100:
            hp = 100
        print("😴 Bạn nghỉ ngơi và hồi", hoi, "máu.")

    elif chon == "3":
        print("Tạm biệt hiệp sĩ!")
        break

    else:
        print("Lựa chọn không hợp lệ!")

    print("❤️ Máu:", hp, "| 💰 Vàng:", vang)

    if hp <= 0:
        print("💀 Bạn đã kiệt sức và gục ngã trong rừng...")
        break
