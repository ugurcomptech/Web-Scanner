import os
import re
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# ANSI Renk Kodları
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Tarama yapılacak dizin ve log dosyası
SCAN_DIR = "/www/wwwroot/"
LOG_FILE = "/var/log/malware_scan.log"
APACHE_VHOST_DIR = "/www/server/panel/vhost/apache/"
APACHE_SERVICE = "httpd.service"

SUSPICIOUS_PATTERNS = {
    r"base64_decode\s*\(": "Base64 ile şifrelenmiş kod",
    r"eval\s*\(": "Eval ile çalıştırılabilir kötü amaçlı kod",
    r"shell_exec\s*\(": "Sistem komutlarını çalıştıran fonksiyon",
    r"system\s*\(": "Sistem komutu çalıştırma",
    r"exec\s*\(": "Komut çalıştırma",
    r"subprocess\.Popen": "Python ile sistem komut çalıştırma",
    r"document\.write\(atob": "JS ile Base64 gizlenmiş kod",
    r'"base64_decode"\s*\(': "Base64 fonksiyonunun gizlenmiş kullanımı",
    r'"ev"\s*\.\s*"al"\s*\(': "Eval fonksiyonunun gizlenmiş kullanımı",
    r"\$\w+\s*=\s*[\"']ZXZhbCg[a-zA-Z0-9+/=]+[\"']": "Base64 içinde eval şifrelemesi"
}


def log_event(message, color=RESET):
    """ Log dosyasına olay kaydeder ve ekrana renkli basar. """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(f"{color}{log_entry}{RESET}")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry + "\n")


def disable_vhost(file_path):
    """ Şüpheli dosyanın bulunduğu siteyi devre dışı bırakır. """
    domain = file_path.split("/")[3]  # Örneğin: /www/wwwroot/site.com/index.php
    vhost_conf = os.path.join(APACHE_VHOST_DIR, f"{domain}.conf")
    disabled_conf = vhost_conf + ".disabled"

    if os.path.exists(vhost_conf):
        shutil.move(vhost_conf, disabled_conf)
        log_event(f"🚫 {domain} için Apache vhost devre dışı bırakıldı!", RED)
        restart_apache()
    else:
        log_event(f"⚠️ {domain} için vhost yapılandırması bulunamadı.", YELLOW)


def restart_apache():
    """ Apache servisini yeniden başlatır. """
    log_event("🔄 Apache servisi yeniden başlatılıyor...", BLUE)
    os.system(f"systemctl restart {APACHE_SERVICE}")
    log_event("✅ Apache servisi yeniden başlatıldı!", GREEN)


def scan_file(file_path):
    """ Belirtilen dosyada şüpheli kodları tarar. """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            file_suspicions = []
            for pattern, desc in SUSPICIOUS_PATTERNS.items():
                if re.search(pattern, content):
                    file_suspicions.append(f"  - {YELLOW}{desc}{RESET} → {BLUE}{pattern}{RESET}")

            if file_suspicions:
                log_event(f"⚠️ Şüpheli dosya tespit edildi: {file_path}", RED)
                for detail in file_suspicions:
                    print(detail)
                    log_event(detail.replace(YELLOW, "").replace(RED, "").replace(BLUE, "").replace(RESET, ""))
                disable_vhost(file_path)
    except Exception as e:
        log_event(f"[!] {file_path} okunurken hata oluştu: {e}", RED)


class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            log_event(f"⚠️ Dosya Değiştirildi: {event.src_path}", YELLOW)
            scan_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            log_event(f"🚨 Yeni Dosya Eklendi: {event.src_path}", YELLOW)
            scan_file(event.src_path)


def start_monitoring():
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=SCAN_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    log_event("🔍 Başlangıç taraması yapılıyor...", BLUE)
    for root, _, files in os.walk(SCAN_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith((".php", ".js", ".py", ".html", ".htaccess")):
                scan_file(file_path)
    log_event("📡 Gerçek zamanlı izleme başlatılıyor...", GREEN)
    start_monitoring()
