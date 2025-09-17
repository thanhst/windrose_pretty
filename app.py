import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from windrose import WindroseAxes
import socket
from functools import partial

device_name = socket.gethostname()
print("Device name:", device_name)

if device_name == "DESKTOP-K3UQK9B":
    print("Chạy config dành riêng cho máy này 🚀")
if device_name == "R734":
    print("Máy này là máy của Huyền này 🚀")


class WindroseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windrose Data Explorer")
        self.root.geometry(f"{int(root.winfo_screenwidth()*0.75)}x{int(root.winfo_screenheight()*0.75)}")

        self.df = None
        self.filters = []  # Sửa thành list

        # Frame trên: chọn file + hiển thị dữ liệu
        top_frame = ttk.Frame(root)
        top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_btn = ttk.Button(top_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(anchor="w")

        self.tree = ttk.Treeview(top_frame, show="headings")
        self.tree.pack(fill="both", expand=True)

        # Frame giữa: chọn cột và thêm bộ lọc
        mid_frame = ttk.Frame(root)
        mid_frame.pack(fill="x", padx=10, pady=10)

        frame_direction_v = ttk.Frame(mid_frame)
        frame_direction_v.grid(row=0,column=0, columnspan=3, sticky="ew")

        self.direction_var = tk.StringVar()
        self.speed_var = tk.StringVar()

        # self.direction_combo = ttk.Combobox(mid_frame, textvariable=self.direction_var, state="readonly")
        # self.direction_combo.grid(row=1, column=0, padx=5, sticky="ew")

        # self.speed_combo = ttk.Combobox(mid_frame, textvariable=self.speed_var, state="readonly")
        # self.speed_combo.grid(row=1, column=2, padx=5, sticky="ew")

        self.add_filter_btn = ttk.Button(mid_frame, text="Thêm Bộ Lọc", command=self.add_filter)
        self.add_filter_btn.grid(row=2, column=0, pady=10, sticky="w")

        self.plot_btn = ttk.Button(mid_frame, text="Vẽ Hoa Gió", command=self.plot_windrose, width=20,padding=10)
        self.plot_btn.grid(row=2, column=2, pady=10, sticky="e")

        mid_frame.grid_columnconfigure(0, weight=1)
        mid_frame.grid_columnconfigure(2, weight=1)

        # Frame dưới: hiển thị bộ lọc và biểu đồ
        filter_frame = ttk.LabelFrame(root, text="Bộ Lọc")
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Thêm canvas + scrollbar cho vùng bộ lọc
        self.filter_canvas = tk.Canvas(filter_frame, height=120)
        self.filter_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.filter_scrollbar = ttk.Scrollbar(filter_frame, orient="vertical", command=self.filter_canvas.yview)
        self.filter_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.filter_canvas.configure(yscrollcommand=self.filter_scrollbar.set)
        self.filter_area = tk.Frame(self.filter_canvas)
        self.filter_canvas.create_window((0, 0), window=self.filter_area, anchor="nw")



        wind_frame = ttk.LabelFrame(frame_direction_v, text="Hướng")
        wind_frame.pack(fill="x", padx=10, pady=10)

        self.wind_canvas = tk.Canvas(wind_frame, height=50)
        self.wind_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.wind_scrollbar = ttk.Scrollbar(wind_frame, orient="vertical", command=self.wind_canvas.yview)
        self.wind_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.wind_canvas.configure(yscrollcommand=self.wind_scrollbar.set)
        self.wind_area = tk.Frame(self.wind_canvas)
        self.wind_canvas.create_window((0,0), window=self.wind_area, anchor="nw")

        speed_frame = ttk.LabelFrame(frame_direction_v, text="Vận tốc gió")
        speed_frame.pack(fill="x", padx=10, pady=10)

        self.speed_canvas = tk.Canvas(speed_frame, height=50)
        self.speed_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.speed_scrollbar = ttk.Scrollbar(speed_frame, orient="vertical", command=self.speed_canvas.yview)
        self.speed_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.speed_canvas.configure(yscrollcommand=self.speed_scrollbar.set)
        self.speed_area = tk.Frame(self.speed_canvas)
        self.speed_canvas.create_window((0,0), window=self.speed_area, anchor="nw")

        # Kích hoạt con lăn chuột và scrollbar
        # self.filter_area.bind("<Enter>", lambda e: self._bind_mousewheel(self.filter_canvas))
        # self.filter_area.bind("<Leave>", lambda e: self._unbind_mousewheel(self.filter_canvas))
        # self.filter_canvas.bind('<Configure>', self._on_canvas_configure)

    def add_speed_item(self, value):
        frame = ttk.Frame(self.speed_area)
        frame.pack(fill="x", pady=2)

        label = ttk.Label(frame, text=f"{value}")
        label.pack(side=tk.LEFT, padx=5)

        remove_btn = ttk.Button(frame, text="Xóa", 
                                command=lambda: self.remove_speed_item(frame))
        remove_btn.pack(side=tk.RIGHT, padx=5)

        if not hasattr(self, "speed_items"):
            self.speed_items = []
        self.speed_items.append({
            "value": value,
            "frame": frame
        })

        self._update_speed_scrollbar()

    def remove_speed_item(self, frame):
        frame.destroy()
        self.speed_items = [s for s in self.speed_items if s["frame"] != frame]
        self._update_speed_scrollbar()

    def _update_speed_scrollbar(self):
        self.speed_canvas.update_idletasks()
        self.speed_canvas.configure(scrollregion=self.speed_canvas.bbox("all"))



    def add_wind_item(self, value):
        frame = ttk.Frame(self.wind_area)
        frame.pack(fill="x", pady=2)

        label = ttk.Label(frame, text=f"{value}")
        label.pack(side=tk.LEFT, padx=5)

        remove_btn = ttk.Button(frame, text="Xóa", 
                                command=lambda: self.remove_wind_item(frame))
        remove_btn.pack(side=tk.RIGHT, padx=5)

        if not hasattr(self, "wind_items"):
            self.wind_items = []
        self.wind_items.append({
            "value": value,
            "frame": frame
        })

        self._update_wind_scrollbar()

    def remove_wind_item(self, frame):
        frame.destroy()
        self.wind_items = [w for w in self.wind_items if w["frame"] != frame]
        self._update_wind_scrollbar()

    def _update_wind_scrollbar(self):
        self.wind_canvas.update_idletasks()
        self.wind_canvas.configure(scrollregion=self.wind_canvas.bbox("all"))

    def detect_direction_speed_columns(self, columns):
        # Từ khóa cho hướng gió và vận tốc (cả tiếng Anh & Việt)
        direction_keywords = ["direction", "hướng", "dir"]
        speed_keywords = ["speed", "vận tốc", "v", "spd"]

        direction_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in direction_keywords) or col.lower().startswith("hướng")]
        speed_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in speed_keywords) or col.lower().startswith("v")]
        
        for d in direction_cols:
            self.add_wind_item(d)

        for s in speed_cols:  # speed_cols lấy từ detect_direction_speed_columns
            self.add_speed_item(s)

        return direction_cols, speed_cols

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data files", "*.csv *.xls *.xlsx"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                self.df = pd.read_csv(file_path)
            else:
                self.df = pd.read_excel(file_path)

            cols = list(self.df.columns)
            direction_cols, speed_cols = self.detect_direction_speed_columns(cols)
            # Chỉ hiển thị các cột hướng ở combobox hướng
            # self.direction_combo["values"] = direction_cols if direction_cols else cols
            # self.speed_combo["values"] = speed_cols if speed_cols else cols

            # Update bảng dữ liệu
            self.update_tree()

            messagebox.showinfo("Thành công", "File đã được load!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không load được file: {e}")

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)

        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        for _, row in self.df.head(100).iterrows():
            self.tree.insert("", "end", values=list(row))

    def _on_canvas_configure(self, event):
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))
        bbox = self.filter_canvas.bbox("all")
        if bbox:
            content_height = bbox[3] - bbox[1]
            canvas_height = self.filter_canvas.winfo_height()
            if content_height <= canvas_height:
                # Ẩn scrollbar
                if self.filter_scrollbar.winfo_ismapped():
                    self.filter_scrollbar.pack_forget()
                # Tắt cuộn
                self._unbind_mousewheel(self.filter_canvas)
            else:
                # Hiện scrollbar
                if not self.filter_scrollbar.winfo_ismapped():
                    self.filter_scrollbar.pack(side=tk.RIGHT, fill="y")
                # Bật cuộn cho canvas, chỉ canvas thôi
                self._bind_mousewheel(self.filter_canvas)


    def _bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda e: self._activate_mousewheel(widget))
        widget.bind("<Leave>", lambda e: self._deactivate_mousewheel(widget))

    def _activate_mousewheel(self, widget, event=None):
        widget.bind("<MouseWheel>", lambda e: self._on_mousewheel(widget, e))

    def _deactivate_mousewheel(self, widget, event=None):
        widget.unbind("<MouseWheel>")

    def _on_mousewheel(self, widget, event):
        widget.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"
    def _unbind_mousewheel(self, widget): 
        widget.unbind("<MouseWheel>")

    def add_filter(self):
        if self.df is None:
            return

        cols = list(self.df.columns)
        direction_cols, speed_cols = self.detect_direction_speed_columns(cols)
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
                unique_values = sorted(self.df[col].dropna().unique())
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
        self._update_scrollbar()
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))

    def remove_filter(self, frame):
        for f in self.filters:
            if f["frame"] == frame:
                f["frame"].destroy()
                self.filters.remove(f)
                break
        # Cập nhật scrollregion sau khi xóa filter
        self.filter_canvas.update_idletasks()
        self._update_scrollbar()
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))
    
    def _update_scrollbar(self):
        self.filter_canvas.update_idletasks()
        self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all"))

        bbox = self.filter_canvas.bbox("all")
        if bbox:
            content_height = bbox[3] - bbox[1]
            canvas_height = self.filter_canvas.winfo_height()

            if content_height <= canvas_height:
                # Ẩn scrollbar
                if self.filter_scrollbar.winfo_ismapped():
                    self.filter_scrollbar.pack_forget()
                self._unbind_mousewheel(self.filter_canvas)
            else:
                # Hiện scrollbar
                if not self.filter_scrollbar.winfo_ismapped():
                    self.filter_scrollbar.pack(side=tk.RIGHT, fill="y")
                # Bật scroll cho canvas
                self._activate_mousewheel(self.filter_canvas)


    def apply_filters(self):
        filtered_df = self.df.copy()
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

    def plot_windrose(self):
        if self.df is None:
            messagebox.showwarning("Không có dữ liệu", "Hãy load dữ liệu trước khi vẽ biểu đồ!")
            return

        direction_col = self.direction_var.get()
        speed_col = self.speed_var.get()

        if not direction_col or not speed_col:
            messagebox.showwarning("Chưa chọn", "Hãy chọn cả cột hướng gió và tốc độ gió!")
            return

        filtered_df = self.apply_filters()

        if filtered_df.empty:
            messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu sau khi áp dụng bộ lọc!")
            return

        directions = filtered_df[direction_col].dropna().astype(float)
        speeds = filtered_df[speed_col].dropna().astype(float)

        if directions.empty or speeds.empty:
            messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để vẽ biểu đồ!")
            return

        calm_count = (speeds <= 0.5).sum()
        calm_percent = calm_count / len(speeds) * 100 if len(speeds) > 0 else 0

        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        fig = plt.Figure(figsize=(6, 6), dpi=100)
        ax = WindroseAxes.from_ax(fig=fig)
        ax.bar(
            directions,
            speeds,
            normed=True,
            opening=0.8,
            edgecolor="white",
            bins=bins,
            cmap=plt.cm.RdYlBu_r
        )
        ax.set_legend(title="Tốc độ gió (m/s)", loc="lower right", fontsize=8)
        fig.text(0.5, 0.05, f"Tần suất gió lặng: {calm_percent:.2f}%", ha="center", fontsize=10)

        # Hiển thị trên cửa sổ mới
        new_window = tk.Toplevel(self.root)
        new_window.title("Windrose Chart")
        new_window.geometry(f"{int(root.winfo_screenwidth()*0.5)}x{int(root.winfo_screenheight()*0.5)}")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = WindroseGUI(root)
    root.mainloop()