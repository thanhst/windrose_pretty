import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from windrose import WindroseAxes
import tkinter as tk
from tkinter import ttk


class WindrosePlotter:
    def __init__(self, parent):
        self.parent = parent

        # Frame dưới: hiển thị biểu đồ
        self.frame = ttk.LabelFrame(parent, text="Windrose Visualization")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.plot_area = tk.Frame(self.frame)
        self.plot_area.pack(fill="both", expand=True)

    def plot(self, df, direction_col, speed_col):
        # Kiểm tra dữ liệu đầu vào
        if df is None or direction_col not in df.columns or speed_col not in df.columns:
            tk.messagebox.showerror("Lỗi", "Dữ liệu hoặc cột không hợp lệ!")
            return

        try:
            # Lấy dữ liệu từ các cột
            directions = df[direction_col].dropna().astype(float)
            speeds = df[speed_col].dropna().astype(float)

            # Kiểm tra nếu không có dữ liệu
            if directions.empty or speeds.empty:
                tk.messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để vẽ biểu đồ!")
                return

            # Tính gió lặng (≤ 0.5 m/s)
            calm_count = (speeds <= 0.5).sum()
            calm_percent = calm_count / len(speeds) * 100 if len(speeds) > 0 else 0

            # Vẽ windrose
            fig = plt.Figure(figsize=(6, 6), dpi=100)
            ax = WindroseAxes.from_ax(fig=fig)
            ax.bar(
                directions,
                speeds,
                normed=True,
                opening=0.8,
                edgecolor="white",
                bins=[1, 2, 3, 4, 5, 6, 7, 8],
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

        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Không thể vẽ biểu đồ: {e}")