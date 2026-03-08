"""
layout_9_16.py
==============
Redefine unit vectors và font-size constants cho tỷ lệ 9:16.

Lý do:
  - 16:9 mặc định: frame_width = 14.22, frame_height = 8
  - 9:16 của ta  : frame_width =  4.5,  frame_height = 8

  → UP/DOWN  : chiều dọc KHÔNG đổi (frame_height vẫn = 8).
  → LEFT/RIGHT: chiều ngang thu hẹp theo hệ số 4.5 / 14.22 ≈ 0.316.
    Tức là mỗi đơn vị RIGHT bây giờ "đi xa hơn" so với 16:9 → scale xuống
    để code 16:9 cũ cho phép số lớn như "RIGHT * 5" vẫn dùng được.

Cách dùng:
  from object.layout_9_16 import *   # đặt SAU "from manimlib import *"
  → UP, DOWN, LEFT, RIGHT, ORIGIN bị ghi đè bởi phiên bản 9:16.

Bảng đổi tương đương:
  16:9 half-width  ≈ 7.11  →  9:16 half-width  ≈ 2.25
  Scale factor   = 2.25 / 7.11 ≈ 0.316
"""

import numpy as np

# ─── Hệ số co ──────────────────────────────────────────────────────────────
_H_SCALE = 4.5 / 14.222   # ≈ 0.316  (chiều ngang)
# _V_SCALE = 1.0           # chiều dọc giữ nguyên

# ─── Unit vectors (ghi đè manimlib) ────────────────────────────────────────
# UP / DOWN : không đổi magnitude (frame_height giữ nguyên)
UP    = np.array([0.,  1., 0.])
DOWN  = np.array([0., -1., 0.])

# LEFT / RIGHT: scale lại để 1 đơn vị vẫn "chiếm cùng % màn hình" như 16:9
LEFT  = np.array([-1., 0., 0.]) * _H_SCALE   # ≈ [-0.316, 0, 0]
RIGHT = np.array([ 1., 0., 0.]) * _H_SCALE   # ≈ [ 0.316, 0, 0]

# ORIGIN giữ nguyên
ORIGIN = np.array([0., 0., 0.])

# ─── Font-size constants ────────────────────────────────────────────────────
# Quy ước Color_vs_Font.md         16:9    →   9:16
TITLE_FONT_SIZE    = 20   # (thay vì 48)  – đủ rõ, không tràn chiều ngang
SUBTITLE_FONT_SIZE = 12   # (thay vì 32)  – fit trong frame hẹp
CAPTION_FONT_SIZE  = 10   # text chú thích nhỏ

# ─── Safe-zone anchor points ────────────────────────────────────────────────
# frame_height=8  → half = 4.0  → 15% margin = 0.6  → safe = ±3.4
# frame_width=4.5 → half = 2.25 → 15% margin = 0.34 → safe = ±1.91
SAFE_TOP    = np.array([0.,  3.4, 0.])
SAFE_BOTTOM = np.array([0., -3.4, 0.])
SAFE_LEFT   = np.array([-1.9, 0., 0.])
SAFE_RIGHT  = np.array([ 1.9, 0., 0.])
