import logging
import os

log_path = "logs/"
if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_path}/api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)