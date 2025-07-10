# AI Destekli Kurs Platformu

Django ve Google Gemini AI kullanılarak geliştirilmiş, otomatik kurs içeriği oluşturan bir web platformu.

## Özellikler

- Yapay zeka destekli otomatik içerik üretimi
- Responsive tasarım
- Admin paneli üzerinden içerik yönetimi
- SEO dostu URL yapısı
- Güvenli kimlik doğrulama sistemi

## Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/shzany/AI-Destekli-Kurs-Platformu-Python-Django.git
cd AI-Destekli-Kurs-Platformu-Python-Django
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. .env dosyasını oluşturun:
- .env.example dosyasını .env olarak kopyalayın
- Gerekli değişkenleri kendi değerlerinizle güncelleyin

5. Veritabanı migrasyonlarını yapın:
```bash
python manage.py migrate
```

6. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

## Çevre Değişkenleri

Projenin çalışması için aşağıdaki çevre değişkenlerinin .env dosyasında tanımlanması gerekir:

- SECRET_KEY: Django güvenlik anahtarı
- DEBUG: Geliştirme modu (True/False)
- ALLOWED_HOSTS: İzin verilen host adresleri
- YOUR_API_KEY: Google Gemini AI API anahtarı
- DATABASE_URL: Veritabanı bağlantı URL'i

## Teknolojiler

- Django 4.2+
- Google Gemini AI
- SQLite
- Bootstrap
- Prism.js

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
