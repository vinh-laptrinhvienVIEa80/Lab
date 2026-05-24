#include <iostream>
#include <cmath>
#include <conio.h> // Thư viện chứa hàm getch() để giữ màn hình

using namespace std;

// [Giữ nguyên từ v1.0] Hàm kiểm tra số nguyên tố
bool checkPrime(long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

// [Giữ nguyên từ v1.0] Hàm tìm Ước chung lớn nhất
long long findGCD(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

// [Giữ nguyên từ v1.0] Hàm giải bài toán Gà và Chó
void solveChickenAndDog(int totalAnimals, int totalLegs) {
    int dogs = (totalLegs - totalAnimals * 2) / 2;
    int chickens = totalAnimals - dogs;
    
    if (dogs >= 0 && chickens >= 0 && (chickens * 2 + dogs * 4 == totalLegs)) {
        cout << "=> So Ga la: " << chickens << " con.\n";
        cout << "=> So Cho la: " << dogs << " con.\n";
    } else {
        cout << "=> Khong co dap an hop le cho so lieu nay!\n";
    }
}

int main() {
    cout << "====================================\n";
    cout << "      VINH MATH TOOLBOX V1.1        \n";
    cout << "  (Phien ban: Nhap du lieu tu ban phim) \n";
    cout << "====================================\n\n";

    // --- CẬP NHẬT TRÊN V1.1: TƯƠNG TÁC NGƯỜI DÙNG ---

    // 1. Nhập và kiểm tra Số nguyên tố
    long long checkNum;
    cout << "[1] KIEM TRA SO NGUYEN TO\n";
    cout << "Nhap vao so can kiem tra: ";
    cin >> checkNum; // Nhận số từ bàn phím
    if (checkPrime(checkNum)) {
        cout << "=> " << checkNum << " la SO NGUYEN TO.\n\n";
    } else {
        cout << "=> " << checkNum << " KHONG PHAI so nguyên to.\n\n";
    }

    cout << "------------------------------------\n";

    // 2. Nhập và tìm Ước chung lớn nhất
    long long num1, num2;
    cout << "[2] TIM UOC CHUNG LON NHAT\n";
    cout << "Nhap so thu nhat: ";
    cin >> num1;
    cout << "Nhap so thu hai: ";
    cin >> num2;
    cout << "=> UCLN cua " << num1 << " va " << num2 << " la: " << findGCD(num1, num2) << "\n\n";

    cout << "------------------------------------\n";

    // 3. Nhập và giải bài toán Gà - Chó
    int animals, legs;
    cout << "[3] GIAI BAI TOAN GA VA CHO\n";
    cout << "Nhap tong so CON: ";
    cin >> animals;
    cout << "Nhap tong so CHAN: ";
    cin >> legs;
    solveChickenAndDog(animals, legs);

    cout << "\n====================================\n";
    cout << "Bam mot phim bat ky de thoat chuong trinh...";
    
    getch(); // Giữ màn hình đứng im trên Windows
    return 0;
}