1. Chuyển cảnh cơ bản: Dùng `FadeIn` và `FadeOut` (có thể tuỳ chỉnh kèm phương hướng `shift`).
2. Điểm nhấn: Dùng hiệu ứng `Indicate(mob)`.
3. Khoanh vùng, cảnh báo: Dùng `ApplyMethod(mob.set_color)` kết hợp `SurroundingRectangle`.
4. Tạo hình đồ thị/đường dẫn: Dùng `ShowCreation()` để vẽ ra từ từ.
5. Biến đổi hình thái: Dùng `ReplacementTransform(old, new)` khi thực sự cần đổi form vật chất.
6. Gạch bỏ/Xóa dữ liệu: Dùng `Cross(mob)`.
7. Hiệu ứng gõ Text: Dùng `Write()`.
8. Biến đổi công thức: Dùng `TransformMatchingTex()`.
9. Tập trung con trỏ/Máy quay: Dùng `self.camera.frame.animate.move_to(...)` để di chuyển góc nhìn.
10. Run time: 
   - Xuất hiện tĩnh cơ bản: `0.5s`.
   - Chuyển tiếp nhanh: `0.2s` đến `0.3s`.
   - Luồng animation dữ liệu chậm rãi: `1.0s` đến `1.5s`. Đồng bộ bằng `ValueTracker`.
