import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_wind_rose_qnkt(
    excel_path: str,
    sheet_name: str = "Sheet1",
    year: int = 2005,
    speed_bins = (0, 2, 4, 6, 8, 10, 100),
    percent: bool = False,
    save_path: str = None,
):
    """
    Vẽ hoa gió 16 hướng cho dữ liệu QNKT.xlsx.
    - Quy ước: cột 'Hướng x' lưu theo thang 10° (cần nhân *10 để ra độ).
    - Chia 16 hướng chuẩn: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW.
    - Các thanh được xếp chồng theo các cấp gió (m/s).

    Tham số:
        excel_path: đường dẫn tới file Excel (ví dụ: '/mnt/data/QNKT.xlsx')
        sheet_name: tên sheet (mặc định 'Sheet1')
        year      : năm cần vẽ (mặc định 2005)
        speed_bins: ngưỡng m/s để phân loại cấp gió
        percent   : True → hiển thị theo %; False → số đếm
        save_path : nếu đặt, sẽ lưu hình ra đường dẫn này
    """
    # Đọc & lọc dữ liệu
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df = df[df["Năm"] == year].copy()

    # Gom cặp cột Hướng_i & V_i, nhân Hướng * 10°
    wind_parts = []
    for col in df.columns:
        if isinstance(col, str) and col.startswith("Hướng "):
            idx = col.split(" ")[-1]          # '1','7','13','19',...
            dir_col = col
            spd_col = f"V{idx}"
            if spd_col in df.columns:
                part = df[[dir_col, spd_col]].rename(columns={dir_col: "dir", spd_col: "spd"})
                part["dir"] = part["dir"] * 10
                wind_parts.append(part)

    if not wind_parts:
        raise ValueError("Không tìm thấy cặp cột 'Hướng x' và 'Vx' trong sheet.")

    wind_df = pd.concat(wind_parts, ignore_index=True)
    wind_df = wind_df[(wind_df["spd"] > 0) & wind_df["dir"].notna()]

    # 16 hướng chuẩn
    labels_dir = ["N", "NNE", "NE", "ENE",
                  "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW",
                  "W", "WNW", "NW", "NNW"]
    num_dir = 16
    bins_dir = np.linspace(0, 360, num_dir + 1)

    # Cấp gió (m/s)
    speed_bins = tuple(speed_bins)
    speed_labels = [f"{int(speed_bins[i])}-{int(speed_bins[i+1])}" if i < len(speed_bins)-2 else f">{int(speed_bins[i])}"
                    for i in range(len(speed_bins)-1)]
    wind_df["spd_cat"] = pd.cut(wind_df["spd"], bins=speed_bins, labels=speed_labels, right=False, include_lowest=True)
    wind_df["dir_sector"] = pd.cut(wind_df["dir"], bins=bins_dir, labels=labels_dir, right=False, include_lowest=True)

    # Bảng tần suất (hướng × cấp gió)
    freq = wind_df.pivot_table(index="dir_sector", columns="spd_cat", values="spd", aggfunc="count", fill_value=0)
    freq = freq.reindex(labels_dir, fill_value=0)           # đảm bảo đủ 16 hướng
    for lab in speed_labels:                                # đảm bảo đủ cột cấp gió
        if lab not in freq.columns:
            freq[lab] = 0
    freq = freq[speed_labels]

    if percent:
        total = freq.to_numpy().sum()
        if total > 0:
            freq = freq * 100.0 / total

    # Vẽ polar bar chart (xếp chồng) – không set màu thủ công
    angles = np.deg2rad(np.linspace(0, 360, num_dir, endpoint=False))
    width = 2 * np.pi / num_dir

    fig = plt.figure(figsize=(9, 9))
    ax = plt.subplot(111, polar=True)

    bottom = np.zeros(len(freq))
    for lab in speed_labels:
        values = freq[lab].to_numpy()
        ax.bar(angles, values, width=width, bottom=bottom, align="center", label=lab)
        bottom += values

    ax.set_theta_zero_location("N")   # Bắc ở trên
    ax.set_theta_direction(-1)        # xoay chiều kim đồng hồ
    ax.set_xticks(angles)
    ax.set_xticklabels(labels_dir)

    unit = "%" if percent else "counts"
    ax.set_title(f"Hoa gió 16 hướng - Năm {year} (đã nhân hướng ×10°) [{unit}]", va="bottom")
    ax.legend(title="Cấp gió (m/s)", bbox_to_anchor=(1.15, 1.05))

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=160)
    return fig, ax, freq

# Ví dụ chạy nhanh:
fig, ax, freq = plot_wind_rose_qnkt(
    excel_path="QNKT.xls",
    sheet_name="Sheet1",
    year=2005,
    speed_bins=(0, 2, 4, 6, 8, 10, 100),
    percent=False,
    save_path="wind_rose_2005.png"
)
print(freq)