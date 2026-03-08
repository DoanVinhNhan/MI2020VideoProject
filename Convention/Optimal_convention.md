1. Tiết kiệm tài nguyên vòng lặp: Dùng `FadeIn`, `FadeOut`, hoặc cập nhật thuộc tính Mobject tĩnh thay cho `Transform` liên tục.
2. Vẽ đồ thị động (Dynamic plots): Dùng `set_points_as_corners` cập nhật mảng tọa độ, cấm khởi tạo `get_graph` lặp lại.
3. Tối ưu sinh Text: Bắt buộc dùng Text Caching tĩnh (dictionary) cho text lặp lại số lượng lớn.
4. Xử lý dữ liệu lớn (Backend Loaders): Tính toán nặng phải C++ (compile file .so/.dylib/.dll), gọi qua `ctypes`. Cấm dùng vòng lặp Python.
5. Giải phóng bộ nhớ: Phải gọi lệnh `free()` qua `ctypes` sau khi lấy xong dữ liệu từ mảng C++ Pointer.
6. Xóa bỏ rác hiển thị: Dùng `self.remove(mob)` khi object đã out of màn hình để giảm số lượng Mobject được render.
7. Nhóm đối tượng: Gom nhóm mobject vào `VGroup` để xử lý di chuyển một khối chung thay vì loop từng mobject.
8. Animation Update: Dùng hàm `add_updater` cho các logic chạy ngầm độc lập với timeline chính.
