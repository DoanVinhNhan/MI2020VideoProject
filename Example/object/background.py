from manimlib import *

class Background(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Lưới (Grid)
        # Tọa độ 9:16: frame_width=4.5 (X: -2.25~2.25), frame_height=8 (Y: -4~4)
        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
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
