import random

diem_nguoi = 0
diem_may = 0
van = 1

print("🎲 GAME XÚC XẮC MAY MẮN (VinhGame.Inc)")
print("Mỗi ván bạn và máy sẽ đổ xúc xắc.")
print("Ai có số lớn hơn sẽ thắng!\n")

while True:
    print("====== VÁN", van, "======")
    input("Nhấn Enter để đổ xúc xắc...")

    nguoi = random.randint(1, 6)
    may = random.randint(1, 6)

    print("🎯 Bạn đổ được:", nguoi)
    print("🤖 Máy đổ được:", may)

    if nguoi > may:
        print("🎉 Bạn thắng ván này!")
        diem_nguoi += 1
    elif nguoi < may:
        print("😢 Máy thắng ván này!")
        diem_may += 1
    else:
        print("⚖️ Hòa!")

    print("📊 Điểm - Bạn:", diem_nguoi, "| Máy:", diem_may)
    print("-" * 30)

    tiep = input("Chơi tiếp không? (y/n): ").lower()
    if tiep != "y":
        break

    van += 1

print("\n🏁 Kết thúc game!")
print("Tổng điểm - Bạn:", diem_nguoi)
print("Tổng điểm - Máy:", diem_may)
print("Cảm ơn bạn đã chơi Game Xúc Xắc May Mắn!")
