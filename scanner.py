import os
import re
from logger import log_event, GREEN, YELLOW, RED
from config import SUSPICIOUS_PATTERNS, APACHE_VHOST_DIR, APACHE_SERVICE

# Renk kodları eksik olduğu için ekleniyor
RESET = "\033[0m"
BLUE = "\033[94m"

def scan_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            file_suspicions = []
            
            for pattern, desc in SUSPICIOUS_PATTERNS.items():
                if re.search(pattern, content, re.IGNORECASE):
                    file_suspicions.append(f"  - {YELLOW}{desc}{RESET} → {BLUE}{pattern}{RESET}")
            
            if file_suspicions:
                log_event(f"⚠️ Şüpheli dosya tespit edildi: {file_path}", YELLOW)
                for suspicion in file_suspicions:
                    log_event(suspicion, YELLOW)
                
                domain = extract_domain(file_path)
                if domain:
                    handle_suspicious_vhost(domain)
    except Exception as e:
        log_event(f"[!] {file_path} okunurken hata oluştu: {e}", RED)

def extract_domain(file_path):
    match = re.search(r"/www/wwwroot/([^/]+)/", file_path)
    return match.group(1) if match else None

def handle_suspicious_vhost(domain):
    vhost_path = os.path.join(APACHE_VHOST_DIR, f"{domain}.conf")
    vhost_disabled_path = os.path.join(APACHE_VHOST_DIR, f"{domain}.conf.disabled")
    
    if os.path.exists(vhost_disabled_path):
        log_event(f"⚠️ {domain} için vhost yapılandırması askıya alınmış.", YELLOW)
    elif not os.path.exists(vhost_path):
        log_event(f"⚠️ {domain} için vhost yapılandırması bulunamadı.", YELLOW)
    else:
        os.rename(vhost_path, vhost_disabled_path)
        log_event(f"🚫 {domain} için Apache vhost devre dışı bırakıldı!", RED)
        restart_apache()

def restart_apache():
    log_event("🔄 Apache servisi yeniden başlatılıyor...", GREEN)
    os.system(f"systemctl restart {APACHE_SERVICE}")

def scan_all_sites():
    root_dir = "/www/wwwroot/"
    
    for site in os.listdir(root_dir):
        site_path = os.path.join(root_dir, site)
        if os.path.isdir(site_path):
            for root, _, files in os.walk(site_path):
                for file in files:
                    scan_file(os.path.join(root, file))

if __name__ == "__main__":
    log_event("🔍 Başlangıç taraması yapılıyor...", GREEN)
    scan_all_sites()
    log_event("📡 Gerçek zamanlı izleme başlatılıyor...", GREEN)
