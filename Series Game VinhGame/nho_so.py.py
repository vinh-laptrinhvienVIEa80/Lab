import random
import time
import os

print("🧠 GAME NHỚ SỐ (VinhGame.Inc)")
print("Hãy nhớ dãy số và nhập lại cho đúng!\n")

level = 1

while True:
    do_dai = level + 2
    day_so = ""

    for i in range(do_dai):
        day_so += str(random.randint(0, 9))

    print("Level", level)
    print("Ghi nhớ dãy số sau:")
    print(day_so)

    time.sleep(3)
    os.system("cls")  # xóa màn hình (Windows)

    tra_loi = input("Nhập lại dãy số: ")

    if tra_loi == day_so:
        print("✅ Chính xác! Lên level mới!")
        level += 1
    else:
        print("❌ Sai rồi!")
        print("Dãy đúng là:", day_so)
        break

    print("-" * 30)

print("\n🏁 Kết thúc game!")
print("Bạn đạt tới level:", level)
