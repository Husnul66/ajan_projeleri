# 🤖 Otonom Finans ve Haber Analiz Ajanı (AI-Powered Daily Briefing Agent)

Bu proje; bulut bilişim, Büyük Dil Modeli (LLM) entegrasyonu ve veri kazıma (Web Scraping) yeteneklerini birleştiren uçtan uca (end-to-end) çalışan otonom bir Python mikro-servisidir.

Sistem, GitHub Actions üzerinden sunucusuz (serverless) olarak her sabah otomatik uyanır, güncel piyasa verilerini ve haberleri toplar, yapay zeka ile analiz eder ve yönetici bülteni formatında e-posta olarak gönderir.

## ✨ Özellikler

- **Gerçek Zamanlı Piyasa Verisi:** `yfinance` kullanılarak Dolar, Euro, Afgani kurları ve Gram Altın fiyatlarının anlık ve geriye dönük (hafta sonu korumalı) çekilmesi.
- **Hava Durumu Entegrasyonu:** Open-Meteo API üzerinden anlık sıcaklık ve rüzgar verisi takibi.
- **Yedekli Haber Kazıma (Scraping):** Hata toleranslı mimari ile güncel RSS kaynaklarından `BeautifulSoup` kullanılarak ekonomi manşetlerinin çekilmesi.
- **LLM ile Doğal Dil Üretimi:** Toplanan ham verilerin **Google Gemini 2.5 Flash** modeli ile anlamlı, akıcı ve kişiselleştirilmiş bir sabah bültenine dönüştürülmesi.
- **Otonom İş Akışı (CI/CD):** GitHub Actions (`schedule.yml`) ile belirlenen Cron zamanlamasına göre tam otomatik çalışma.
- **Güvenli İletişim:** Çıktıların SMTP üzerinden iletilmesi ve tüm hassas verilerin GitHub Secrets ile izole edilmesi.

---

## 🚀 Kendi Hesabınızda Nasıl Kullanırsınız? (Sizin İçin Kurulum Rehberi)

Bu ajanın her sabah **size de özel bir bülten göndermesini** isterseniz, sistemi kendi GitHub hesabınızda tamamen ücretsiz ve saniyeler içinde canlıya alabilirsiniz. Hiçbir sunucu kurmanıza veya kod bilmenize gerek yoktur!

**Adım Adım Kurulum:**

1. **Projeyi Kopyalayın (Fork):**
   Sayfanın sağ üst köşesindeki **"Fork"** butonuna tıklayarak bu projeyi kendi GitHub hesabınıza kopyalayın.

2. **Gizli Şifrelerinizi Ekleyin (Secrets):**
   Kendi deponuzda üst menüden **Settings (Ayarlar)** sekmesine gidin. Sol menüden **Secrets and variables > Actions** yolunu izleyin.
   Aşağıdaki 4 adet bilgiyi "New repository secret" butonuna basarak tek tek ekleyin (İsimleri tam olarak aşağıdaki gibi yazmalısınız):
   - `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)'dan alacağınız ücretsiz API anahtarı.
   - `EMAIL_SENDER`: Bülteni gönderecek olan Gmail adresiniz.
   - `EMAIL_PASSWORD`: Gmail hesabınızdan alacağınız 16 haneli "Uygulama Şifresi" (App Password).
   - `EMAIL_RECEIVER`: Bültenin her sabah gelmesini istediğiniz kendi e-posta adresiniz.

3. **Ajanı Uyandırın (GitHub Actions):**
   - Üst menüden ▶️ **Actions** sekmesine tıklayın.
   - GitHub güvenlik gereği "I understand my workflows, go ahead and enable them" butonuna basmanızı isteyebilir, onaylayın.
   - Sol menüden **"Gunluk Bulten Ajani"** iş akışını seçin.
   - Sağ taraftaki **"Run workflow"** butonuna tıklayarak sistemi ilk kez manuel olarak tetikleyin.

🎉 **Tebrikler!** Sistem başarıyla kuruldu. Ajanınız ilk maili birkaç dakika içinde size gönderecek ve artık her gün belirlediğiniz saatte sizin için çalışmaya devam edecektir.

---

## 💻 Geliştiriciler İçin Yerel Kurulum (Local Development)

Projeyi kendi bilgisayarınızda test etmek ve geliştirmek isterseniz:

1. Depoyu klonlayın ve klasöre girin:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/Ajan_Projesi.git](https://github.com/KULLANICI_ADIN/Ajan_Projesi.git)
   cd Ajan_Projesi
