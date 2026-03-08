"""
open_scene.py
=============
Mở đầu video: Logo → Title → Câu hỏi mở.

Nội dung dựa trên script.txt – Phần 1: Tình huống dẫn nhập.
  • Title    : "Xác Suất Lỗi Bit" / "BEP"
  • Subtitle : "Bit Error Probability"
  • Câu hỏi mở: "Làm sao để đánh giá được chất lượng
                 và độ tin cậy của một hệ thống truyền tin?"

Tuân thủ:
  - Video_format   : 9:16, 1080×1920, 60 fps
  - Color_vs_Font  : WHITE title / BLUE bg / RED subtitle / BLACK nền
  - Effects        : FadeIn, Write, Indicate, safe-zone
  - Optimal        : VGroup, remove khi hết màn hình
  - layout.py      : TITLE_FONT_SIZE, SUBTITLE_FONT_SIZE, CAPTION_FONT_SIZE,
                     SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT
"""

import sys
import os

# ─── Thêm thư mục gốc workspace vào path ─────────────────────────────────────
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from manimlib import *
from layout import (
    UP, DOWN, LEFT, RIGHT, ORIGIN,
    TITLE_FONT_SIZE, SUBTITLE_FONT_SIZE, CAPTION_FONT_SIZE,
    SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT,
)
from object.background import Background
from object.logo import Logo

# ─────────────────────────────────────────────────────────────────────────────
# Hằng số cục bộ
# ─────────────────────────────────────────────────────────────────────────────
LOGO_CORNER   = SAFE_TOP + LEFT * 4 + DOWN * 0.1   # góc trên-trái an toàn
LOGO_CENTER   = SAFE_TOP + DOWN * 0.55              # chính giữa khi mở đầu

TITLE_TEXT    = "Xác Suất Lỗi Bit"
TITLE_SUB     = "Bit Error Probability"
ACRONYM_TEXT  = "BEP"

QUESTION_LINE1 = "Làm sao để đánh giá được"
QUESTION_LINE2 = "chất lượng và độ tin cậy"
QUESTION_LINE3 = "của một hệ thống truyền tin?"


# ─────────────────────────────────────────────────────────────────────────────
class OpenScene(Scene):
    """
    Cấu trúc 3 beat:
      Beat 1 – Logo reveal   : Logo xuất hiện chính giữa, rồi thu nhỏ và
                               bay về góc trên-trái.
      Beat 2 – Title card    : Hộp tiêu đề (BLUE bg / WHITE text) và
                               acronym BEP (RED / YELLOW bg) FadeIn từ dưới.
      Beat 3 – Câu hỏi mở   : Câu hỏi Write() từng dòng, Indicate nhấn mạnh.
    """

    def construct(self):
        # ── Thiết lập màn hình ─────────────────────────────────────────────
        self.camera.background_color = BLACK

        bg = Background()
        self.add(bg)

        # ═══════════════════════════════════════════════════════════════════
        # BEAT 1 – Logo reveal
        # ═══════════════════════════════════════════════════════════════════
        logo_big = Logo().scale(1.6).move_to(ORIGIN)
        self.play(FadeIn(logo_big, shift=DOWN * 0.3), run_time=0.8)
        self.wait(0.6)

        # Thu nhỏ và bay về góc trên-trái
        logo_small = Logo().scale(0.55).move_to(LOGO_CORNER)
        self.play(
            ReplacementTransform(logo_big, logo_small),
            run_time=0.6,
        )
        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════════════
        # BEAT 2 – Title card
        # ═══════════════════════════════════════════════════════════════════
        # --- Hộp tiêu đề chính (nền BLUE, text WHITE) ----------------------
        title_box = RoundedRectangle(
            width=3.6, height=1.0,
            corner_radius=0.12,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1,
        ).move_to(ORIGIN + UP * 1.2)

        title_text = Text(
            TITLE_TEXT,
            font="Sans-serif",
            font_size=TITLE_FONT_SIZE,
            weight=BOLD,
            color=WHITE,
        ).move_to(title_box.get_center())

        title_group = VGroup(title_box, title_text)

        # --- Hộp acronym BEP (nền YELLOW, text RED) ------------------------
        bep_box = RoundedRectangle(
            width=1.4, height=0.7,
            corner_radius=0.10,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=1,
        ).move_to(ORIGIN + UP * 0.35)

        bep_text = Text(
            ACRONYM_TEXT,
            font="Sans-serif",
            font_size=TITLE_FONT_SIZE + 4,
            weight=BOLD,
            color=RED,
        ).move_to(bep_box.get_center())

        bep_group = VGroup(bep_box, bep_text)

        # --- Dòng subtitle (nền transparent, text WHITE nhỏ) ----------------
        subtitle = Text(
            TITLE_SUB,
            font="Sans-serif",
            font_size=SUBTITLE_FONT_SIZE,
            color=WHITE,
        ).move_to(ORIGIN + DOWN * 0.25)

        # --- Animate title card vào ----------------------------------------
        self.play(
            FadeIn(title_group, shift=UP * 0.25),
            run_time=0.5,
        )
        self.play(
            FadeIn(bep_group, shift=UP * 0.2),
            FadeIn(subtitle, shift=UP * 0.2),
            run_time=0.5,
        )
        self.wait(0.8)

        # Indicate acronym để nhấn mạnh
        self.play(Indicate(bep_group), run_time=0.6)
        self.wait(0.4)

        # Dọn title card để chuyển qua beat câu hỏi mở
        self.play(
            FadeOut(title_group, shift=UP * 0.25),
            FadeOut(bep_group, shift=UP * 0.15),
            FadeOut(subtitle, shift=UP * 0.15),
            run_time=0.4,
        )
        self.remove(title_group, bep_group, subtitle)

        # ═══════════════════════════════════════════════════════════════════
        # BEAT 3 – Câu hỏi mở
        # ═══════════════════════════════════════════════════════════════════
        # Dấu hỏi lớn làm điểm nhấn trực quan
        big_q = Text("?", font="Sans-serif", font_size=80, weight=BOLD, color=YELLOW)
        big_q.move_to(ORIGIN + UP * 1.8)
        self.play(FadeIn(big_q, shift=DOWN * 0.2), run_time=0.4)

        # Ba dòng câu hỏi Write() tuần tự
        q1 = Text(
            QUESTION_LINE1,
            font="Sans-serif",
            font_size=SUBTITLE_FONT_SIZE,
            color=WHITE,
        ).move_to(ORIGIN + UP * 0.9)

        q2 = Text(
            QUESTION_LINE2,
            font="Sans-serif",
            font_size=SUBTITLE_FONT_SIZE,
            color=WHITE,
        ).move_to(ORIGIN + UP * 0.55)

        q3 = Text(
            QUESTION_LINE3,
            font="Sans-serif",
            font_size=SUBTITLE_FONT_SIZE,
            color=YELLOW,
            weight=BOLD,
        ).move_to(ORIGIN + UP * 0.18)

        self.play(Write(q1), run_time=0.8)
        self.play(Write(q2), run_time=0.8)
        self.play(Write(q3), run_time=1.0)
        self.wait(0.5)

        # Nhấn mạnh toàn bộ câu hỏi
        question_group = VGroup(big_q, q1, q2, q3)
        self.play(Indicate(question_group), run_time=0.8)
        self.wait(1.2)

        # Fade out toàn bộ để kết thúc cảnh mở đầu
        self.play(
            FadeOut(question_group, shift=UP * 0.2),
            FadeOut(logo_small, shift=LEFT * 0.2),
            FadeOut(bg),
            run_time=0.5,
        )
