#include <iostream>
#include <cmath>
#include <conio.h> // Thư viện chứa hàm getch() để giữ màn hình

using namespace std;

// 1. Hàm kiểm tra số nguyên tố (Tối ưu bằng cách chỉ kiểm tra đến căn bậc hai)
bool checkPrime(long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    // Vòng lặp nhảy bước 6 giúp kiểm tra siêu nhanh cho các số lớn
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

// 2. Hàm tìm Ước chung lớn nhất (Sử dụng thuật toán Euclid trừ/chia lấy dư cực nhanh)
long long findGCD(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

// 3. Hàm giải bài toán Gà và Chó (Bài toán cổ tìm số chân)
// Tổng số con là totalAnimals, tổng số chân là totalLegs
void solveChickenAndDog(int totalAnimals, int totalLegs) {
    // Công thức giả thiết tạm: Giả sử tất cả là gà (2 chân)
    // Số chó = (Tổng số chân - Tổng số con * 2) / 2
    int dogs = (totalLegs - totalAnimals * 2) / 2;
    int chickens = totalAnimals - dogs;
    
    // Kiểm tra xem số liệu có hợp lý không
    if (dogs >= 0 && chickens >= 0 && (chickens * 2 + dogs * 4 == totalLegs)) {
        cout << "-> So Ga la: " << chickens << " con.\n";
        cout << "-> So Cho la: " << dogs << " con.\n";
    } else {
        cout << "-> Khong co dap an hop le cho so lieu nay!\n";
    }
}

int main() {
    cout << "====================================\n";
    cout << "      VINH MATH TOOLBOX V1.0        \n";
    cout << "====================================\n\n";

    // --- KIỂM TRA TÍNH NĂNG 1: SỐ NGUYÊN TỐ ---
    long long checkNum = 99999999977; // Một số nguyên tố cực kỳ lớn
    cout << "[1] Kiem tra so nguyen to lon:\n";
    cout << "Dang kiem tra so: " << checkNum << "...\n";
    if (checkPrime(checkNum)) {
        cout << "-> Chinh xac! Day la so nguyen to.\n\n";
    } else {
        cout << "-> Khong phai so nguyen to.\n\n";
    }

    // --- KIỂM TRA TÍNH NĂNG 2: ƯỚC CHUNG LỚN NHẤT ---
    long long num1 = 123456, num2 = 7890;
    cout << "[2] Tim Uoc chung lon nhat cua " << num1 << " va " << num2 << ":\n";
    cout << "-> UCLN la: " << findGCD(num1, num2) << "\n\n";

    // --- KIỂM TRA TÍNH NĂNG 3: GIẢI TOÁN CỔ ---
    int animals = 36, legs = 100; // Bài toán gốc: 36 con, 100 chân vừa đi vừa chạy
    cout << "[3] Giai bai toan co: 36 con, 100 chan:\n";
    solveChickenAndDog(animals, legs);

    cout << "\n====================================\n";
    cout << "Bam mot phim bat ky de thoat chuong trinh...";
    
    getch(); // Giữ màn hình đứng im cho cậu xem kết quả trên Windows
    return 0;
}