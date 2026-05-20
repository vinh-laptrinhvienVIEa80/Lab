import random
import time

diem = 0
so_cau = 5

print("🧠 GAME TOÁN TỐC ĐỘ (VinhGame.Inc)")
print("Trả lời nhanh các phép toán sau!")
print("Có", so_cau, "câu hỏi.\n")

for i in range(1, so_cau + 1):
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    phep = random.choice(["+", "-", "*"])

    if phep == "+":
        dap_an = a + b
    elif phep == "-":
        dap_an = a - b
    else:
        dap_an = a * b

    print("Câu", i, ":", a, phep, b, "= ?")
    bat_dau = time.time()
    tra_loi = input("Đáp án: ")
    ket_thuc = time.time()

    thoi_gian = ket_thuc - bat_dau

    if tra_loi.isdigit() and int(tra_loi) == dap_an and thoi_gian <= 10:
        print("✅ Đúng! Thời gian:", round(thoi_gian, 2), "giây")
        diem += 1
    else:
        print("❌ Sai hoặc quá thời gian!")
        print("Đáp án đúng là:", dap_an)

    print("-" * 30)

print("\n🏁 Kết thúc game!")
print("🎯 Điểm của bạn:", diem, "/", so_cau)
