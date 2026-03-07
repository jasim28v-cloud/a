import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_final_scraper():
    # المصدر الجديد: سكاي نيوز عربية (الأكثر احترافية حالياً)
    rss_url = "https://www.skynewsarabia.com/feeds/rss/sport.xml"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            # سحب الصور بجودة عالية من سكاي نيوز
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x450"
            
            if i == 0:
                # الخبر الرئيسي (Hero) بتصميم كووورة الفخم
                news_html += f'''
                <div class="v-hero">
                    <a href="{my_link}" target="_blank">
                        <img src="{img}">
                        <div class="v-hero-info">
                            <span class="v-tag-live">تغطية خاصة</span>
                            <h3>{title}</h3>
                            <div class="v-meta">📅 {datetime.now().strftime('%d مارس 2026')}</div>
                        </div>
                    </a>
                </div>'''
            else:
                # الأخبار التالية بتصميم كروت Vortex الاحترافي
                news_html += f'''
                <div class="v-premium-card">
                    <a href="{my_link}" target="_blank">
                        <div class="v-img-box">
                            <img src="{img}" loading="lazy">
                            <span class="v-exclusive">حصري</span>
                        </div>
                        <div class="v-details">
                            <h3>{title}</h3>
                            <div class="v-footer">
                                <span class="v-time">{datetime.now().strftime('%H:%M')} ⏱️</span>
                                <span class="v-btn">قراءة المزيد</span>
                            </div>
                        </div>
                    </a>
                </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX 26 | NEWS</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --v-bg: #0a0b0e; --v-card: #12151a; --v-gold: #c5a059; --v-white: #ffffff; }}
        body {{ background: var(--v-bg); color: var(--v-white); font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 50px; }}
        
        header {{ background: var(--v-card); padding: 15px 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--v-gold); position: sticky; top: 0; z-index: 1000; }}
        .v-logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .v-logo span {{ color: var(--v-gold); }}

        .v-main {{ max-width: 700px; margin: 0 auto; padding: 0 15px; }}

        /* تصميم الخبر الرئيسي */
        .v-hero {{ position: relative; width: 100%; height: 380px; border-radius: 0 0 20px 20px; overflow: hidden; margin-bottom: 25px; border: 1px solid #1f242d; }}
        .v-hero img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-hero-info {{ position: absolute; bottom: 0; width: 100%; padding: 40px 20px 20px; background: linear-gradient(transparent, rgba(0,0,0,0.95)); box-sizing: border-box; }}
        .v-tag-live {{ background: #ed1c24; padding: 2px 12px; font-size: 11px; font-weight: 900; border-radius: 4px; }}
        .v-hero h3 {{ font-size: 22px; margin: 12px 0; line-height: 1.5; }}

        /* تصميم الكروت المطورة */
        .v-premium-card {{ background: var(--v-card); border-radius: 15px; margin-bottom: 20px; overflow: hidden; border: 1px solid #1c2128; transition: 0.3s; }}
        .v-premium-card:hover {{ border-color: var(--v-gold); transform: translateY(-3px); }}
        .v-premium-card a {{ text-decoration: none; color: inherit; }}
        .v-img-box {{ position: relative; width: 100%; height: 240px; }}
        .v-img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-exclusive {{ position: absolute; top: 15px; right: 15px; background: var(--v-gold); color: #000; font-size: 10px; font-weight: 900; padding: 3px 10px; border-radius: 4px; }}
        
        .v-details {{ padding: 20px; }}
        .v-details h3 {{ font-size: 18px; margin: 0 0 20px; line-height: 1.6; font-weight: 700; }}
        .v-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #232a33; padding-top: 15px; }}
        .v-btn {{ color: var(--v-gold); font-size: 12px; font-weight: 900; text-transform: uppercase; border-bottom: 1px solid var(--v-gold); }}
        .v-time {{ font-size: 11px; color: #777; }}

        @media (max-width: 600px) {{
            .v-hero {{ height: 300px; }}
            .v-img-box {{ height: 200px; }}
            .v-details h3 {{ font-size: 16px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div style="color: #00ff88; font-size: 12px; font-weight: bold;">● مباشر الآن</div>
        <a href="#" class="v-logo">VORTEX<span>26</span></a>
    </header>

    <div class="v-main">
        {news_html}
    </div>

    <footer style="text-align: center; padding: 40px; font-size: 11px; color: #444;">
        جميع الحقوق محفوظة لمنصة VORTEX 26 الإخبارية
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_final_scraper()
