import pandas as pd

class DataManager:
    def __init__(self):
        self.df = None

    def load_file(self, file_path):
        if file_path.endswith(".csv"):
            self.df = pd.read_csv(file_path)
        else:
            self.df = pd.read_excel(file_path)
        return self.df

    def detect_direction_speed_columns(self, columns):
        direction_keywords = ["direction", "hướng", "dir"]
        speed_keywords = ["speed", "vận tốc", "v", "spd"]
        direction_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in direction_keywords) or col.lower().startswith("hướng")]
        speed_cols = [col for col in columns if any(
            kw.lower() in col.lower() for kw in speed_keywords) or col.lower().startswith("v")]
        return direction_cols, speed_cols

    def apply_filters(self, filters):
        filtered_df = self.df.copy()
        filter_dict = {}
        for f in filters:
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