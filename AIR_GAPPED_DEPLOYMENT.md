# 🚀 Air-Gapped Deployment - Adım Adım Kılavuz

## 📍 Senaryo: İntel x86_64 Sunucu → Air-Gapped Müşteri Ortamı

---

## 1️⃣ Intel Sunucuda (İnternete Erişimli - x86_64)

### Adım 1: Projeyi Transfer Et
```bash
# Projeyi intel sunucuya kopyala
cd /path/to/thy-500-main
```

### Adım 2: Script'i Çalıştırılabilir Yap
```bash
chmod +x build-and-export.sh
```

### Adım 3: Build ve Export İşlemini Başlat
```bash
./build-and-export.sh
```

**Bu script:**
- ✅ Backend image'ini build eder (x86_64)
- ✅ Frontend image'ini build eder (x86_64)
- ✅ MongoDB:7 image'ini çeker
- ✅ Hepsini `thy500-images.tar` dosyasına kaydeder

**Beklenen çıktı boyutu:** ~2-3 GB TAR dosyası

### Adım 4: Transfer İçin Dosyaları Hazırla
```bash
# Transfer edilecek dosyalar
ls -lh thy500-images.tar
ls -lh docker-compose.yml
ls -lh .env  # eğer varsa
ls -lh load-and-deploy.sh
```

---

## 2️⃣ Müşteri Ortamına Transfer (Air-Gapped - x86_64)

### Transfer Yöntemleri:
- 📀 USB flash disk
- 💾 External hard drive
- 🔐 Secure file transfer (SCP/SFTP eğer internal network varsa)
- 📦 Physical media

### Transfer Edilmesi Gerekenler:
```bash
thy500-images.tar          # ~2-3 GB
docker-compose.yml         # Compose config
load-and-deploy.sh         # Deployment script
.env                       # Environment variables (oluşturulacak)
```

---

## 3️⃣ Müşteri Ortamında (Air-Gapped - Podman 5.6.0)

### Adım 1: Dosyaları Kontrol Et
```bash
cd /path/to/transferred/files
ls -lh

# Beklenen dosyalar:
# - thy500-images.tar
# - docker-compose.yml
# - load-and-deploy.sh
```

### Adım 2: .env Dosyası Oluştur (Eğer Yoksa)
```bash
cat > .env << 'EOF'
# AWS Credentials
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=eu-north-1
S3_BUCKET=your-s3-bucket-name
S3_PREFIX=thy500/

# JWT Configuration
JWT_SECRET_KEY=super-secret-key-minimum-32-characters-long-please
JWT_ALGORITHM=HS256

# Admin Credentials
ADMIN_EMAIL=admin@thy500.local
ADMIN_PASSWORD=SecurePassword123!

# Token Settings
ACCESS_TOKEN_EXPIRE_MINUTES=30
PRESIGN_EXPIRES_SECONDS=900
EOF
```

### Adım 3: Script'i Çalıştırılabilir Yap
```bash
chmod +x load-and-deploy.sh
```

### Adım 4: Deploy Et
```bash
./load-and-deploy.sh
```

**Bu script:**
- ✅ TAR dosyasından image'leri yükler
- ✅ .env dosyasını kontrol eder
- ✅ podman-compose'u kurar (eğer yoksa)
- ✅ Servisleri başlatır

### Adım 5: Deployment Doğrula
```bash
# Container'ları kontrol et
podman ps

# Logları izle
podman-compose -f docker-compose.yml logs -f

# Health check
curl http://localhost:8000/health   # Backend
curl http://localhost:3000          # Frontend
```

---

## 🔧 Manuel Komutlar (İsteğe Bağlı)

### Intel Sunucuda (Build):
```bash
# Manuel build - Backend
podman build --platform linux/amd64 \
  -t thy500-backend:latest \
  -f backend/Dockerfile \
  ./backend

# Manuel build - Frontend
podman build --platform linux/amd64 \
  -t thy500-frontend:latest \
  -f frontend/Dockerfile \
  ./frontend

# MongoDB pull
podman pull --platform linux/amd64 docker.io/library/mongo:7

# Export to TAR
podman save -o thy500-images.tar \
  thy500-backend:latest \
  thy500-frontend:latest \
  mongo:7
```

### Müşteri Ortamında (Load):
```bash
# Manuel load
podman load -i thy500-images.tar

# Image'leri listele
podman images

# Manuel deployment
podman-compose -f docker-compose.yml up -d

# Logları izle
podman-compose logs -f backend
podman-compose logs -f frontend
podman-compose logs -f mongo
```

---

## 🚨 Sorun Giderme

### Problem: TAR dosyası çok büyük
**Çözüm:**
```bash
# Sıkıştırılmış TAR
gzip thy500-images.tar
# Transfer et: thy500-images.tar.gz
# Müşteri tarafında: gunzip thy500-images.tar.gz
```

### Problem: podman-compose bulunamadı
**Çözüm:**
```bash
# Python3 pip ile kur
pip3 install --user podman-compose

# Veya yum/dnf ile
sudo dnf install podman-compose -y
```

### Problem: Permission denied hatası
**Çözüm:**
```bash
# Rootless mode kontrol
podman unshare chown -R 1001:0 /var/lib/containers/storage/volumes

# Veya rootless reset
podman system reset
```

### Problem: Container başlamıyor
**Çözüm:**
```bash
# Detaylı log
podman logs thy500-backend --tail 100
podman logs thy500-frontend --tail 100

# Container inspect
podman inspect thy500-backend

# Network kontrol
podman network ls
```

### Problem: MongoDB connection error
**Çözüm:**
```bash
# MongoDB loglarını kontrol et
podman logs thy500-mongo

# MongoDB'ye bağlan
podman exec -it thy500-mongo mongosh
```

---

## 📋 Kontrol Listesi

### Intel Sunucuda (Build Tarafı):
- [ ] Podman kurulu
- [ ] İnternete erişim var
- [ ] Yeterli disk alanı (10+ GB)
- [ ] `build-and-export.sh` çalıştırıldı
- [ ] `thy500-images.tar` oluşturuldu (~2-3 GB)

### Transfer:
- [ ] `thy500-images.tar` transfer edildi
- [ ] `docker-compose.yml` transfer edildi
- [ ] `load-and-deploy.sh` transfer edildi
- [ ] `.env` dosyası hazırlandı

### Müşteri Ortamında (Deploy Tarafı):
- [ ] Podman 5.6.0 kurulu
- [ ] `podman-compose` kuruldu
- [ ] `.env` dosyası doğru değerlerle dolduruldu
- [ ] `load-and-deploy.sh` çalıştırıldı
- [ ] Container'lar çalışıyor (`podman ps`)
- [ ] Frontend erişilebilir (port 3000)
- [ ] Backend erişilebilir (port 8000)

---

## ⏱️ Tahmini Süreler

| İşlem | Süre |
|-------|------|
| Intel sunucuda build | 10-15 dakika |
| TAR export | 2-5 dakika |
| Transfer (USB) | 5-10 dakika* |
| Müşteri ortamında load | 2-5 dakika |
| Deployment | 1-2 dakika |
| **TOPLAM** | **~20-35 dakika** |

*Internet hızına/transfer ortamına bağlı

---

## 📞 Destek

Sorun yaşarsan:
1. `podman ps -a` çıktısını kontrol et
2. `podman logs <container-name>` ile logları incele
3. `.env` dosyasındaki değerleri doğrula
4. Network bağlantılarını test et
