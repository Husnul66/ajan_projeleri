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
    """Günlük finans ve haber verilerini toplayıp AI ile özetleyen otonom ajan."""

    def __init__(self):
        # Hassas veriler işletim sisteminin veya GitHub'ın gizli ortam değişkenlerinden çekilir
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
        """Yahoo Finance üzerinden altın ve döviz verilerini hesaplar."""
        logger.info("Piyasa verileri çekiliyor...")
        try:
            usd_try = yf.Ticker("TRY=X").history(period="1d")['Close'].iloc[-1]
            gold_oz_usd = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin_try = (gold_oz_usd / 31.1034768) * usd_try
            return {"Gram_Altin": f"{gram_altin_try:.2f}", "USD_TRY": f"{usd_try:.2f}"}
        except Exception as e:
            logger.error(f"Piyasa verisi alınırken hata: {e}")
            return {"Gram_Altin": "Veri Yok", "USD_TRY": "Veri Yok"}

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

    def generate_report(self, market_data: Dict[str, str], news: List[str]) -> str:
        """Toplanan verileri Gemini AI kullanarak yönetici bültenine dönüştürür."""
        logger.info("Gemini AI ile bülten oluşturuluyor...")
        prompt = f"""
        Sen profesyonel bir veri analisti ve asistansın. Aşağıdaki ham verileri kullanarak 
        akıcı, kısa ve profesyonel bir sabah bülteni hazırla.

        PİYASA: Dolar: {market_data['USD_TRY']} TL | Gram Altın: {market_data['Gram_Altin']} TL
        ÖNE ÇIKAN HABERLER: {', '.join(news)}
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
        msg['Subject'] = "🤖 Otonom Sistem: Günlük Finans Raporu"
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
        news = self.fetch_news()
        report = self.generate_report(market_data, news)
        self.send_email(report)
        logger.info("--- Ajan İş Akışı Tamamlandı ---")

if __name__ == "__main__":
    # Sınıfı çağır ve sistemi çalıştır
    agent = DailyBriefingAgent()
    agent.run_pipeline()