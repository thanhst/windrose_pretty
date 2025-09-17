import pandas as pd
from tkinter import ttk, filedialog, messagebox

class DataFrameLoader:
    def __init__(self, parent, tree, WindComponent, SpeedComponent):
        self.parent = parent
        self.df = None
        self.tree=tree
        self.WindComponent=WindComponent
        self.SpeedComponent=SpeedComponent

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
            
            self.detect_direction_speed_columns(cols)
            self.update_direction_speed()
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
            
    def detect_direction_speed_columns(self, columns):
        direction_keywords = ["direction", "hướng", "dir"]
        speed_keywords = ["speed", "vận tốc", "v", "spd"]

        direction_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in direction_keywords) or col.lower().startswith("hướng")]
        speed_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in speed_keywords) or col.lower().startswith("v")]

        return direction_cols, speed_cols
    
    def update_direction_speed(self):
        direction_cols, speed_cols = self.detect_direction_speed_columns(list(self.df.columns))
        for d in direction_cols:
            self.WindComponent.add_wind_item(d)
        for s in speed_cols:
            self.SpeedComponent.add_speed_item(s)