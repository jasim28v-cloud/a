import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_rt_ads_scraper():
    # العودة لمصدر RT رياضة بناءً على طلبك
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الإعلاني الجديد الخاص بك
        my_ad_link = "https://data527.click/21330bf1d025d41336e6/4ba0cfe12d/?placementName=default"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x450"
            
            if i == 0:
                news_html += f'''
                <div class="v-hero">
                    <a href="{my_ad_link}" target="_blank">
                        <img src="{img}">
                        <div class="v-hero-info">
                            <span class="v-tag-live">تغطية RT مباشر</span>
                            <h3>{title}</h3>
                            <div class="v-meta">⏱️ {datetime.now().strftime('%H:%M')}</div>
                        </div>
                    </a>
                </div>'''
            else:
                news_html += f'''
                <div class="v-ultra-card">
                    <a href="{my_ad_link}" target="_blank">
                        <div class="v-card-img">
                            <img src="{img}" loading="lazy">
                            <span class="v-badge">RT حصري</span>
                        </div>
                        <div class="v-card-content">
                            <h3>"{title}"</h3>
                            <div class="v-card-footer">
                                <span class="v-btn-details">التفاصيل</span>
                                <span class="v-time">{datetime.now().strftime('%H:%M')}</span>
                            </div>
                        </div>
                    </a>
                </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX 26 | RT SPORT</title>
    
    <script src="https://data527.click/pfe/current/tag.min.js?z=8345712" data-cfasync="false" async></script>
    
    <script type='text/javascript' src='//pl25330eef.effectiveratecpm.com/26/33/0e/26330eef1cb397212db567d1385dc0b9.js'></script>

    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0d0f14; --card: #161a21; --accent: #c5a059; --text: #f0f0f0; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 30px; }}
        header {{ background: var(--card); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 2px solid var(--accent); position: sticky; top: 0; z-index: 1000; }}
        .v-logo {{ font-size: 24px; font-weight: 900; text-decoration: none; color: #fff; }}
        .v-logo span {{ color: var(--accent); }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 10px; }}
        .v-hero {{ position: relative; height: 350px; overflow: hidden; margin-bottom: 20px; border-radius: 0 0 15px 15px; border: 1px solid #1f242d; }}
        .v-hero img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-hero-info {{ position: absolute; bottom: 0; width: 100%; padding: 30px 20px; background: linear-gradient(transparent, rgba(0,0,0,0.95)); box-sizing: border-box; }}
        .v-ultra-card {{ background: var(--card); border-radius: 18px; margin-bottom: 15px; overflow: hidden; border: 1px solid #232932; }}
        .v-ultra-card a {{ text-decoration: none; color: inherit; }}
        .v-card-img {{ width: 100%; height: 220px; position: relative; }}
        .v-card-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-badge {{ position: absolute; top: 15px; right: 15px; background: var(--accent); color: #000; font-size: 11px; font-weight: 900; padding: 3px 12px; border-radius: 6px; }}
        .v-card-content {{ padding: 20px; text-align: center; }}
        .v-card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #252a33; padding-top: 15px; }}
        .v-btn-details {{ color: var(--accent); border: 1px solid var(--accent); padding: 4px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
    </style>
</head>
<body onclick="void(0)">
    <header>
        <div style="color: #00ff88; font-size: 13px; font-weight: bold;">● مباشر</div>
        <a href="#" class="v-logo">VORTEX<span>26</span></a>
    </header>
    <div class="container">
        {news_html}
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_rt_ads_scraper()
