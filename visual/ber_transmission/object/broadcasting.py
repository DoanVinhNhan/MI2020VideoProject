from manimlib import *
import os

from object.bit import BitSequence

class Broadcasting(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "svg", "broadcasting.svg"))
        self.icon = SVGMobject(svg_path).scale(1.3).set_color(GOLD_B)
        self.add(self.icon)
        
        self.label = Text("Sent:", font_size=24, weight=BOLD).next_to(self.icon, DOWN, buff=0.5).set_color(WHITE)
        self.add(self.label)
        
        self.current_seq_display = None
        self.prev_seq_display = None
        
    def update_sequence(self, scene, new_seq_str, run_time=0.3):
        new_display = BitSequence(sequence=new_seq_str, color="#00FF00", font_size=32)
        new_display.next_to(self.label, DOWN, buff=0.5)
        
        if self.current_seq_display:
            animations = []
            if self.prev_seq_display:
                animations.append(FadeOut(self.prev_seq_display))
            
            self.prev_seq_display = self.current_seq_display
            self.current_seq_display = new_display
            
            animations.append(FadeIn(self.current_seq_display))
            animations.append(
                self.prev_seq_display.animate.next_to(self.current_seq_display, DOWN, buff=0.3).set_opacity(0.3)
            )
            
            scene.play(*animations, run_time=run_time)
        else:
            self.current_seq_display = new_display
            scene.play(FadeIn(self.current_seq_display), run_time=run_time)
