# Scanner Script

Scanner Script, belirlenen dizinlerdeki web dosyalarını tarayarak şüpheli içerikleri tespit eden bir güvenlik aracıdır. Tespit edilen şüpheli dosyalarla ilişkili vhost konfigürasyonlarını devre dışı bırakabilir ve Apache servisini yeniden başlatabilir.

## Özellikler
- **Otomatik Dosya Taraması**: Belirtilen dizinlerdeki `.js`, `.php`, `.sh` ve diğer önemli dosyaları inceler.
- **Regex Destekli İçerik Tespiti**: Tanımlanan şüpheli içerik desenlerine göre dosyaları analiz eder.
- **Apache Vhost Yönetimi**: Şüpheli dosya tespit edildiğinde ilgili vhost dosyasını devre dışı bırakır.
- **Gerçek Zamanlı İzleme**: Dosya taramaları belirli aralıklarla çalıştırılarak sürekli güvenlik kontrolü sağlar.

##  Kurulum
1. **Gerekli bağımlılıkları yükleyin:**
   ```bash
   sudo apt update && sudo apt install python3
   ```
2. **Projeyi klonlayın:**
   ```bash
   https://github.com/ugurcomptech/Web-Scanner.git
   cd Web-Scanner
   ```
3. **Config Dosyasını Düzenleyin**
   `config.py` dosyasını açarak şüpheli içerik regex'lerini ve Apache ayarlarını yapılandırın.

## Kullanım
Scripti manuel olarak çalıştırabilirsiniz:
```bash
python3 main.py
```

Eğer bir `systemd` servisi olarak çalıştırmak isterseniz:
```bash
sudo cp scanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable scanner.service
sudo systemctl start scanner.service
```

## 📄 Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.

---


