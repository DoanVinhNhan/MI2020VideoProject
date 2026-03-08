import sys
import os

# Tuân thủ Agent Instruction: Cập nhật đường dẫn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manimlib import *
from object.background import Background
from object.logo import Logo

# Tuân thủ Video_format.md:
# 1. Định dạng 9:16 (Mobile/Shorts/Reels/TikTok)
# 2. Độ phân giải: 1080x1920
# 3. FPS: 60
# 4. Vùng an toàn: 15% trên/dưới (frame_height=14.22 -> safe margin = 2.13 units từ rìa)
#    Tức là object phải nằm trong khoảng y: [-4.98, 4.98]
config.frame_size = (1080, 1920)
config.frame_rate = 60

# Hằng số vùng an toàn
# frame_height ≈ 14.22 (= 8 * 16/9), safe_margin = 15% * 7.11 = 2.13
# => Giới hạn Y an toàn: top_safe = UP * (7.11 - 2.13) = UP * 4.98
SAFE_TOP    = UP    * 4.5   # buffer thêm để chắc chắn
SAFE_BOTTOM = DOWN  * 4.5


class OpenVideo(Scene):
    def construct(self):
        # 1. Tuân thủ Định dạng video: Đặt màu nền là BLACK
        self.camera.background_color = BLACK
        
        # 2. Tuân thủ Các object dùng chung: Tái sử dụng Background class
        bg = Background()
        self.add(bg)
        
        # 3. Logo mở đầu: Đặt vị trí chính giữa khi mở đầu (ORIGIN)
        logo = Logo().move_to(ORIGIN)
        # Chuyển cảnh tĩnh theo Danh sách hiệu ứng: run_time=0.5
        self.play(FadeIn(logo, shift=UP), run_time=0.5)
        self.wait(0.5)
        
        # Di chuyển logo lên trong vùng an toàn (SAFE_TOP)
        # Tuân thủ Video_format.md: tránh vùng 15% trên cùng (rìa tuyệt đối ≈ 7.11)
        # Logo được đặt tại SAFE_TOP để nằm trong vùng hiển thị hợp lệ
        self.play(
            logo.animate.scale(0.5).move_to(SAFE_TOP + LEFT * 3.0),
            run_time=0.5
        )
        
        # 4. Tiêu đề (Title)
        # Bảng màu & Phông chữ: Title là Chữ trắng (WHITE), nền xanh (BLUE), font_size=48, weight=BOLD
        # Tuân thủ Video_format.md: Tập trung object quan trọng ở ORIGIN -> title đặt hơi trên ORIGIN
        title_text = Text(
            "Đánh giá chất lượng\nHệ thống truyền tin", 
            font_size=48, 
            weight=BOLD, 
            color=WHITE,
            font="Sans-serif"
        )
        title_bg = BackgroundRectangle(title_text, color=BLUE, fill_opacity=1, buff=0.3)
        # Đặt title phía trên ORIGIN một chút, trong vùng an toàn
        title = VGroup(title_bg, title_text).move_to(UP * 2.5)
        
        self.play(FadeIn(title, shift=DOWN), run_time=0.5)
        self.wait(1)
        
        # 5. Câu hỏi mở từ script.txt: 
        # "Làm sao để ta có thể đánh giá được chất lượng và độ tin cậy của một hệ thống truyền tin?"
        question_text = Text(
            "Làm sao để ta có thể đánh giá được\nchất lượng và độ tin cậy\ncủa một hệ thống truyền tin?", 
            font_size=32, 
            color=WHITE,
            font="Sans-serif",
            alignment="CENTER"
        )
        # Câu hỏi đặt ở ORIGIN (hoặc dưới title), đây là object quan trọng nhất
        # Tuân thủ Video_format.md: tập trung object quan trọng ở ORIGIN
        question_text.move_to(ORIGIN + DOWN * 1.0)
        
        # Danh sách hiệu ứng: Sinh Text (hiệu ứng gõ Text) dùng Write()
        self.play(Write(question_text), run_time=1.0)
        self.wait(1)
        
        # Điểm nhấn danh sách hiệu ứng: Dùng ApplyMethod kết hợp SurroundingRectangle để khoanh vùng
        box = SurroundingRectangle(question_text, color=YELLOW, buff=0.2)
        self.play(ShowCreation(box), run_time=0.5)
        
        # Điểm nhấn danh sách hiệu ứng: Dùng Indicate(mob)
        self.play(Indicate(question_text), run_time=0.5)
        self.wait(2)
        
        # Chuyển cảnh cơ bản: FadeOut
        self.play(
            FadeOut(title),
            FadeOut(question_text),
            FadeOut(box),
            shift=DOWN,
            run_time=0.5
        )
        self.wait(0.5)
