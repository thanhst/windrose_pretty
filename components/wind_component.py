import tkinter as tk
from tkinter import ttk
from events.scroll_event import scroll_event

class Wind_component:
    def __init__(self, parent,wind_canvas,wind_area,scollbar=None):
        self.parent = parent
        self.df = None
        self.wind_canvas = wind_canvas
        self.wind_area = wind_area
        self.scoller = scroll_event()
        self.scollbar = scollbar
        self.style = ttk.Style()
        self.style.configure("Card.TFrame", background="#f9f9f9", padding=10)  # padding nội bộ


    def add_wind_item(self, value):
        if not hasattr(self, "wind_items"):
            self.wind_items = []
        index = len(self.wind_items)
        max_cols = 4
        row = index // max_cols
        col = index % max_cols
        
        frame = ttk.LabelFrame(self.wind_area, text=value)
        frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")

        self.wind_area.grid_columnconfigure(col, weight=1)

        remove_btn = ttk.Button(frame, text="Xóa",
                                command=lambda: self.remove_wind_item(frame))
        remove_btn.pack(side=tk.RIGHT, padx=5)

        self.wind_items.append({
            "value": value,
            "frame": frame
        })

        self.scoller._update_scrollbar(self.wind_canvas,self.scollbar)

    def remove_wind_item(self, frame):
        frame.destroy()
        self.wind_items = [w for w in self.wind_items if w["frame"] != frame]
        self.scoller._update_scrollbar(self.wind_canvas,self.scollbar)
    def get_selected_columns(self):
        return [item["value"] for item in self.wind_items]