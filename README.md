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

### Örnek Çıktılar

Eğer site askıya alınmışsa aşağıdaki gibi askıya alındığına dair uyarı vermektedir. 

![image](https://github.com/user-attachments/assets/ca33a698-0d53-4613-9752-9e68938d5389)

Yeni bir dosya eklendiği zaman aşağıdaki gibi dosyayı tarayıp içerisinde eğer zararlı bir kod var ise göstermektedir.

![image](https://github.com/user-attachments/assets/c3976495-13bf-4d5f-ac11-a02038aa38fb)

Dosyanın içeriği değiştirildiği zaman ve içinde herhangi bir zararlı kod var ise aşağıdaki gibi göstermektedir.

![image](https://github.com/user-attachments/assets/3e38599c-75d5-4868-a4cd-ed77085faa42)


Eğer bir `systemd` servisi olarak çalıştırmak isterseniz:
```bash
sudo cp scanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable scanner.service
sudo systemctl start scanner.service
```

## Not

Scriptlerde yazılan dosya yolları örnek olarak yazılmıştır. Kendi sunucunuza göre yapılandırmanız gerekmektedir.

## 📄 Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.

---


