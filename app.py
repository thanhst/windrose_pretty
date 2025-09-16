import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from windrose import WindroseAxes
import socket

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
        self.filters = {}

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

        ttk.Label(mid_frame, text="Chọn cột hướng gió:").grid(row=0, column=0, sticky="w")
        ttk.Label(mid_frame, text="Chọn cột tốc độ gió:").grid(row=0, column=2, sticky="w")

        self.direction_var = tk.StringVar()
        self.speed_var = tk.StringVar()

        self.direction_combo = ttk.Combobox(mid_frame, textvariable=self.direction_var, state="readonly")
        self.direction_combo.grid(row=1, column=0, padx=5, sticky="ew")

        self.speed_combo = ttk.Combobox(mid_frame, textvariable=self.speed_var, state="readonly")
        self.speed_combo.grid(row=1, column=2, padx=5, sticky="ew")

        self.add_filter_btn = ttk.Button(mid_frame, text="Thêm Bộ Lọc", command=self.add_filter)
        self.add_filter_btn.grid(row=2, column=0, pady=10, sticky="w")

        self.plot_btn = ttk.Button(mid_frame, text="Vẽ Hoa Gió", command=self.plot_windrose)
        self.plot_btn.grid(row=2, column=2, pady=10, sticky="e")

        mid_frame.grid_columnconfigure(0, weight=1)
        mid_frame.grid_columnconfigure(2, weight=1)

        # Frame dưới: hiển thị bộ lọc và biểu đồ
        filter_frame = ttk.LabelFrame(root, text="Bộ Lọc")
        filter_frame.pack(fill="x", padx=10, pady=10)

        self.filter_area = tk.Frame(filter_frame)
        self.filter_area.pack(fill="x", expand=True)

        bottom_frame = ttk.LabelFrame(root, text="Windrose Visualization")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.plot_area = tk.Frame(bottom_frame)
        self.plot_area.pack(fill="both", expand=True)

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

            # Cập nhật combobox
            cols = list(self.df.columns)
            self.direction_combo["values"] = cols
            self.speed_combo["values"] = cols

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

    def add_filter(self):
        if self.df is None:
            return

        # Tạo bộ lọc mới
        filter_frame = ttk.Frame(self.filter_area)
        filter_frame.pack(fill="x", pady=5)

        column_var = tk.StringVar()
        column_combo = ttk.Combobox(filter_frame, textvariable=column_var, state="readonly")
        column_combo["values"] = list(self.df.columns)
        column_combo.grid(row=0, column=0, padx=5, sticky="ew")

        value_var = tk.StringVar()
        value_entry = ttk.Entry(filter_frame, textvariable=value_var)
        value_entry.grid(row=0, column=1, padx=5, sticky="ew")

        remove_btn = ttk.Button(filter_frame, text="Xóa", command=lambda: self.remove_filter(filter_frame, column_var.get()))
        remove_btn.grid(row=0, column=2, padx=5)

        self.filters[column_var.get()] = value_var

    def remove_filter(self, frame, column_var):
        frame.destroy()
        if column_var in self.filters:
            del self.filters[column_var]

    def apply_filters(self):
        filtered_df = self.df.copy()
        for column_var, value_var in self.filters.items():
            column = column_var.get()
            value = value_var.get()
            if column and value:
                filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, na=False)]
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

        # Kiểm tra nếu không có dữ liệu
        if directions.empty or speeds.empty:
            messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để vẽ biểu đồ!")
            return

        # Tính gió lặng (≤ 0.5 m/s)
        calm_count = (speeds <= 0.5).sum()
        calm_percent = calm_count / len(speeds) * 100 if len(speeds) > 0 else 0

        # Điều chỉnh bins để phù hợp với dữ liệu
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        # Vẽ windrose
        fig = plt.Figure(figsize=(6, 6), dpi=100)
        ax = WindroseAxes.from_ax(fig=fig)
        ax.bar(
            directions,
            speeds,
            normed=True,
            opening=0.8,
            edgecolor="white",
            bins=bins,  # Sử dụng bins bắt đầu từ 0
            cmap=plt.cm.RdYlBu_r
        )
        ax.set_legend(title="Tốc độ gió (m/s)", loc="lower right", fontsize=8)
        fig.text(0.5, 0.05, f"Tần suất gió lặng: {calm_percent:.2f}%", ha="center", fontsize=10)

        # Hiển thị trong Tkinter
        for widget in self.plot_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = WindroseGUI(root)
    root.mainloop()