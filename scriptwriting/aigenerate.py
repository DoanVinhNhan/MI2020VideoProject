import os
import json
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types

# Cấu hình API Key (sẽ lấy từ biến môi trường hoặc nhập cứng định sẵn)
if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("Vui lòng thiết lập biến môi trường GEMINI_API_KEY")

client = genai.Client()
MODEL_ID = 'gemini-3.1-pro-preview' # Fallback name in genai SDK, equivalent to 2.5/3.1 preview

# Tự định nghĩa mapping tên file tiếng Anh ngắn gọn cho các chủ đề
TOPIC_FILENAMES = [
    "bayes_spam_filter",            # 1
    "ber_transmission",             # 2
    "system_reliability",           # 3
    "decision_tree_investment",     # 4
    "exponential_server_response",  # 5
    "normal_dist_machining",        # 6
    "gaussian_noise_signal",        # 7
    "covariance_portfolio",         # 8
    "3d_emission_diffusion",        # 9
    "robot_positioning_error",      # 10
    "linear_regression_housing",    # 11
    "regression_sensor_calibration",# 12
    "confidence_interval_ab_test",  # 13
    "mtbf_estimation",              # 14
    "ttest_algorithm_speed",        # 15
    "qc_machine_deviation",         # 16
    "smart_elevator_queue",         # 17
    "bootstrap_resampling"          # 18
]

def read_file_content(filepath):
    """Đọc nội dung từ file text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_json_from_response(text):
    """Trích xuất mảng JSON từ phản hồi dạng text."""
    try:
        # Tìm đoạn bắt chéo qua []
        match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # Trả về text gốc nếu không match (hy vọng là JSON hợp lệ)
    except Exception:
        return text

def process_topic(topic, filename_base, prompt_template, sample_script, output_dir, max_retries=3):
    """
    Xử lý một chủ đề: Gọi API, parse JSON, và lưu ra file.
    """
    if not topic.strip():
        return
        
    print(f"[*] Bắt đầu xử lý chủ đề: {topic}")
    
    # 1. Thiết lập đường dẫn output
    output_path = os.path.join(output_dir, f"{filename_base}.json")
    
    # Nếu file đã tồn tại thì bỏ qua để tiết kiệm (hoặc có thể ghi đè tùy ý)
    if os.path.exists(output_path):
        print(f"[!] File đã tồn tại: {output_path}. Bỏ qua chủ đề này.")
        return
        
    # 2. Xây dựng prompt cuối cùng
    final_prompt = f"""{prompt_template}

--- CHỦ ĐỀ ĐƯỢC GIAO ---
{topic}

--- KỊCH BẢN MẪU ---
{sample_script}
"""

    # 3. Gọi API với cơ chế retry
    for attempt in range(1, max_retries + 1):
        try:
            print(f"   -> [Attempt {attempt}/{max_retries}] Gọi API cho: {filename_base}.json")
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                )
            )
            
            raw_text = response.text
            json_str = extract_json_from_response(raw_text)
            
            # Kiểm tra xem có parse được thành JSON không
            try:
                json_data = json.loads(json_str)
                # Ghi file thành công
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                print(f"[SUCCESS] Đã lưu kịch bản tại: {output_path}")
                break # Thành công thoát vòng lặp retry
            except json.JSONDecodeError as decode_err:
                 print(f"   -> [Lỗi JSON] API phản hồi không đúng chuẩn JSON ở lần thử {attempt}: {decode_err}")
                 if attempt == max_retries:
                     # Ghi log file lỗi để dễ debug
                    error_path = os.path.join(output_dir, f"{filename_base}_error.txt")
                    with open(error_path, 'w', encoding='utf-8') as f:
                        f.write(raw_text)
                    print(f"[FAILED] Quá số lần thử parse JSON. Đã lưu raw response vào: {error_path}")
                 time.sleep(2) # Đợi một lát trước khi retry
                 
        except Exception as api_err:
             print(f"   -> [Lỗi API] Lần thử {attempt} thất bại: {api_err}")
             if attempt == max_retries:
                 print(f"[FAILED] Quá số lần thử gọi API cho chủ đề: {topic[:30]}...")
             time.sleep(5) # Đợi lâu hơn nếu lỗi liên quan mạng/API


def main():
    # Thư mục đầu ra
    output_dir = "raw_script"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Đã tạo thư mục: {output_dir}")

    # Đọc dữ liệu đầu vào
    try:
         prompt_template = read_file_content("prompt.txt")
         sample_script = read_file_content("sample_script.txt")
         topics_text = read_file_content("topic.txt")
    except FileNotFoundError as e:
         print(f"Lỗi: Không tìm thấy file đầu vào. {e}")
         return

    # Tách danh sách chủ đề theo dòng (bỏ qua các dòng trống)
    # File topic.txt format: "1. Ứng dụng..."
    topics = []
    for line in topics_text.split('\n'):
        line = line.strip()
        if line:
            # Loại bỏ số thứ tự ở đầu (vd: "1. ", "12. ")
            clean_topic = re.sub(r'^\d+\.\s*', '', line)
            topics.append(clean_topic)

    print(f"Tiến hành sinh kịch bản cho {len(topics)} chủ đề...")
    
    # Số luồng đồng thời (tránh rate limit)
    MAX_WORKERS = 3

    # Chạy đa luồng
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
         # Gửi từng topic vào ThreadPool
         futures = []
         for i, topic in enumerate(topics):
             filename_base = TOPIC_FILENAMES[i] if i < len(TOPIC_FILENAMES) else f"topic_{i+1}"
             futures.append(executor.submit(process_topic, topic, filename_base, prompt_template, sample_script, output_dir))
         
         # Đợi tất cả hoàn thành
         for future in as_completed(futures):
             try:
                 future.result()
             except Exception as exc:
                 print(f"Có lỗi ngầm xả ra trong luồng: {exc}")

    print("\n[HOÀN TẤT] Quá trình sinh kịch bản đã kết thúc!")

if __name__ == "__main__":
    main()
