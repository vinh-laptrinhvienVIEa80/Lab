import random

diem = 0
van = 1

print("🎯 GAME BẮN SỐ MAY MẮN (VinhGame.Inc)")
print("Đoán số từ 1 đến 10. Trúng là ghi điểm!\n")

while True:
    print("====== VÁN", van, "======")
    so_bi_mat = random.randint(1, 10)

    doan = input("Bắn số (1-10) hoặc gõ 'thoat' để dừng: ")

    if doan.lower() == "thoat":
        break

    if not doan.isdigit():
        print("❌ Phải nhập số!")
        continue

    doan = int(doan)

    if doan < 1 or doan > 10:
        print("❌ Số phải từ 1 đến 10!")
        continue

    print("🎯 Số bí mật là:", so_bi_mat)

    if doan == so_bi_mat:
        print("🎉 TRÚNG ĐÍCH! +1 điểm")
        diem += 1
    else:
        print("😢 Trật rồi!")

    print("⭐ Điểm:", diem)
    print("-" * 30)

    van += 1

print("\n🏁 Kết thúc game!")
print("Tổng điểm của bạn:", diem)
print("Cảm ơn bạn đã chơi Game Bắn Số May Mắn – VinhGame.Inc!")
