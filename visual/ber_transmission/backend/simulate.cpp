#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

// 1. Hàm giống với monte_carlo.py
// Sinh chuỗi N bit ngẫu nhiên
vector<bool> generate_bit_sequence(long long N, mt19937_64 &rng) {
  uniform_int_distribution<int> dist(0, 1);
  vector<bool> bits(N);
  for (long long i = 0; i < N; ++i) {
    bits[i] = dist(rng);
  }
  return bits;
}

// Cấu trúc trả về cho hàm nhiễu
struct NoiseResult {
  vector<bool> received_bits;
  long long total_errors;
};

// 2. Hàm giống với noise.py
// Lật bit với xác suất p
NoiseResult apply_noise(const vector<bool> &original_bits,
                        double error_probability, mt19937_64 &rng) {
  long long N = original_bits.size();
  vector<bool> received_bits(N);
  uniform_real_distribution<double> dist(0.0, 1.0);

  long long errors = 0;
  for (long long i = 0; i < N; ++i) {
    if (dist(rng) < error_probability) {
      received_bits[i] = !original_bits[i]; // Lật bit (XOR 1)
      errors++;
    } else {
      received_bits[i] = original_bits[i]; // Giữ nguyên (XOR 0)
    }
  }
  return {received_bits, errors};
}

// 3. Hàm giống với caculate_bep.py
// Tính BEP lũy kế
vector<double> calculate_cumulative_bep(const vector<bool> &original_bits,
                                        const vector<bool> &received_bits) {
  long long N = original_bits.size();
  if (N != (long long)received_bits.size()) {
    throw invalid_argument(
        "Size mismatch between original and received sequences");
  }

  vector<double> bep_data(N);
  long long error_count = 0;
  for (long long i = 0; i < N; ++i) {
    if (original_bits[i] != received_bits[i]) {
      error_count++;
    }
    bep_data[i] = (double)error_count / (i + 1);
  }
  return bep_data;
}

extern "C" {
double calculate_ber_from_str(const char *orig_str, const char *recv_str,
                              int length) {
  vector<bool> orig(length);
  vector<bool> recv(length);
  for (int i = 0; i < length; ++i) {
    orig[i] = (orig_str[i] == '1');
    recv[i] = (recv_str[i] == '1');
  }
  vector<double> bep_data = calculate_cumulative_bep(orig, recv);
  if (bep_data.empty())
    return 0.0;
  return bep_data.back();
}

double *calculate_ber_array_from_str(const char *orig_str, const char *recv_str,
                                     int total_length, int interval,
                                     int *out_array_size) {
  if (total_length <= 0 || interval <= 0) {
    *out_array_size = 0;
    return nullptr;
  }

  int size = total_length / interval;
  *out_array_size = size;

  double *result_array = new double[size];

  long long cumulative_errors = 0;
  for (int i = 0; i < size; ++i) {
    int start_idx = i * interval;
    int end_idx = start_idx + interval;

    long long chunk_errors = 0;
    for (int j = start_idx; j < end_idx; ++j) {
      if (orig_str[j] != recv_str[j]) {
        chunk_errors++;
      }
    }
    cumulative_errors += chunk_errors;

    result_array[i] = (double)cumulative_errors / end_idx;
  }

  return result_array;
}

void free_ber_array(double *arr) { delete[] arr; }
}

int main(int argc, char *argv[]) {
  // Cài đặt mặc định
  long long N = 50000000;
  double target_prob = 1e-6;
  string output_file = "bep_data.bin";

  // Phân tích tham số đầu vào
  if (argc >= 2) {
    N = stoll(argv[1]);
  }
  if (argc >= 3) {
    target_prob = stod(argv[2]);
  }
  if (argc >= 4) {
    output_file = argv[3];
  }

  mt19937_64 rng(1337);

  // Bước 1: Sinh chuỗi
  vector<bool> original = generate_bit_sequence(N, rng);

  // Bước 2: Kênh truyền thêm nhiễu
  NoiseResult noise_res = apply_noise(original, target_prob, rng);

  // Bước 3: Tính toán BEP lũy kế
  vector<double> bep_data =
      calculate_cumulative_bep(original, noise_res.received_bits);

  // Ghi lưu dữ liệu vào nhị phân
  ofstream outfile(output_file, ios::binary);
  if (!outfile) {
    cerr << "Error opening file for writing." << endl;
    return 1;
  }

  // Ghi toàn bộ mảng double vector ra file nhị phân trong 1 lần để tối ưu i/o
  outfile.write(reinterpret_cast<const char *>(bep_data.data()),
                N * sizeof(double));
  outfile.close();

  // In ra tổng số lỗi vào std::cout (cho python lấy data)
  cout << noise_res.total_errors << endl;

  return 0;
}
