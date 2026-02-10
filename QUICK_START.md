# 🎯 Hızlı Başlangıç - Air-Gapped Deployment

## ✅ Docker → Podman Uyumluluğu

**Endişelenme!** Docker ile build edilen image'ler Podman ile **%100 uyumludur**.

```
[Mac/Docker Build] → [TAR] → [Transfer] → [Müşteri/Podman Load] ✅
```

---

## 🚀 3 Adımda Deployment

### 1️⃣ Mac'inde Build Et (15-20 dk)
```bash
cd /Users/oguzhanigrek/Downloads/thy-500-main
./build-and-export-docker.sh
```

**Oluşur:** `thy500-images.tar` (~2.5-3 GB)

---

### 2️⃣ Müşteriye Transfer Et (USB/Disk)
**Dosyalar:**
- `thy500-images.tar` (2.5-3 GB)
- `docker-compose.yml`
- `load-and-deploy.sh`

---

### 3️⃣ Müşteri Ortamında Kaldır (5-8 dk)
```bash
# .env dosyası oluştur (AWS credentials, JWT secret, vb.)
nano .env

# Deploy et
./load-and-deploy.sh

# Kontrol et
podman ps
curl http://localhost:3000  # Frontend
curl http://localhost:8000  # Backend
```

---

## 📚 Detaylı Kılavuz

**Tüm detaylar için:** [`AIR_GAPPED_DEPLOYMENT.md`](AIR_GAPPED_DEPLOYMENT.md)

---

## 🔧 Manuel Komutlar

### Build (Mac):
```bash
docker build --platform linux/amd64 -t thy500-backend:latest -f backend/Dockerfile ./backend
docker build --platform linux/amd64 -t thy500-frontend:latest -f frontend/Dockerfile ./frontend
docker pull --platform linux/amd64 mongo:7
docker save -o thy500-images.tar thy500-backend:latest thy500-frontend:latest mongo:7
```

### Load (Müşteri):
```bash
podman load -i thy500-images.tar
podman images  # Image'leri kontrol et
podman-compose -f docker-compose.yml up -d
```

---

## ❓ SSS

**S: Docker ile build, Podman ile çalışır mı?**  
✅ **Evet!** Her ikisi de OCI standardını kullanır.

**S: İnternete erişim olmadan nasıl çalışacak?**  
✅ TAR dosyası tüm image'leri içerir, internet gerekmez.

**S: x86_64 uyumluluğu var mı?**  
✅ `--platform linux/amd64` ile build edildi.

---

## 🎬 Şimdi Ne Yapmalısın?

1. ✅ `./build-and-export-docker.sh` çalıştır (Mac'inde)
2. ⏳ 15-20 dakika bekle
3. 📦 `thy500-images.tar` dosyasını USB'ye kopyala
4. 🚚 Müşteriye transfer et
5. 🚀 Müşteri ortamında `./load-and-deploy.sh` çalıştır

**Detaylar:** `AIR_GAPPED_DEPLOYMENT.md` dosyasını oku! 📖
