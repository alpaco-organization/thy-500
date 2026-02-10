# 🚀 Air-Gapped Ortamda Podman ile Deployment Kılavuzu

## 🎯 Müşteri Ortam Özellikleri
- ❌ İnternete çıkış YOK
- ✅ Red Hat registry'leri mevcut (registry.access.redhat.com, registry.redhat.io)
- ✅ Podman 5.6.0 kurulu
- ❌ Docker kullanımı yasak

## 📋 Senaryo 1: Red Hat UBI Base Images (ÖNERİLEN)

### Adım 1: Registry Erişimini Test Et
```bash
podman info | grep -A 5 registries
podman pull registry.access.redhat.com/ubi9/python-312:latest --log-level=debug
```

### Adım 2: Podman-Compose ile Başlat
```bash
# podman-compose kurulu değilse
pip3 install podman-compose

# Servisleri başlat
podman-compose -f podman-compose.yml up -d

# Logları izle
podman-compose -f podman-compose.yml logs -f
```

### Adım 3: Kontrol
```bash
podman ps
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 📋 Senaryo 2: Önceden Build Edilmiş Images (Müşteri Registry'si Varsa)

Eğer müşterinin kendi **internal registry'si** varsa:

### İnternete Erişimi Olan Ortamda (Sizin Tarafınızda):
```bash
# Orijinal Dockerfile'ları kullanarak build et
podman build -t thy500-backend:latest -f backend/Dockerfile ./backend
podman build -t thy500-frontend:latest -f frontend/Dockerfile ./frontend

# MongoDB image'ini çek
podman pull docker.io/library/mongo:7

# Image'leri TAR dosyasına aktar
podman save -o thy500-images.tar \
  thy500-backend:latest \
  thy500-frontend:latest \
  mongo:7
```

### Müşteri Ortamında (Air-Gapped):
```bash
# TAR dosyasını yükle
podman load -i thy500-images.tar

# Image'leri listele
podman images

# docker-compose.yml kullanarak başlat (orijinal dosya)
podman-compose -f docker-compose.yml up -d
```

---

## 📋 Senaryo 3: Internal Registry'ye Push

Eğer müşterinin **internal container registry'si** varsa (Harbor, Nexus, vb.):

### Sizin Tarafınızda:
```bash
# Build
podman build -t thy500-backend:latest -f backend/Dockerfile ./backend
podman build -t thy500-frontend:latest -f frontend/Dockerfile ./frontend

# Tag for customer registry
podman tag thy500-backend:latest customer-registry.example.com/thy500/backend:latest
podman tag thy500-frontend:latest customer-registry.example.com/thy500/frontend:latest
podman tag mongo:7 customer-registry.example.com/thy500/mongo:7

# Export to tar
podman save -o images-for-transfer.tar \
  customer-registry.example.com/thy500/backend:latest \
  customer-registry.example.com/thy500/frontend:latest \
  customer-registry.example.com/thy500/mongo:7
```

### Müşteri Ortamında:
```bash
# Load images
podman load -i images-for-transfer.tar

# Push to internal registry (eğer güvenlik politikaları izin veriyorsa)
podman login customer-registry.example.com
podman push customer-registry.example.com/thy500/backend:latest
podman push customer-registry.example.com/thy500/frontend:latest
podman push customer-registry.example.com/thy500/mongo:7
```

Sonra `podman-compose.yml` içinde image adreslerini güncelleyin:
```yaml
services:
  mongo:
    image: customer-registry.example.com/thy500/mongo:7
  backend:
    image: customer-registry.example.com/thy500/backend:latest
  frontend:
    image: customer-registry.example.com/thy500/frontend:latest
```

---

## 🔧 Sorun Giderme

### Problem: Red Hat UBI image'leri çekilemiyor
```bash
# Registry ayarlarını kontrol et
cat /etc/containers/registries.conf

# Manuel çekmeyi dene
podman pull registry.access.redhat.com/ubi9/python-312:latest --tls-verify=false
```

### Problem: MongoDB için Red Hat alternatifi yok
**Çözüm**: MongoDB'yi TAR dosyasıyla transfer edin (Senaryo 2)

### Problem: Permission hatası
```bash
# Rootless mode kontrol
podman unshare chown -R 1001:0 /path/to/volumes
```

### Problem: Build sırasında network hatası
**Çözüm**: Tüm build işlemlerini internete erişimi olan ortamda yapıp TAR olarak transfer edin.

---

## ✅ Hangi Senaryoyu Kullanmalı?

| Durum | Önerilen Senaryo |
|-------|------------------|
| Red Hat registry'lerine erişim var | **Senaryo 1** (UBI images) |
| Internal registry YOK, image transfer gerekli | **Senaryo 2** (TAR transfer) |
| Internal registry var (Harbor/Nexus) | **Senaryo 3** (Registry push) |

---

## 🚨 Önemli Notlar

1. **MongoDB**: Red Hat MongoDB image'i ticari lisansa tabii olabilir. Alternatif olarak TAR ile transfer edin.
2. **Permissions**: UBI image'leri OpenShift uyumlu olduğu için rootless çalışır.
3. **Network**: Air-gapped ortamda build yapmayın, pre-built image kullanın.
4. **Storage**: Podman volumes varsayılan olarak `~/.local/share/containers/storage/volumes/` altında.

---

## 📞 Müşteriye Sorulması Gerekenler

1. ✅ Internal container registry var mı? (Harbor, Nexus, Artifactory)
2. ✅ Red Hat registry'lerine erişim var mı?
3. ✅ MongoDB için mevcut enterprise image var mı?
4. ✅ File transfer yöntemi ne? (USB, secure file transfer, vb.)
5. ✅ Rootless pod çalıştırma izni var mı yoksa root gerekiyor mu?
