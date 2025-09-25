import logging
import os

def setup_logging(app_name="windrose_app"):
    log_dir = os.path.join(os.getenv("APPDATA"), app_name)
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")
    
    logging.basicConfig(
        level=logging.DEBUG,            
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename=log_path,
        filemode="a",
        encoding="utf-8"
    )
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    logging.info(f"Logging initialized. Log file: {log_path}")
    return logging.getLogger(app_name)
