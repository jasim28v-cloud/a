import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_world_class_scraper():
    # مصادر البيانات المتقدمة
    news_rss = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    try:
        # رابطك الربحي الذهبي
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. جلب الأخبار بنظام الـ Cards الحديث
        news_res = requests.get(news_rss, headers=headers, timeout=15)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'xml')
        items = news_soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/400x250"
            news_html += f'''
            <div class="prime-card">
                <a href="{my_link}" target="_blank">
                    <div class="card-img-wrap">
                        <img src="{img}" loading="lazy">
                        <div class="card-badge">حصري</div>
                    </div>
                    <div class="card-body">
                        <h3>{title}</h3>
                        <div class="card-footer-info">⏱️ منذ قليل | 🏟️ تغطية عالمية</div>
                    </div>
                </a>
            </div>'''

        # 2. جلب المباريات بنظام Live Scoreboard من يلا كورة
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        leagues = match_soup.find_all('div', class_='matchCard')
        
        matches_section = ""
        for league in leagues[:5]:
            l_name = league.find('h2').text.strip() if league.find('h2') else "بطولة كبرى"
            matches_section += f'<div class="league-header-ultra">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:3]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text} - {res[1].text}" if len(res) > 1 else "vs"
                time = m.find('span', class_='time').text.strip()
                matches_section += f'''
                <div class="ultra-match-item">
                    <div class="u-team">{t1}</div>
                    <div class="u-score-area">
                        <span class="u-score-val">{score}</span>
                        <span class="u-time">{time}</span>
                    </div>
                    <div class="u-team">{t2}</div>
                    <a href="{my_link}" target="_blank" class="u-btn-live">متابعة</a>
                </div>'''

        # 3. بناء الواجهة الأسطورية
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | القمة الرياضية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        :root {{ --p: #004d9c; --s: #ffcc00; --dark: #121212; --bg: #f8f9fa; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; margin: 0; }}
        
        /* Navbar */
        nav {{ background: var(--p); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
        .nav-logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .nav-logo span {{ color: var(--s); }}
        .live-pulse {{ background: #ff4757; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; animation: pulse 1.5s infinite; }}
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}

        /* Layout */
        .main-wrapper {{ max-width: 1100px; margin: 20px auto; display: grid; grid-template-columns: 1fr 350px; gap: 20px; padding: 0 15px; }}
        
        /* News Grid */
        .news-grid {{ display: grid; grid-template-columns: 1fr; gap: 15px; }}
        .prime-card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; }}
        .prime-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .prime-card a {{ text-decoration: none; color: inherit; display: flex; }}
        .card-img-wrap {{ width: 160px; height: 110px; position: relative; flex-shrink: 0; }}
        .card-img-wrap img {{ width: 100%; height: 100%; object-fit: cover; }}
        .card-badge {{ position: absolute; top: 5px; right: 5px; background: var(--s); font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px; }}
        .card-body {{ padding: 12px; flex-grow: 1; }}
        .card-body h3 {{ font-size: 16px; margin: 0 0 10px 0; color: #333; line-height: 1.4; }}
        .card-footer-info {{ font-size: 11px; color: #888; }}

        /* Match Center Sidebar */
        .sidebar {{ background: #fff; border-radius: 12px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); align-self: start; }}
        .league-header-ultra {{ background: var(--dark); color: #fff; padding: 8px 12px; font-size: 13px; font-weight: bold; margin: 15px 0 10px 0; border-radius: 4px; }}
        .ultra-match-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
        .u-team {{ width: 35%; font-size: 12px; font-weight: bold; text-align: center; }}
        .u-score-area {{ width: 30%; text-align: center; }}
        .u-score-val {{ display: block; background: #fdf2c4; padding: 3px; border-radius: 4px; font-weight: 900; color: #d32f2f; }}
        .u-time {{ font-size: 10px; color: #999; }}
        .u-btn-live {{ display: block; margin-top: 5px; background: var(--p); color: #fff; text-decoration: none; font-size: 10px; padding: 2px 8px; border-radius: 4px; }}

        /* Footer Modern */
        footer {{ background: #000; color: #fff; padding: 50px 20px; text-align: center; margin-top: 50px; border-top: 5px solid var(--s); }}
        .f-apps img {{ width: 120px; margin: 10px; transition: 0.3s; }}
        .f-apps img:hover {{ opacity: 0.7; }}
        .f-socials {{ margin: 30px 0; }}
        .f-socials a {{ color: #fff; font-size: 24px; margin: 0 15px; text-decoration: none; }}
        .f-bottom {{ border-top: 1px solid #333; padding-top: 20px; font-size: 12px; color: #777; }}

        @media (max-width: 900px) {{
            .main-wrapper {{ grid-template-columns: 1fr; }}
            .sidebar {{ order: -1; }}
            .card-img-wrap {{ width: 120px; height: 90px; }}
            .card-body h3 {{ font-size: 14px; }}
        }}
    </style>
</head>
<body>
    <nav>
        <a href="#" class="nav-logo">STADIUM<span>24</span></a>
        <div class="live-pulse">● مباشر</div>
    </nav>

    <div class="main-wrapper">
        <div class="news-grid">
            <h2 style="border-right: 4px solid var(--p); padding-right: 15px; margin-bottom: 20px;">أحدث الأخبار</h2>
            {news_html}
        </div>

        <div class="sidebar">
            <h2 style="margin-top:0; color: var(--p);"><i class="fas fa-trophy"></i> مركز المباريات</h2>
            {matches_section}
        </div>
    </div>

    <footer>
        <div style="font-size: 30px; font-weight: 900; margin-bottom: 10px;">YallaKora <span style="color: var(--s);">24</span></div>
        <p>موقعك الرياضي الأول لمتابعة النتائج والأخبار لحظة بلحظة</p>
        <div class="f-apps">
            <img src="https://yallakora.com/images/badget-app-store.png">
            <img src="https://yallakora.com/images/badget-google-play.png">
        </div>
        <div class="f-socials">
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
        </div>
        <div class="f-bottom">
            <p>© جميع الحقوق محفوظة لـ ملاعب لايف | تم التطوير بأحدث تقنيات 2026</p>
        </div>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_world_class_scraper()
