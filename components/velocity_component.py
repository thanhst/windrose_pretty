from tkinter import ttk
import tkinter as tk
from events.scroll_event import scroll_event
class Velocity_component:
    def __init__(self, parent,speed_canvas,speed_area,scrollbar=None):
        self.parent = parent
        self.df = None
        self.speed_canvas = speed_canvas
        self.speed_area = speed_area
        self.scroller = scroll_event()
        self.scrollbar = scrollbar
        
    def add_speed_item(self, value):
        frame = ttk.Frame(self.speed_area)
        frame.pack(fill="x", pady=2)
        
        speed_combo = ttk.Label(frame, text=value)
        speed_combo.pack(side=tk.LEFT, padx=10)

        remove_btn = ttk.Button(frame, text="Xóa", 
                                command=lambda: self.remove_speed_item(frame))
        remove_btn.pack(side=tk.RIGHT, padx=5)

        if not hasattr(self, "speed_items"):
            self.speed_items = []
        self.speed_items.append({
            "value": value,
            "frame": frame
        })

        self.scroller._update_scrollbar(self.speed_canvas,self.scrollbar)

    def remove_speed_item(self, frame):
        frame.destroy()
        self.speed_items = [s for s in self.speed_items if s["frame"] != frame]
        self.scroller._update_scrollbar(self.speed_canvas,self.scrollbar)
    def get_selected_columns(self):
        return [item["value"] for item in self.speed_items]