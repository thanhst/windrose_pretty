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
        if not hasattr(self, "speed_items"):
            self.speed_items = []
        index = len(self.speed_items)
        max_cols = 4
        row = index // max_cols
        col = index % max_cols
        
        frame = ttk.LabelFrame(self.speed_area, text=value)
        frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
                
        self.speed_area.grid_columnconfigure(col, weight=1)

        remove_btn = ttk.Button(frame, text="Xóa", 
                                command=lambda: self.remove_speed_item(frame))
        remove_btn.pack(side=tk.RIGHT, padx=5)

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