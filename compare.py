import pandas as pd

all_df = pd.read_csv("wind_non_calm_lib.csv")
non_df = pd.read_csv("wind_non_calm.csv")

print("Tổng mẫu all:", len(all_df))
print("Tổng mẫu non-calm:", len(non_df))

# So sánh tần suất theo hướng
all_counts = all_df.groupby("dir")["spd"].count()
non_counts = non_df.groupby("dir")["spd"].count()

diff = pd.DataFrame({
    "all": all_counts,
    "non_calm": non_counts
}).fillna(0)

diff["chênh lệch"] = diff["all"] - diff["non_calm"]
print(diff)
