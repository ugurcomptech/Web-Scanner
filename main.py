import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger import log_event, GREEN, YELLOW, RED
from scanner import scan_file
from config import SCAN_DIR

EXCLUDE_EXTENSIONS = [".swp", ".tmp", ".log"]

class FileChangeHandler(FileSystemEventHandler):
    """ Dosya değişikliklerini izler ve tarama başlatır. """

    def on_created(self, event):
        if not event.is_directory and not any(event.src_path.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
            log_event(f"🚨 Yeni Dosya Eklendi: {event.src_path}", YELLOW)
            scan_file(event.src_path)  # Dosya oluşturulduğunda tara

    def on_modified(self, event):
        if not event.is_directory and not any(event.src_path.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
            log_event(f"⚠️ Dosya Değiştirildi: {event.src_path}", RED)
            scan_file(event.src_path)  # Dosya değiştiğinde tekrar tara

def start_monitoring(directory):
    """ Belirtilen klasörde gerçek zamanlı izleme başlatır. """
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    log_event("🔍 Başlangıç taraması yapılıyor...", GREEN)
    
    for root, _, files in os.walk(SCAN_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith((".php", ".js", ".py", ".rb", ".pl", ".html", ".htaccess")):
                scan_file(file_path)
    
    log_event("📡 Gerçek zamanlı izleme başlatılıyor...", GREEN)
    start_monitoring(SCAN_DIR)
