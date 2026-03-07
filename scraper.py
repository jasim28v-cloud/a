import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_stadium_pro():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي الذكي
        my_link = "Https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')

        # بناء شريط المباريات العلوي (Kooora Header Style)
        matches_html = ""
        leagues = ["الدوري الإسباني", "الدوري الإنجليزي", "دوري أبطال أوروبا"]
        for league in leagues:
            matches_html += f'''
            <div class="match-card">
                <div class="league-name">{league}</div>
                <div class="teams">
                    <span>فريق A</span>
                    <span class="score">0 - 0</span>
                    <span>فريق B</span>
                </div>
                <a href="{my_link}" target="_blank" class="match-details">تفاصيل المباراة</a>
            </div>'''

        # بناء قائمة الأخبار
        news_html = ""
        for i, item in enumerate(items[:20]):
            title = item.title.text
            link = item.link.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600"
            
            news_html += f'''
            <div class="kooora-news-item">
                <a href="{my_link}" target="_blank" class="news-link">
                    <div class="news-img"><img src="{img}" loading="lazy"></div>
                    <div class="news-content">
                        <h3>{title}</h3>
                        <div class="news-meta">🏟️ كرة عالمية | ⏱️ منذ قليل</div>
                    </div>
                </a>
            </div>'''
            
            # إعلان "حمل التطبيق" (مثل كووورة)
            if i == 2:
                news_html += f'''
                <div class="kooora-ad-box">
                    <a href="{my_link}" target="_blank">
                        <img src="https://logodownload.org/wp-content/uploads/2019/07/kooora-logo.png" style="width:50px; margin-bottom:10px;">
                        <p>تابع النتائج أولاً بأول عبر تطبيقنا</p>
                        <div class="ad-btn">حمل التطبيق الآن</div>
                    </a>
                </div>'''

        html_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | كووورة لايف</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --kooora-yellow: #ffcc00; --kooora-bg: #f4f4f4; --text: #333; }}
        body {{ background: var(--kooora-bg); font-family: 'Cairo', sans-serif; margin: 0; padding-top: 60px; }}
        
        /* Navbar */
        nav {{ background: #fff; border-bottom: 3px solid var(--kooora-yellow); position: fixed; top: 0; width: 100%; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 5%; z-index: 1000; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .logo-text {{ font-weight: 900; font-size: 24px; color: #000; text-decoration: none; }}
        .logo-text span {{ color: var(--kooora-yellow); }}
        .live-dot {{ color: red; animation: blink 1s infinite; font-weight: bold; font-size: 14px; }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}

        /* Matches Strip */
        .matches-strip {{ display: flex; overflow-x: auto; background: #fff; padding: 10px; gap: 10px; border-bottom: 1px solid #ddd; }}
        .match-card {{ min-width: 180px; background: #f9f9f9; border: 1px solid #eee; border-radius: 5px; padding: 10px; text-align: center; }}
        .league-name {{ font-size: 10px; color: #888; margin-bottom: 5px; }}
        .teams {{ font-size: 13px; font-weight: bold; margin-bottom: 5px; }}
        .score {{ background: var(--kooora-yellow); padding: 2px 5px; border-radius: 3px; margin: 0 5px; }}
        .match-details {{ font-size: 11px; color: #0066cc; text-decoration: none; }}

        /* News Layout */
        .main-grid {{ max-width: 800px; margin: 20px auto; padding: 0 10px; }}
        .kooora-news-item {{ background: #fff; margin-bottom: 15px; border-radius: 5px; overflow: hidden; display: flex; border-bottom: 2px solid #eee; }}
        .news-link {{ text-decoration: none; color: inherit; display: flex; width: 100%; }}
        .news-img {{ width: 120px; height: 90px; flex-shrink: 0; }}
        .news-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .news-content {{ padding: 10px; flex-grow: 1; }}
        .news-content h3 {{ font-size: 16px; margin: 0 0 10px 0; line-height: 1.4; }}
        .news-meta {{ font-size: 11px; color: #888; }}

        /* Ad Box */
        .kooora-ad-box {{ background: #fffbe6; border: 1px dashed var(--kooora-yellow); padding: 20px; text-align: center; margin: 15px 0; border-radius: 5px; }}
        .ad-btn {{ background: #000; color: #fff; padding: 8px 20px; border-radius: 20px; display: inline-block; margin-top: 10px; font-size: 13px; font-weight: bold; text-decoration: none; }}
    </style>
</head>
<body>
    <nav>
        <a href="#" class="logo-text">ستاديوم<span>24</span></a>
        <div><span class="live-dot">●</span> مباشر</div>
    </nav>
    <div class="matches-strip">{matches_html}</div>
    <div class="main-grid">{news_html}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html_content)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_stadium_pro()
