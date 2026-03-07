import subprocess
import os
import struct
import matplotlib.pyplot as plt

def run_simulation(N: int = 50000000000, target_prob: float = 1e-6):
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    cpp_source = os.path.join(backend_dir, "simulate.cpp")
    executable = os.path.join(backend_dir, "simulate")
    data_file = os.path.join(backend_dir, "bep_data.bin")
    
    # 1. Compile C++
    print("Compiling C++ backend...")
    compile_cmd = ["g++", "-O3", "-std=c++17", cpp_source, "-o", executable]
    subprocess.run(compile_cmd, check=True)
    
    # 2. Chạy thư viện C++ đã biên dịch
    print(f"Running simulation with N={N}, Error Probability={target_prob} ...")
    run_cmd = [executable, str(N), str(target_prob), data_file]
    result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
    
    total_errors = int(result.stdout.strip())
    print(f"Total Errors observed (from C++): {total_errors}")
    
    # 3. Đọc dữ liệu ra
    print("Reading data from binary payload...")
    y_vals = []
    
    # Đọc block nhị phân (chứa N phần tử C++ 'double', mỗi phần tử 8 bytes)
    with open(data_file, "rb") as f:
        # Tối ưu đọc với struct.unpack thay vì vòng lặp read(8)
        content = f.read()
        # Tính toán chính xác định dạng để parse nhanh list double.
        num_doubles = len(content) // 8
        y_vals = list(struct.unpack(f"{num_doubles}d", content))
        
    print(f"Final BER: {y_vals[-1]:.8f} (Target was {target_prob})")
        
    print("Pruning redundant data points to speed up plotting...")
    # BER = errors / N. Giữa 2 lần xuất hiện lỗi, số lỗi không đổi -> BER giảm theo hàm 1/x.
    # Trên đồ thị log-log, hàm 1/x là một đoạn thẳng do log(c/x) = log(c) - log(x).
    # Do đó, ta chỉ cần lưu các điểm ngay khi có lỗi mới (để tạo bước nhảy)
    # và điểm ngay trước khi có lỗi mới (để nối thẳng 1/x từ điểm lỗi trước đó).
    x_plot = [1]
    y_plot = [y_vals[0]]
    
    current_errors = round(y_vals[0] * 1)
    
    for i in range(1, len(y_vals)):
        x = i + 1
        y = y_vals[i]
        errors = round(y * x)
        if errors > current_errors:
            if x - 1 != x_plot[-1]:
                # Giữ nguyên decay 1/x đến ngay sát trước lúc nhảy vọt
                x_plot.append(x - 1)
                y_plot.append(y_vals[i - 1])
            # Thêm điểm bắt đầu tăng nhảy vọt
            x_plot.append(x)
            y_plot.append(y)
            current_errors = errors
            
    if x_plot[-1] != N:
        x_plot.append(N)
        y_plot.append(y_vals[-1])
            
    print(f"Reduced from {N} points to {len(x_plot)} points for plotting.")
    
    print("Plotting results...")
    plt.figure(figsize=(10, 6))
    
    # Trực quan hóa
    # Dùng plt.plot thay vì plt.step để nối thẳng các điểm trên trục đồ thị logarit (vẽ đúng đường 1/x).
    plt.plot(x_plot, y_plot, label='Cumulative Simulated BEP', color='blue', linewidth=1.5)
    plt.axhline(y=target_prob, color='red', linestyle='--', label=f'Theoretical BEP ({target_prob})')
    
    plt.title("Monte Carlo Simulation: Convergence of BEP (Law of Large Numbers)")
    plt.xlabel("Number of Transmitted Bits (N) - Log Scale")
    plt.ylabel("Bit Error Rate (BER) - Log Scale")
    plt.xscale('log') 
    plt.yscale('log') 
    
    plt.legend()
    
    # Lưu biểu đồ
    output_path = os.path.join(backend_dir, "bep_simulation_plot.png")
    plt.savefig(output_path, dpi=200)
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    # Chỉ gọi hàm chính
    run_simulation(N=50000000, target_prob=1e-6)
