# config.py
import os

# Tarama yapılacak dizin ve log dosyası
SCAN_DIR = "/www/wwwroot/"
LOG_FILE = "/var/log/malware_scan.log"
APACHE_VHOST_DIR = "/www/server/panel/vhost/apache/"
APACHE_SERVICE = "httpd.service"

# ANSI Renk Kodları
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"


# Şüpheli kod kalıpları

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
