import random

hp = 100
thuc_an = 3
nuoc = 3
ngay = 1

print("🏝 GAME SINH TỒN HOANG ĐẢO (VinhGame.Inc)")
print("Bạn bị lạc trên một hòn đảo hoang!")
print("Hãy sinh tồn càng lâu càng tốt!\n")

while True:
    print("\n" + "="*30)
    print("📅 Ngày:", ngay)
    print("❤️ Máu:", hp, "| 🍖 Thức ăn:", thuc_an, "| 💧 Nước:", nuoc)
    print("="*30)
    print("1. Tìm thức ăn")
    print("2. Tìm nước")
    print("3. Nghỉ ngơi")
    print("4. Thoát game")

    chon = input("Chọn hành động: ")

    if chon == "1":
        if random.random() < 0.7:
            thuc_an += 1
            print("🍖 Bạn tìm được thức ăn!")
        else:
            hp -= 10
            print("😢 Không tìm được thức ăn, bạn mất 10 máu!")

    elif chon == "2":
        if random.random() < 0.7:
            nuoc += 1
            print("💧 Bạn tìm được nước!")
        else:
            hp -= 10
            print("😢 Không tìm được nước, bạn mất 10 máu!")

    elif chon == "3":
        if thuc_an > 0 and nuoc > 0:
            thuc_an -= 1
            nuoc -= 1
            hp += 20
            if hp > 100:
                hp = 100
            print("😴 Bạn nghỉ ngơi và hồi 20 máu.")
        else:
            print("❌ Không đủ thức ăn hoặc nước để nghỉ ngơi!")

    elif chon == "4":
        print("👋 Tạm biệt người sinh tồn!")
        break

    else:
        print("❌ Lựa chọn không hợp lệ!")

    ngay += 1

    if hp <= 0:
        print("\n💀 Bạn đã kiệt sức và gục ngã trên đảo...")
        print("⏳ Bạn đã sinh tồn được", ngay - 1, "ngày!")
        break
