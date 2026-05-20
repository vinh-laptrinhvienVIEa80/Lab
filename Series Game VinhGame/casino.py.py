import random

tien = 100  # tiền ban đầu

print("🎰 MINI CASINO CHỮ (VinhGame.Inc)")
print("Bạn bắt đầu với 100 tiền ảo.")
print("Đoán số từ 1 đến 6. Nếu trúng sẽ được x2 tiền cược!\n")

while tien > 0:
    print("💰 Tiền hiện có:", tien)

    cuoc = input("Nhập số tiền cược (hoặc 'thoat' để dừng): ")
    if cuoc.lower() == "thoat":
        break

    if not cuoc.isdigit():
        print("❌ Tiền cược phải là số!")
        continue

    cuoc = int(cuoc)

    if cuoc <= 0 or cuoc > tien:
        print("❌ Số tiền cược không hợp lệ!")
        continue

    doan = input("Đoán số (1-6): ")

    if doan not in ["1", "2", "3", "4", "5", "6"]:
        print("❌ Bạn phải chọn số từ 1 đến 6!")
        continue

    doan = int(doan)
    ket_qua = random.randint(1, 6)

    print("🎲 Máy quay ra số:", ket_qua)

    if doan == ket_qua:
        print("🎉 TRÚNG LỚN! Bạn thắng", cuoc * 2, "tiền!")
        tien += cuoc
    else:
        print("😢 Thua rồi! Bạn mất", cuoc, "tiền.")
        tien -= cuoc

    print("-" * 30)

print("\n🏁 Kết thúc Mini Casino!")
print("💰 Số tiền còn lại:", tien)
print("Cảm ơn bạn đã chơi Mini Casino Chữ – VinhGame.Inc!")
