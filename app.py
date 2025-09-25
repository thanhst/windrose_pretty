import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from windrose import WindroseAxes
import socket
from components.dataframe_loader import DataFrameLoader
from events.scroll_event import scroll_event
from components.filter_component import Filter_component
from components.wind_component import Wind_component
from components.velocity_component import Velocity_component
import numpy as np
from tkinter import PhotoImage
import sys, os
from helper.helper import circle_crop,round_corners, RainbowCircle, resource_path
from helper.config import getConfig,getConfigPath
import json

device_name = socket.gethostname()
print("Device name:", device_name)

if device_name == "DESKTOP-K3UQK9B":
    print("Chạy config dành riêng cho máy này 🚀")
if device_name == "R734":
    print("Máy này là máy của Huyền này 🚀")
if device_name == "Thanh-Laptop":
    print("Máy này là máy của Thanh này 🚀")



class WindroseGUI:
    def __init__(self, root):
        self.root= root
        self.root.columnconfigure(0, weight=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=30) 
        
        self.filters = []

        top_frame = ttk.Frame(root)
        top_frame.grid(padx=10, pady=10, sticky="nsew", row=0, column=0)

        mid_frame = ttk.Frame(root)
        mid_frame.grid(padx=10, pady=10, sticky="ew", row=1, column=0)

        mid_frame.grid_columnconfigure(0, weight=1)
        mid_frame.grid_columnconfigure(2, weight=1)
        
        
        #helper

        self.tree = ttk.Treeview(top_frame, show="headings", height=5)  # chỉ hiện 5 dòng
        self.tree.pack(fill="x", expand=False)

        self.scroller= scroll_event()

        #dir_v
        frame_direction_v = ttk.Frame(mid_frame)
        frame_direction_v.grid(row=0,column=0, columnspan=8, sticky="ew")


        self.plot_btn = ttk.Button(mid_frame, text="Vẽ Hoa Gió", command=self.plot_windrose, width=25,padding=5)
        self.plot_btn.grid(row=2, column=5, pady=10, sticky="e")
        #filter
        filter_frame = ttk.LabelFrame(root, text="Bộ Lọc")
        filter_frame.grid(padx=10, pady=10, sticky="nsew", row=2, column=0)
        
        self.filter_canvas = tk.Canvas(filter_frame, height=120)
        self.filter_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.filter_scrollbar = ttk.Scrollbar(filter_frame, orient="vertical", command=self.filter_canvas.yview)
        self.filter_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.filter_canvas.configure(yscrollcommand=self.filter_scrollbar.set)
        self.filter_area = tk.Frame(self.filter_canvas)
        self.filter_canvas.create_window((0, 0), window=self.filter_area, anchor="nw")
        

        #wind
        wind_frame = ttk.LabelFrame(frame_direction_v, text="Hướng")
        wind_frame.pack(fill="both", padx=10, pady=10, expand=True)
        wind_frame.pack_propagate(False)

        wind_frame.config(height=int(root.winfo_screenheight() * 0.15))
        
        self.wind_canvas = tk.Canvas(wind_frame, height=50)
        self.wind_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.wind_scrollbar = ttk.Scrollbar(wind_frame, orient="vertical", command=self.wind_canvas.yview)
        self.wind_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.wind_canvas.configure(yscrollcommand=self.wind_scrollbar.set)
        self.wind_area = tk.Frame(self.wind_canvas)
        self.wind_canvas.create_window((0,0), window=self.wind_area, anchor="nw")
        
        self.windcom = Wind_component(self.root,self.wind_canvas,self.wind_area,self.wind_scrollbar)
        
        #speed
        speed_frame = ttk.LabelFrame(frame_direction_v, text="Vận tốc gió")
        speed_frame.pack(fill="both", padx=10, pady=10, expand=True)
        speed_frame.pack_propagate(False)

        speed_frame.config(height=int(root.winfo_screenheight() * 0.15))
        
        self.speed_canvas = tk.Canvas(speed_frame, height=50)
        self.speed_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.speed_scrollbar = ttk.Scrollbar(speed_frame, orient="vertical", command=self.speed_canvas.yview)
        self.speed_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.speed_canvas.configure(yscrollcommand=self.speed_scrollbar.set)
        self.speed_area = tk.Frame(self.speed_canvas)
        self.speed_canvas.create_window((0,0), window=self.speed_area, anchor="nw")
        self.speedcom = Velocity_component(self.root,self.speed_canvas,self.speed_area,self.speed_scrollbar)
        
        fram_load = ttk.Frame(top_frame)
        fram_load.pack(fill="both", pady=5)
        
        self.dataLoader = DataFrameLoader(fram_load,self.tree,self.windcom,self.speedcom)
        left_frame = tk.Frame(fram_load)
        left_frame.pack(side="left", padx=5)

        right_frame = tk.Frame(fram_load)
        right_frame.pack(side="right", padx=5)

        self.load_btn = ttk.Button(left_frame, text="Load File", command=self.dataLoader.load_file)
        self.load_btn.pack(pady=5, anchor="w", fill="x")

        self.load_dir_speed_btn = ttk.Button(left_frame, text="Load Direction and Velocity", command=self.dataLoader.update_direction_speed)
        self.load_dir_speed_btn.pack(pady=5, anchor="w", fill="x")
        
        if device_name == "R734" or device_name == "Thanh-Laptop":
            if getConfig():
                text_pretty = "Tắt sự xinh đẹp khi vào nha!"
            else:
                text_pretty = "Bật sự xinh đẹp khi vào nha!"
            
            self.set_up_btn = ttk.Button(right_frame, text=text_pretty, command=self.toggle_pretty)
            self.set_up_btn.pack(pady=20)
        
        self.filter = Filter_component(root,self.filter_canvas,self.filter_area,self.filter_scrollbar,self.dataLoader)

        self.add_filter_btn = ttk.Button(mid_frame, text="Thêm Bộ Lọc", command=self.filter.add_filter)
        self.add_filter_btn.grid(row=3, column=0, pady=10, sticky="w")
        
        ttk.Label(mid_frame, text="Bins (vd: 0,1,2,3,4,5)").grid(row=2, column=3, sticky="w", padx=10, pady=2)
        self.bins_entry = ttk.Entry(mid_frame)
        self.bins_entry.grid(row=3, column=3, sticky="ew", padx=5, pady=2)
        self.bins_entry.insert(0, "0,1,2,3,4,5,6,7,8")
        
        ttk.Label(mid_frame, text="Calm limit (vd: 0.5)").grid(row=2, column=4, sticky="w", padx=100, pady=2)
        self.calm_entry = ttk.Entry(mid_frame)
        self.calm_entry.grid(row=3, column=4, sticky="ew", padx=100, pady=2)
        self.calm_entry.insert(0, "None")
        
        
        
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
                self.scroller._unbind_mousewheel(self.filter_canvas)
            else:
                # Hiện scrollbar
                if not self.filter_scrollbar.winfo_ismapped():
                    self.filter_scrollbar.pack(side=tk.RIGHT, fill="y")
                # Bật cuộn cho canvas, chỉ canvas thôi
                self.scroller._bind_mousewheel(self.filter_canvas)

    def plot_windrose(self):
        import numpy as np
        if self.dataLoader.df is None:
            messagebox.showwarning("Không có dữ liệu", "Hãy load dữ liệu trước khi vẽ biểu đồ!")
            return

        direction_cols = self.windcom.get_selected_columns()
        speed_cols = self.speedcom.get_selected_columns()

        if not direction_cols or not speed_cols:
            messagebox.showwarning("Chưa chọn", "Hãy chọn ít nhất một cột hướng gió và tốc độ gió!")
            return

        filtered_df = self.filter.apply_filters()
        if filtered_df.empty:
            messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu sau khi áp dụng bộ lọc!")
            return

        fig = plt.Figure(figsize=(6, 6), dpi=100)
        ax = WindroseAxes.from_ax(fig=fig)

        total_speeds = []
        
        all_directions = []
        all_speeds = []
        df_list = []
        for d_col, s_col in zip(direction_cols, speed_cols):
            if d_col not in filtered_df.columns or s_col not in filtered_df.columns:
                continue
            
            tmp = filtered_df[[d_col, s_col]].dropna()
            # tmp = tmp[tmp[s_col] > 0]

            if tmp.empty:
                continue

            directions = tmp[d_col].astype(float)
            speeds = tmp[s_col].astype(float)
            tmp.columns = ["dir", "spd"]
            df_list.append(tmp)
            
            # directions = filtered_df[d_col].dropna().astype(float)
            # speeds = filtered_df[s_col].dropna().astype(float)

            if directions.max() <= 36:
                directions = directions * 10
            
            all_directions.append(directions)
            all_speeds.append(speeds)
            
            if directions.empty or speeds.empty:
                continue

            total_speeds.extend(speeds.tolist())
            
        wind_df = pd.concat(df_list, ignore_index=True)

        # Chuẩn hóa hướng
        if wind_df["dir"].max() <= 36:
            wind_df["dir"] = wind_df["dir"] * 10
        
        try:
            bins_str = self.bins_entry.get()
            bins = [float(b.strip()) for b in bins_str.split(",")]
            self.bins_entry.delete(0, tk.END)
            self.bins_entry.insert(0, ",".join(str(int(x)) for x in bins))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Bins không hợp lệ: {e}")
            return
        
        calm_input = self.calm_entry.get().strip()
        if calm_input.lower() == "none" or calm_input =="0":
            calm_limit = 0
            if len(bins) == 0 or bins[0] != 0:
                bins = [0] + bins
        else:
            try:
                calm_limit = float(calm_input)
                bins = [b for b in bins if b > calm_limit]
                bins_str
            except Exception as e:
                messagebox.showerror("Lỗi", f"Calm limit không hợp lệ: {e}")
                return
            
        non_calm = wind_df[wind_df["spd"] > calm_limit]
        non_calm.to_csv("wind_non_calm_lib.csv", index=False, encoding="utf-8-sig")
        ax.bar(
            non_calm["dir"],
            non_calm["spd"],
            bins=bins,
            normed=True,
            opening=1,
            edgecolor="white",
            cmap=plt.cm.jet,
            calm_limit=calm_limit,
            nsector=16,
            sectoroffset=0
        )

        # --- tính calm wind cho toàn bộ ---
        total_speeds = pd.Series(total_speeds)
        calm_count = (total_speeds <= calm_limit).sum()
        calm_percent = calm_count / len(total_speeds) * 100 if len(total_speeds) > 0 else 0
        ax.set_legend(
            title="Tốc độ gió (m/s)",
            loc='lower right',           # anchor point là góc dưới trái của legend
            bbox_to_anchor=(0, 0),  # (x, y) vị trí ngoài chart
            fontsize=8,
        )
        labels_dir = ["E", "ENE", "NE", "NNE", "N", "NNW", "NW", "WNW",
                "W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE"]

        angles = np.deg2rad(np.arange(0,360,360/16))   # 16 hướng
        ax.set_xticks(angles)
        ax.set_xticklabels(labels_dir, fontsize=9)
        ax.xaxis.set_tick_params(pad=15)
        fig.text(0.5, 0.02, f"Tần suất gió lặng: {calm_percent:.2f}%", ha="center", fontsize=10)

        new_window = tk.Toplevel(self.root)
        new_window.title("Windrose Chart")
        new_window.geometry(f"{int(self.root.winfo_screenwidth()*0.8)}x{int(self.root.winfo_screenheight()*0.8)}")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        all_directions = pd.concat(all_directions, ignore_index=True)
        all_speeds = pd.concat(all_speeds, ignore_index=True)
        df_counts = self.get_frequency_table(all_directions, all_speeds, bins, nsector=16, calm_limit=calm_limit)
        new_window_table = tk.Toplevel(self.root)
        new_window_table.title("Biểu đồ tần suất gió")
        new_window_table.geometry(f"{int(self.root.winfo_screenwidth()*0.8)}x{int(self.root.winfo_screenheight()*0.5)}")
        new_window_table.resizable(True, True)

        tree = ttk.Treeview(new_window_table)
        columns = ["Tốc độ gió"] + df_counts.columns.tolist()
        tree['columns'] = columns
        tree['show'] = 'headings'

        # Customize style
        #  # rowheight lớn hơn

        # headers
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=60, anchor='center')  # rộng hơn

        # rows
        for idx in df_counts.index:
            row_values = [idx] + df_counts.loc[idx].tolist()
            tree.insert("", "end", values=row_values)

        tree.pack(fill=tk.BOTH, expand=True)

    def get_frequency_table(self, directions, speeds, bins, nsector=16, calm_limit=None):
        import numpy as np
        import pandas as pd

        # Chuẩn hóa dữ liệu
        directions = directions.dropna().astype(float).values % 360
        speeds = speeds.dropna().astype(float).values

        if calm_limit is not None:
            mask = speeds > calm_limit
            directions = directions[mask]
            speeds = speeds[mask]

        # Chia sector + bin (bin cuối gom cả ∞)
        sector_edges = np.linspace(0, 360, nsector + 1)
        bin_edges = np.array(bins + [np.inf])

        # Tạo ma trận đếm
        freq_matrix = np.zeros((nsector, len(bin_edges) - 1), dtype=int)

        for i in range(nsector):
            sector_mask = (directions >= sector_edges[i]) & (directions < sector_edges[i + 1])
            sector_speeds = speeds[sector_mask]
            for j in range(len(bin_edges) - 1):
                bin_mask = (sector_speeds >= bin_edges[j]) & (sector_speeds < bin_edges[j + 1])
                freq_matrix[i, j] = np.sum(bin_mask)

        # Label sector
        sector_labels = np.round(sector_edges[:-1], 1)

        # Thêm tên hướng (N, NE, E, …)
        dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
                "S","SSW","SW","WSW","W","WNW","NW","NNW"]
        dir_labels = [dirs[int(i * len(dirs) / nsector)] for i in range(nsector)]

        # Label bin
        bin_labels = []
        for i in range(len(bin_edges) - 1):
            if np.isinf(bin_edges[i + 1]):
                bin_labels.append(f">= {bin_edges[i]}")
            else:
                bin_labels.append(f"{bin_edges[i]}-{bin_edges[i + 1]}")

        # DataFrame gốc: hướng là hàng
        df_counts = pd.DataFrame(freq_matrix, index=sector_labels, columns=bin_labels)

        # Đổi index từ độ -> tên hướng
        df_counts.index = [f"{int(sector_labels[i])}° ({dir_labels[i]})" for i in range(len(sector_labels))]

        # Transpose để: hàng = bin tốc độ, cột = hướng
        df_counts = df_counts.T

        return df_counts


    def toggle_pretty(self):
        current = getConfig()  # ✅ True/False
        config_path = getConfigPath()

        if current is False:
            # Bật "xinh đẹp"
            self.set_up_btn.config(text="Tắt sự xinh đẹp khi vào nha!")
            new_config = {
                "isPretty": True,
                "version": "1.0"
            }
        else:
            # Tắt "xinh đẹp"
            self.set_up_btn.config(text="Bật sự xinh đẹp khi vào nè!")
            new_config = {
                "isPretty": False,
                "version": "1.0"
            }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=4, ensure_ascii=False)
    


def open_extra_window(root):
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    extra_win = tk.Toplevel(root)
    extra_win.title("Extra Window")
    extra_win.geometry(f"{int(root.winfo_screenwidth()*0.85)}x{int(root.winfo_screenheight()*0.85)}")
    extra_win.state("zoomed")
    extra_win.configure(bg="#ffe6f0") 
    extra_win.after(15000, extra_win.destroy)

    # Frame để chứa 2 ảnh cạnh nhau
    frame = tk.Frame(extra_win, bg="#ffe6f0")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Ảnh bên trái (vuông bo góc)
    left_img = Image.open(resource_path(os.path.join("public", "img", "image.png"))).resize((int(root.winfo_screenwidth()*0.2), int(root.winfo_screenwidth()*0.2)))
    left_img = round_corners(left_img, radius=50)
    left_tk = ImageTk.PhotoImage(left_img)

    left_frame = tk.Frame(frame, bg="#ffe6f0")
    left_frame.pack(side="left", expand=True, padx=20)
    left_label = tk.Label(left_frame, image=left_tk, bg="#ffe6f0")
    left_label.image = left_tk
    left_label.pack()
    tk.Label(left_frame, text="Tặng hoa để người đẹp nhất vũ trụ bất tử", fg="black", bg="#ffe6f0", font=("Arial", 16)).pack(pady=10)

    # Ảnh bên phải (tròn)
    right_frame = tk.Frame(frame, bg="#ffe6f0")
    right_frame.pack(side="right", expand=True, padx=20)
    
    rainbow = RainbowCircle(
        right_frame,
        resource_path(os.path.join("public", "img", "pretty.png")),
        size=int(root.winfo_screenwidth()*0.3),
        border_width=20,
        bg="#ffe6f0"
    )
    rainbow.pack()
    
    tk.Label(right_frame, text="Ái tà, ai mà xinh thế?? Người đẹp nhất vũ trụ chứ ai!!!", fg="black", bg="#ffe6f0", font=("Arial", 14)).pack(pady=10)

    extra_win.lift()
    extra_win.focus_force()
    extra_win.transient(root)   # luôn nổi trên root
    extra_win.protocol("WM_DELETE_WINDOW", extra_win.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Windrose Data Explorer")
    root.geometry(f"{int(root.winfo_screenwidth()*0.85)}x{int(root.winfo_screenheight()*0.85)}")
    root.state("zoomed")
    # --- tạo canvas có scrollbar bọc toàn bộ ---
    
    main_canvas = tk.Canvas(root,background="black")
    main_canvas.pack(side="left",fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    main_canvas.configure(yscrollcommand=scrollbar.set)

    container = tk.Frame(main_canvas)
    container_id = main_canvas.create_window((0, 0), window=container, anchor="nw")
    
    def on_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfig(container_id, width=event.width)  # ép container luôn full width

    container.bind("<Configure>", on_configure)
    main_canvas.bind("<Configure>", on_configure)  # khi canvas resize thì container cũng resize

    # cuộn bằng con lăn chuột
    def _on_mousewheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    # try:
    #     root.iconbitmap("./icon/icon.png")
    # except:
    #     icon = PhotoImage(file="./icon/icon.png")
    #     root.iconphoto(True, icon)
    if device_name == "R734" and getConfig()==True:
        icon = PhotoImage(file=resource_path(os.path.join("icon", "icon_user.png")))
        root.iconphoto(True, icon)
        open_extra_window(root)
    elif device_name == "Thanh-Laptop" and getConfig()==True:
        icon = PhotoImage(file=resource_path(os.path.join("icon", "icon_user.png")))
        root.iconphoto(True, icon)
        open_extra_window(root)
    else:
        icon = PhotoImage(file=resource_path(os.path.join("icon", "icon.png")))
        root.iconphoto(True, icon)

    app = WindroseGUI(container)

    root.mainloop()