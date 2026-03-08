from manimlib import *

class Background(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Lưới (Grid)
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={
                "stroke_width":0,
                "include_tip":False,
            }
        )

        
        # Thêm lưới và trục toạ độ vào VGroup
        self.add(grid)
