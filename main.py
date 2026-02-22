import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

import requests
import yfinance as yf
from bs4 import BeautifulSoup
from google import genai

# Profesyonel Loglama Yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BriefingAgent")

class DailyBriefingAgent:
    """Günlük finans, haber ve hava durumu verilerini toplayıp AI ile özetleyen otonom ajan."""

    def __init__(self):
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.email_sender = os.environ.get("EMAIL_SENDER")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.email_receiver = os.environ.get("EMAIL_RECEIVER")
        
        if not all([self.gemini_api_key, self.email_sender, self.email_password, self.email_receiver]):
            logger.error("Kritik ortam değişkenleri (Environment Variables) eksik!")
            raise ValueError("Sistem başlatılamadı: Eksik yapılandırma.")

        self.client = genai.Client(api_key=self.gemini_api_key)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/120.0.0.0'}

    def fetch_market_data(self) -> Dict[str, str]:
        """Yahoo Finance üzerinden altın ve döviz verilerini (Hafta sonu korumalı) çeker."""
        logger.info("Piyasa verileri çekiliyor...")
        try:
            # period="5d" ile hafta sonu piyasa kapalıysa Cuma gününün verisini alır
            usd_try = yf.Ticker("TRY=X").history(period="5d")['Close'].iloc[-1]
            eur_try = yf.Ticker("EURTRY=X").history(period="5d")['Close'].iloc[-1]
            
            # Afgani Hesabı (Dolar/Afgani kurunu, Dolar/TL kuruna bölüyoruz)
            usd_afn = yf.Ticker("AFN=X").history(period="5d")['Close'].iloc[-1]
            try_afn = usd_afn / usd_try
            
            gold_oz_usd = yf.Ticker("GC=F").history(period="5d")['Close'].iloc[-1]
            gram_altin_try = (gold_oz_usd / 31.1034768) * usd_try
            
            return {
                "Gram_Altin": f"{gram_altin_try:.2f}", 
                "USD_TRY": f"{usd_try:.2f}",
                "EUR_TRY": f"{eur_try:.2f}",
                "TRY_AFN": f"{try_afn:.2f}"
            }
        except Exception as e:
            logger.error(f"Piyasa verisi alınırken hata: {e}")
            return {"Gram_Altin": "Veri Yok", "USD_TRY": "Veri Yok", "EUR_TRY": "Veri Yok", "TRY_AFN": "Veri Yok"}

    def fetch_weather(self) -> str:
        """Elazığ için hava durumunu çeker."""
        logger.info("Elazığ hava durumu çekiliyor...")
        try:
            # Ücretsiz ve API Key gerektirmeyen wttr.in servisi
            url = "https://wttr.in/Elazığ?format=%C+%t"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
            return "Hava durumu verisi alınamadı."
        except Exception as e:
            logger.error(f"Hava durumu hatası: {e}")
            return "Hava durumu servisine ulaşılamadı."

    def fetch_news(self) -> List[str]:
        """Yedekli mimari ile RSS kaynaklarından haber başlıklarını toplar."""
        logger.info("Haber kaynakları taranıyor...")
        sources = [
            "https://www.haberturk.com/rss/ekonomi.xml",
            "https://www.cnnturk.com/feed/rss/ekonomi/news"
        ]
        
        for url in sources:
            try:
                req = requests.get(url, headers=self.headers, timeout=5)
                if req.status_code == 200:
                    soup = BeautifulSoup(req.content, "html.parser")
                    items = soup.find_all("item", limit=3)
                    if items:
                        return [item.find("title").text.replace("<![CDATA[", "").replace("]]>", "").strip() for item in items if item.find("title")]
            except requests.RequestException:
                continue
        
        logger.warning("Hiçbir haber kaynağına ulaşılamadı.")
        return ["Güncel ekonomi haberi bulunamadı."]

    def generate_report(self, market_data: Dict[str, str], weather: str, news: List[str]) -> str:
        """Toplanan verileri Gemini AI kullanarak yönetici bültenine dönüştürür."""
        logger.info("Gemini AI ile bülten oluşturuluyor...")
        prompt = f"""
        Sen profesyonel bir veri analisti ve asistansın. Aşağıdaki ham verileri kullanarak 
        akıcı, kısa ve profesyonel bir sabah bülteni hazırla.

        PİYASA (Güncel/Kapanış Verileri): 
        - Dolar: {market_data['USD_TRY']} TL 
        - Euro: {market_data['EUR_TRY']} TL
        - 1 TL: {market_data['TRY_AFN']} Afgani
        - Gram Altın: {market_data['Gram_Altin']} TL
        
        HAVA DURUMU (Elazığ): {weather}
        
        ÖNE ÇIKAN HABERLER: {', '.join(news)}
        
        Bültenin sonuna Elazığ'daki hava durumuna göre ufak bir tavsiye eklemeyi unutma.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"AI Raporu oluşturulamadı: {e}")
            return "Sistem hatası: AI raporu oluşturulamadı."

    def send_email(self, content: str) -> None:
        """Oluşturulan raporu SMTP üzerinden güvenli bir şekilde e-posta ile iletir."""
        logger.info("E-posta sunucusuna bağlanılıyor...")
        msg = MIMEMultipart()
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver
        msg['Subject'] = "🤖 Otonom Sistem: Günlük Finans ve Hava Durumu Raporu"
        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            logger.info("✅ Bülten başarıyla gönderildi!")
        except Exception as e:
            logger.critical(f"E-posta gönderimi başarısız: {e}")

    def run_pipeline(self):
        """Ajanın tüm iş akışını (Pipeline) sırasıyla yürütür."""
        logger.info("--- Ajan İş Akışı Başlatıldı ---")
        market_data = self.fetch_market_data()
        weather = self.fetch_weather()
        news = self.fetch_news()
        report = self.generate_report(market_data, weather, news)
        self.send_email(report)
        logger.info("--- Ajan İş Akışı Tamamlandı ---")

if __name__ == "__main__":
    agent = DailyBriefingAgent()
    agent.run_pipeline()