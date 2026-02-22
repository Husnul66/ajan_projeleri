# 🤖 Otonom Finans ve Haber Analiz Ajanı (AI-Powered Daily Briefing Agent)

Bu proje; bulut bilişim, Büyük Dil Modeli (LLM) entegrasyonu ve veri kazıma (Web Scraping) yeteneklerini birleştiren uçtan uca (end-to-end) çalışan otonom bir Python mikro-servisidir.

Sistem, GitHub Actions üzerinden sunucusuz (serverless) olarak her sabah otomatik uyanır, güncel piyasa verilerini ve haberleri toplar, yapay zeka ile analiz eder ve yönetici bülteni formatında e-posta olarak gönderir.

## ✨ Özellikler

- **Gerçek Zamanlı Piyasa Verisi:** `yfinance` kullanılarak Dolar, Euro, Afgani kurları ve Gram Altın fiyatlarının anlık ve geriye dönük (hafta sonu korumalı) çekilmesi.
- **Hava Durumu Entegrasyonu:** Open-Meteo API üzerinden Elazığ koordinatları (38.6743, 39.2232) kullanılarak anlık sıcaklık ve rüzgar verisi takibi.
- **Yedekli Haber Kazıma (Scraping):** Hata toleranslı (Fallback) mimari ile güncel RSS kaynaklarından `BeautifulSoup` kullanılarak ekonomi manşetlerinin çekilmesi.
- **LLM ile Doğal Dil Üretimi:** Toplanan ham sayısal verilerin **Google Gemini 2.5 Flash** modeli ile anlamlı, akıcı ve kişiselleştirilmiş bir sabah bültenine dönüştürülmesi.
- **Otonom İş Akışı (CI/CD):** GitHub Actions (`schedule.yml`) ile belirlenen Cron zamanlamasına göre tam otomatik çalışma.
- **Güvenli İletişim:** Çıktıların SMTP protokolü üzerinden e-posta ile iletilmesi ve tüm hassas verilerin GitHub Secrets ile izole edilmesi.

## 🛠️ Kullanılan Teknolojiler (Tech Stack)

- **Programlama Dili:** Python 3.12+
- **Yapay Zeka:** `google-genai` (Gemini 2.5 Flash SDK)
- **Veri & Scraping:** `yfinance`, `BeautifulSoup4`, `requests`
- **DevOps & Otomasyon:** GitHub Actions (YAML)
- **Ağ & İletişim:** `smtplib`, `email.mime`

## 🚀 Kurulum ve Yerel Çalıştırma (Local Development)

Projeyi kendi bilgisayarınızda test etmek için aşağıdaki adımları izleyebilirsiniz:

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/Ajan_Projesi.git](https://github.com/KULLANICI_ADIN/Ajan_Projesi.git)
   cd Ajan_Projesi
