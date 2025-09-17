from tkinter import ttk
import tkinter as tk
import pandas as pd
from events.scroll_event import scroll_event

class Filter_component:
    def __init__(self, parent,filter_canvas,filter_area=None,filter_scrollbar=None,dataLoader=None):
        self.parent = parent
        self.dataLoader = dataLoader
        self.filter_area = filter_area
        self.filter_canvas = filter_canvas
        self.filter_scrollbar = filter_scrollbar
        self.filters = []
        self.scroller = scroll_event()
        
    def add_filter(self):
        if self.dataLoader.df is None:
            return

        cols = list(self.dataLoader.df.columns)
        direction_cols, speed_cols = self.dataLoader.detect_direction_speed_columns(cols)
        filterable_cols = [col for col in cols if col not in direction_cols + speed_cols]

        filter_frame = ttk.Frame(self.filter_area)
        filter_frame.pack(fill="x", pady=5, expand=True)  # Thêm expand=True

        column_var = tk.StringVar()
        column_combo = ttk.Combobox(filter_frame, textvariable=column_var, state="readonly")
        column_combo["values"] = filterable_cols
        column_combo.grid(row=0, column=0, padx=5, sticky="ew")

        value_var = tk.StringVar()
        value_combo = ttk.Combobox(filter_frame, textvariable=value_var, state="readonly")
        value_combo.grid(row=0, column=1, padx=5, sticky="ew")

        def update_values(event):
            col = column_var.get()
            if col:
                unique_values = sorted(self.dataLoader.df[col].dropna().unique())
                value_combo["values"] = unique_values

        column_combo.bind("<<ComboboxSelected>>", update_values)

        remove_btn = ttk.Button(filter_frame, text="Xóa", command=lambda: self.remove_filter(filter_frame))
        remove_btn.grid(row=0, column=2, padx=5)

        self.filters.append({
            "column_var": column_var,
            "value_var": value_var,
            "frame": filter_frame
        })

        # Cập nhật scrollregion sau khi thêm filter
        self.scroller._update_scrollbar(self.filter_canvas,self.filter_scrollbar)
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))

    def remove_filter(self, frame):
        for f in self.filters:
            if f["frame"] == frame:
                f["frame"].destroy()
                self.filters.remove(f)
                break
        # Cập nhật scrollregion sau khi xóa filter
        self.filter_canvas.update_idletasks()
        self.scroller._update_scrollbar(self.filter_canvas,self.filter_scrollbar)
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))
        
    def apply_filters(self):
        filtered_df = self.dataLoader.df.copy()
        # Gom các điều kiện lọc theo từng cột
        filter_dict = {}
        for f in self.filters:
            column = f["column_var"].get()
            value = f["value_var"].get()
            if column and value:
                filter_dict.setdefault(column, []).append(value)

        for column, values in filter_dict.items():
            col_dtype = filtered_df[column].dtype
            try:
                if pd.api.types.is_numeric_dtype(col_dtype):
                    values_cast = [float(v) for v in values]
                else:
                    values_cast = [str(v) for v in values]
            except Exception:
                values_cast = values
            filtered_df = filtered_df[filtered_df[column].isin(values_cast)]
        return filtered_df