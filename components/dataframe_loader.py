import pandas as pd
from tkinter import ttk, filedialog, messagebox


class DataFrameLoader:
    def __init__(self, parent):
        self.parent = parent
        self.df = None

        # Frame trên: chọn file + hiển thị dữ liệu
        self.frame = ttk.Frame(parent.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_btn = ttk.Button(self.frame, text="Load File", command=self.load_file)
        self.load_btn.pack(anchor="w")

        self.tree = ttk.Treeview(self.frame, show="headings")
        self.tree.pack(fill="both", expand=True)

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

            # Update treeview
            self.update_tree()
            self.parent.on_data_loaded(self.df)

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