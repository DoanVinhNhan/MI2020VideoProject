from manimlib import *

class Logo(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Khởi tạo logo theo chuẩn cơ bản
        box = RoundedRectangle(width=1.5, height=1.5, color=WHITE, fill_color=BLUE, fill_opacity=1)
        text = Text("LOGO", font_size=36, weight=BOLD, color=WHITE)
        self.add(box, text)
