import sys
import os

# Tuân thủ Agent Instruction: Cập nhật đường dẫn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manimlib import *
from object.background import Background
from object.logo import Logo
# Import SAU manimlib để ghi đè UP/DOWN/LEFT/RIGHT và định nghĩa font-size constants
from object.layout_9_16 import *

config.frame_size = (1080,1920) 


class OpenVideo(Scene):
    def construct(self):
        # 1. Tuân thủ Định dạng video: Đặt màu nền là BLACK
        self.camera.background_color = BLACK
        
        # 2. Tuân thủ Các object dùng chung: Tái sử dụng Background class
        bg = Background()
        self.add(bg)
        
        # 3. Logo mở đầu: Fade in tại ORIGIN
        logo = Logo().move_to(ORIGIN)
        self.play(FadeIn(logo, shift=UP), run_time=0.5)
        self.wait(0.5)
        
        # Di chuyển logo vào góc trên trái trong vùng an toàn
        # Dùng SAFE_TOP và SAFE_LEFT từ layout_9_16 để đảm bảo không bị cắt
        self.play(
            logo.animate.scale(0.4).move_to(SAFE_TOP + SAFE_LEFT),
            run_time=0.5
        )
        
        # 4. Tiêu đề (Title)
        # Bảng màu & Phông chữ: Title là Chữ trắng (WHITE), nền xanh (BLUE), font_size=48, weight=BOLD
        title_text = Text(
            "Đánh giá chất lượng\nHệ thống truyền tin", 
            font_size=TITLE_FONT_SIZE,
            weight=BOLD, 
            color=WHITE,
            font="Sans-serif"
        )
        title_bg = BackgroundRectangle(title_text, color=BLUE, fill_opacity=1, buff=0.2)
        # Đặt title ngay dưới logo, bên trong vùng an toàn
        # SAFE_TOP (y=3.4) trừ chiều cao title + logo để layout thẳng đứng
        title = VGroup(title_bg, title_text).move_to(UP * 2.2)
        
        self.play(FadeIn(title, shift=DOWN), run_time=0.5)
        self.wait(1)
        
        # 5. Câu hỏi mở từ script.txt: 
        # "Làm sao để ta có thể đánh giá được chất lượng và độ tin cậy của một hệ thống truyền tin?"
        question_text = Text(
            "Làm sao để ta có thể đánh giá được\nchất lượng và độ tin cậy\ncủa một hệ thống truyền tin?", 
            font_size=SUBTITLE_FONT_SIZE,
            color=WHITE,
            font="Sans-serif",
            alignment="CENTER"
        )
        # Câu hỏi mở — đặt tại ORIGIN (tâm màn hình) theo Video_format.md
        question_text.move_to(ORIGIN)
        
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
