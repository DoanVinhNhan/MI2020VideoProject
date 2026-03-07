#include <iostream>
#include <random>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char *argv[]) {
  // Mode: 1 argument N (độ dài) và 1 argument prob (tỷ lệ lỗi)
  long long N = 8;
  double target_prob = 0.1;

  if (argc >= 2) {
    N = stoll(argv[1]);
  }
  if (argc >= 3) {
    target_prob = stod(argv[2]);
  }

  // Khởi tạo random
  random_device rd;
  mt19937 rng(rd());
  uniform_int_distribution<int> bit_dist(0, 1);
  uniform_real_distribution<double> error_dist(0.0, 1.0);

  string original_str = "";
  string received_str = "";

  for (long long i = 0; i < N; ++i) {
    int bit = bit_dist(rng);
    original_str += to_string(bit);

    // Áp dụng nhiễu
    if (error_dist(rng) < target_prob) {
      received_str += to_string(!bit); // Bị lật bit
    } else {
      received_str += to_string(bit);
    }
  }

  // In ra đúng 2 dòng: dòng 1 là bit gốc gửi đi, dòng 2 là bit thu được
  cout << original_str << "\n" << received_str << "\n";

  return 0;
}
