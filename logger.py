# logger.py
from datetime import datetime
from config import LOG_FILE
from config import YELLOW, RED, GREEN, BLUE, RESET

# ANSI Renk Kodları
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def log_event(message, color=RESET):
    """ Log dosyasına olay kaydeder ve ekrana renkli basar. """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(f"{color}{log_entry}{RESET}")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry + "\n")
