import os
import json

def getConfigPath():
    """
    Lấy đường dẫn file config trong AppData.
    Ví dụ: C:\Users\<User>\AppData\Roaming\windrose_app\config.json
    """
    appdata = os.getenv("APPDATA")  # Thư mục AppData\Roaming
    config_dir = os.path.join(appdata, "windrose_app")
    os.makedirs(config_dir, exist_ok=True)  # đảm bảo thư mục tồn tại
    return os.path.join(config_dir, "config.json")

def getConfig():
    config_path = getConfigPath()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("isPretty", False)  # ✅ chỉ trả về True/False
        except json.JSONDecodeError:
            print("⚠️ File config.json bị hỏng hoặc sai định dạng.")
            return False
    else:
        return initConfig()

def initConfig():
    """Tạo file config mặc định nếu chưa tồn tại"""
    config_path = getConfigPath()
    default_config = {
        "isPretty": False,
        "version": "1.0"
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    return default_config["isPretty"]