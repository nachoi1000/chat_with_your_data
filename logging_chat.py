import logging.config
import time
from pathlib import Path
import os

timestr = time.strftime("%Y%m%d_%H%M")


log_dir = Path(os.getcwd(), "logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_path = str(Path(log_dir, f"squaid_{timestr}.log"))

simple_formatter = logging.Formatter('%(asctime)s - %(message)s')
verbose_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(verbose_formatter)

file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(simple_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)