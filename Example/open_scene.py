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
# 4. Vùng an toàn: 15% trên/dưới
#
# Hệ toạ độ ManimGL với 9:16:
#   frame_height = 8  (mặc định giữ nguyên)
#   frame_width  = 8 * (9/16) = 4.5
#   => X: [-2.25, +2.25]   Y: [-4.0, +4.0]
#   Safe zone 15%: X: [-1.9, +1.9]   Y: [-3.4, +3.4]
config.frame_size   = (1080, 1920)   # kích thước pixel
config.frame_height = 8              # chiều cao toạ độ (giữ mặc định)
config.frame_width  = 4.5            # chiều rộng toạ độ = 8 * (9/16)
config.frame_rate   = 60

# Hằng số vùng an toàn (15% cách rìa)
# Y: 4.0 * 0.85 = 3.4 | X: 2.25 * 0.85 = 1.91
SAFE_TOP    = UP    * 3.2
SAFE_BOTTOM = DOWN  * 3.2
SAFE_LEFT   = LEFT  * 1.8
SAFE_RIGHT  = RIGHT * 1.8


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
        
        # Di chuyển logo lên góc trên trong vùng an toàn
        # frame_width=4.5 => X max = 2.25  => dùng LEFT*1.5 để an toàn
        self.play(
            logo.animate.scale(0.4).move_to(SAFE_TOP + LEFT * 1.5),
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
        title_bg = BackgroundRectangle(title_text, color=BLUE, fill_opacity=1, buff=0.2)
        # Title ở phía trên ORIGIN, căn giữa (frame_height=8 => y in [-4,4])
        title = VGroup(title_bg, title_text).move_to(UP * 1.8)
        
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
        # Câu hỏi mở – đặt dưới title, tập trung gần ORIGIN
        # Căn bắt đầu bất buộc sau title để giữ layout thẳng đứng rõ ràng
        question_text.next_to(title, DOWN, buff=0.8)
        
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
