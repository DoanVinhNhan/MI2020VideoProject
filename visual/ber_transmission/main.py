import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manimlib import *
from object.background import Background
from object.broadcasting import Broadcasting
from object.receiving import Receiving
from object.bit import BitSequence

import subprocess
import ctypes
import sys

class TestTransmission(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Thiết lập tốc độ di chuyển và số lượng frame gửi
        run_time_speed = 1.6 # Thời gian bit chạy (giây). Giảm xuống để đi nhanh hơn.
        num_packets = 100      # Số gói 8-bit liên tục gửi
        error_prob = 0.15    # Tỷ lệ nhiễu truyền kênh (15%)
        
        # 1. Background
        bg = Background()
        self.add(bg)
        

        title = Text("BER Transmission", font_size=48, weight=BOLD).to_edge(UP, buff=1)
        self.add(title)

        
        # 2. Broadcasting and Receiving
        broadcasting = Broadcasting().to_edge(LEFT, buff=1)
        receiving = Receiving().to_edge(RIGHT, buff=1)
        
        self.play(FadeIn(broadcasting), FadeIn(receiving))
        
        # Lấy đường dẫn file exe C++
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
        exe_path = os.path.join(backend_dir, "generate_packet")
        
        # 3. Sinh ra chuỗi bit tổng dài 1 triệu
        total_bits = 1000000
        run_cmd = [exe_path, str(total_bits), str(error_prob)]
        result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split("\n")
        
        full_orig_bits_str = output_lines[0]
        full_recv_bits_str = output_lines[1]
        
        # Load C++ thư viện để tính BER
        lib_ext = ".dylib" if sys.platform == "darwin" else ".so"
        lib_path = os.path.join(backend_dir, f"libsimulate{lib_ext}")
        ber_lib = ctypes.CDLL(lib_path)
        ber_lib.calculate_ber_array_from_str.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        ber_lib.calculate_ber_array_from_str.restype = ctypes.POINTER(ctypes.c_double)
        ber_lib.free_ber_array.argtypes = [ctypes.POINTER(ctypes.c_double)]
        ber_lib.free_ber_array.restype = None
        
        # Tính toán trước danh sách lỗi để hiển thị dưới dạng phân số "lỗi/tổng" bằng C++
        out_array_size = ctypes.c_int(0)
        c_orig_bits = full_orig_bits_str.encode('utf-8')
        c_recv_bits = full_recv_bits_str.encode('utf-8')
        total_length = len(full_orig_bits_str)
        interval = 8
        
        ber_array_ptr = ber_lib.calculate_ber_array_from_str(c_orig_bits, c_recv_bits, total_length, interval, ctypes.byref(out_array_size))
        
        # Chuyển đổi dữ liệu từ C++ mảng sang Python list
        num_elements = out_array_size.value
        precomputed_ber_values = [ber_array_ptr[i] for i in range(num_elements)]
        
        # Giải phóng bộ nhớ mảng từ C++
        ber_lib.free_ber_array(ber_array_ptr)

        # 4. Vòng lặp gửi gói tin (Streaming)
        current_ber_text = None
        for i in range(num_packets):
            
            speed_factor = 20 if i >= 5 else 1
            real_run_time_speed = run_time_speed / speed_factor
            real_fade_in_time = 0.2 / speed_factor
            
            # Lấy 8 bit cho mỗi lần gửi
            start_idx = i * 8
            end_idx = start_idx + 8
            orig_bits_str = full_orig_bits_str[start_idx:end_idx]
            recv_bits_str = full_recv_bits_str[start_idx:end_idx]
            
            # Cập nhật màn hình text "Sent" bên broadcasting
            broadcasting.update_sequence(self, orig_bits_str, run_time=real_fade_in_time)
            
            # Khởi tạo gói bit sẽ di chuyển trên màn hình
            moving_bits = BitSequence(sequence=orig_bits_str, color="#00FF00")
            moving_bits.next_to(broadcasting.icon, RIGHT)
            
            self.play(FadeIn(moving_bits), run_time=real_fade_in_time)
            
            # Hiệu ứng bit bay sang phải kênh truyền (Gọi hàm đóng gói trong BitSequence)
            moving_bits.stream_to(self, receiving.icon, real_run_time_speed)
            

            # Cập nhật màn hình "Received" bên receiving
            receiving.update_sequence(self, orig_bits_str, recv_bits_str, moving_bits, run_time=real_fade_in_time)

            if i == 0:
                equation = Tex(r"BEP \approx \lim_{N\to \infty} BER = \lim_{N\to \infty} \frac{E}{N}", font_size = 32).to_edge(DOWN, buff=1.9)
                self.play(FadeIn(equation))
                curr_equation = equation

            # Lấy Text hiển thị BER đã tính trước từ C++ array
            ber_value = precomputed_ber_values[i]
            ber = Text(f"BER = {ber_value:.4f}", font_size=24, weight=BOLD).to_edge(DOWN, buff=0.7).set_color(WHITE)
            
            if i == 0:
                self.play(FadeIn(ber))
            if current_ber_text:
                self.remove(current_ber_text)
            self.add(ber)
            current_ber_text = ber
            
            # Đứng chờ một nhịp nhỏ trước gói tiếp theo (cũng chia cho speed_factor)
            self.wait(0.2 / speed_factor)
            
        # Kết thúc dọn dẹp
        self.wait(1)
        
        fade_out_group = [FadeOut(broadcasting), FadeOut(receiving)]
        if broadcasting.current_seq_display:
            fade_out_group.append(FadeOut(broadcasting.current_seq_display))
        if broadcasting.prev_seq_display:
            fade_out_group.append(FadeOut(broadcasting.prev_seq_display))
        if receiving.current_seq_display:
            fade_out_group.append(FadeOut(receiving.current_seq_display))
        if current_ber_text:
            fade_out_group.append(FadeOut(current_ber_text))
        if curr_equation:
            fade_out_group.append(FadeOut(curr_equation))
            
        self.play(*fade_out_group)
        self.wait(1)
