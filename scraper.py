import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_ultra_scraper():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x450"
            
            if i == 0:
                # الخبر الرئيسي الكبير (مثل كووورة وسكاي)
                news_html += f'''
                <div class="main-hero">
                    <a href="{my_link}" target="_blank">
                        <img src="{img}">
                        <div class="main-hero-overlay">
                            <span class="category-tag">برشلونة</span>
                            <h3>{title}</h3>
                            <div class="main-meta">⏱️ {datetime.now().strftime('%H:%M')} | 💬 10</div>
                        </div>
                    </a>
                </div>'''
            else:
                # الأخبار العريضة الفخمة (مثل صورة Vortex الأخيرة)
                news_html += f'''
                <div class="v-ultra-card">
                    <a href="{my_link}" target="_blank">
                        <div class="v-card-img">
                            <img src="{img}" loading="lazy">
                            <span class="v-badge">حصري</span>
                        </div>
                        <div class="v-card-content">
                            <h3>"{title}"</h3>
                            <div class="v-card-footer">
                                <span class="v-btn-details">التفاصيل</span>
                                <span class="v-time">{datetime.now().strftime('%H:%M')} ⏱️</span>
                            </div>
                        </div>
                    </a>
                </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX 26 | ستاديوم</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0d0f14; --card: #161a21; --accent: #c5a059; --text: #f0f0f0; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 30px; }}
        
        header {{ background: var(--card); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 2px solid var(--accent); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; text-decoration: none; color: #fff; }}
        .logo span {{ color: var(--accent); }}
        .live-dot {{ color: #00ff88; font-size: 13px; font-weight: bold; }}

        .container {{ max-width: 800px; margin: 0 auto; padding: 0 10px; }}

        /* التصميم الرئيسي (Hero) */
        .main-hero {{ width: 100%; position: relative; height: 350px; overflow: hidden; margin-bottom: 20px; }}
        .main-hero img {{ width: 100%; height: 100%; object-fit: cover; }}
        .main-hero-overlay {{ position: absolute; bottom: 0; width: 100%; padding: 30px 20px; background: linear-gradient(transparent, rgba(0,0,0,0.9)); box-sizing: border-box; }}
        .category-tag {{ font-size: 12px; color: #aaa; margin-bottom: 5px; display: block; }}
        .main-hero h3 {{ font-size: 20px; margin: 5px 0; line-height: 1.5; font-weight: 900; }}
        .main-meta {{ font-size: 11px; color: #888; margin-top: 10px; }}

        /* تصميم كروت Vortex Ultra */
        .v-ultra-card {{ background: var(--card); border-radius: 18px; margin-bottom: 15px; overflow: hidden; border: 1px solid #232932; }}
        .v-ultra-card a {{ text-decoration: none; color: inherit; }}
        .v-card-img {{ width: 100%; height: 220px; position: relative; }}
        .v-card-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-badge {{ position: absolute; top: 15px; right: 15px; background: var(--accent); color: #000; font-size: 11px; font-weight: 900; padding: 3px 12px; border-radius: 6px; }}
        
        .v-card-content {{ padding: 20px; text-align: center; }}
        .v-card-content h3 {{ font-size: 18px; margin: 0 0 20px; line-height: 1.6; font-weight: 700; color: #e0e0e0; }}
        .v-card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #252a33; padding-top: 15px; }}
        .v-btn-details {{ color: var(--accent); border: 1px solid var(--accent); padding: 4px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .v-time {{ font-size: 12px; color: #777; }}

        footer {{ text-align: center; padding: 40px; opacity: 0.4; font-size: 11px; }}

        @media (max-width: 600px) {{
            .main-hero {{ height: 280px; }}
            .v-card-img {{ height: 180px; }}
            .v-card-content h3 {{ font-size: 16px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="live-dot">● مباشر</div>
        <a href="#" class="logo">VORTEX<span>26</span></a>
    </header>

    <div class="container">
        {news_html}
    </div>

    <footer>VORTEX STADIUM 24 - 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_ultra_scraper()
