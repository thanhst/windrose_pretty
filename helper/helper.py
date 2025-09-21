import os
import sys
def resource_path(relative_path):
    """Trả về path đúng khi chạy .py hoặc .exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
def round_corners(img, radius=30):
    """Bo tròn góc ảnh hình vuông/rect"""
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
    img.putalpha(mask)
    return img

def circle_crop(img,size):
    """Cắt ảnh thành hình tròn"""
    img = img.resize((size, size))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    return img

class RainbowCircle(tk.Canvas):
    def __init__(self, parent, img_path, size=300, border_width=10, *args, **kwargs):
        super().__init__(parent, width=size+border_width*2, height=size+border_width*2, highlightthickness=0, *args, **kwargs)

        # Load ảnh cắt tròn
        pil_img = Image.open(img_path)
        pil_img = circle_crop(pil_img,size)
        self.tk_img = ImageTk.PhotoImage(pil_img)

        self.size = size
        self.border_width = border_width

        # Vẽ viền (oval) và ảnh
        self.border = self.create_oval(border_width//2, border_width//2,
                                       size+border_width*1.5, size+border_width*1.5,
                                       width=border_width, outline="red")
        self.create_image(border_width, border_width, anchor="nw", image=self.tk_img)

        # 7 màu cầu vồng
        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        self.color_index = 0

        # Bắt đầu animation
        self.animate()

    def animate(self):
        color = self.colors[self.color_index]
        self.itemconfig(self.border, outline=color)
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.after(300, self.animate)  # đổi màu sau 300ms