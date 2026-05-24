#include <iostream>
#include <vector>
#include <algorithm> // Chứa hàm std::sort siêu nhanh
#include <chrono>    // Dùng để đo thời gian chạy chính xác từng mili-giây
#include <random>    // Bộ tạo số ngẫu nhiên chất lượng cao

using namespace std;
using namespace std::chrono;

int main() {
    // 1. Khởi tạo mảng dữ liệu lớn gồm 1,000,000 (1 triệu) phần tử
    const int DATA_SIZE = 1000000;
    vector<int> data(DATA_SIZE);

    // Sử dụng thuật toán sinh số ngẫu nhiên Mersenne Twister để tạo dữ liệu giả lập
    mt19937 rng(1337); // Số 1337 là seed ngẫu nhiên cố định
    uniform_int_distribution<int> dist(1, 10000000); // Số ngẫu nhiên từ 1 đến 10 triệu

    for (int i = 0; i < DATA_SIZE; ++i) {
        data[i] = dist(rng);
    }

    cout << "Da khoi tao xong " << DATA_SIZE << " phan tu ngau nhien.\n";
    cout << "Dang bat dau sap xep...\n";

    // 2. Bắt đầu bấm đồng hồ đo thời gian
    auto start = high_resolution_clock::now();

    // 3. Thực hiện thuật toán sắp xếp nội bộ (IntroSort - kết hợp QuickSort, HeapSort và InsertionSort)
    // Đây là thuật toán sắp xếp nhanh nhất được tối ưu ở mức phần cứng của C++
    sort(data.begin(), data.end());

    // 4. Dừng đồng hồ
    auto stop = high_resolution_clock::now();

    // 5. Tính toán thời gian chạy
    auto duration = duration_cast<milliseconds>(stop - start);

    cout << "Sap xep hoan thanh!\n";
    cout << "Thoi gian chay: " << duration.count() << " mili-giay.\n";

    // Kiểm tra nhanh xem vài phần tử đầu tiên đã được xếp đúng chưa
    cout << "5 phan tu dau tien sau khi xep: ";
    for (int i = 0; i < 5; ++i) {
        cout << data[i] << " ";
    }
    cout << "\n";

    return 0;
}