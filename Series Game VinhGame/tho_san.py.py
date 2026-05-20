import random

hp = 100
vang = 0
cap = 1

print("⚔ GAME THỢ SĂN QUÁI VẬT (VinhGame.Inc)")
print("Bạn là một thợ săn chuyên nghiệp!\n")

while True:
    print("\n===== THỢ SĂN CẤP", cap, "=====")
    print("❤️ Máu:", hp, "| 💰 Vàng:", vang)
    print("1. Nhận nhiệm vụ săn quái")
    print("2. Nghỉ ngơi hồi máu")
    print("3. Thoát game")

    chon = input("Chọn hành động: ")

    if chon == "1":
        quai = random.choice(["🐲 Rồng", "👹 Quỷ", "🦂 Bọ khổng lồ", "🐺 Sói đột biến"])
        suc_manh = random.randint(15, 30)

        print("\nBạn gặp", quai)
        mat_mau = random.randint(10, suc_manh)
        hp -= mat_mau

        if hp > 0:
            thuong = random.randint(30, 60)
            vang += thuong
            cap += 1
            print("Bạn đã tiêu diệt", quai)
            print("Bạn mất", mat_mau, "máu nhưng nhận", thuong, "vàng!")
            print("🎉 LÊN CẤP! Cấp hiện tại:", cap)
        else:
            print("💀 Bạn đã bị", quai, "đánh bại...")

    elif chon == "2":
        hoi = random.randint(20, 40)
        hp += hoi
        if hp > 100:
            hp = 100
        print("😴 Bạn nghỉ ngơi và hồi", hoi, "máu.")

    elif chon == "3":
        print("Tạm biệt thợ săn!")
        break

    else:
        print("Lựa chọn không hợp lệ!")

    if hp <= 0:
        print("\n💀 Thợ săn đã gục ngã...")
        break
