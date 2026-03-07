import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_ultra_hybrid():
    # روابط المصادر
    news_rss = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي الذكي
        my_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # 1. جلب الأخبار
        news_res = requests.get(news_rss, headers=headers)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'xml')
        items = news_soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            news_html += f'''
            <div class="k-item">
                <a href="{my_link}" target="_blank" class="k-wrap">
                    <div class="k-img"><img src="{img}" loading="lazy"></div>
                    <div class="k-info">
                        <h2>{title}</h2>
                        <div class="k-meta"><span class="k-cat">أخبار الرياضة</span></div>
                    </div>
                </a>
            </div>'''

        # 2. جلب جدول مباريات "يلا كورة" للواجهة السفلية
        match_res = requests.get(matches_url, headers=headers)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        
        leagues = match_soup.find_all('div', class_='matchCard')
        matches_section = ""
        for league in leagues[:4]:
            l_name = league.find('h2').text.strip() if league.find('h2') else "بطولة عامة"
            matches_section += f'<div class="yk-league-head">{l_name}</div>'
            
            all_m = league.find_all('div', class_='allMatchesList')
            for m in all_m:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                score = m.find('div', class_='MResult').find_all('span')
                score_txt = f"{score[0].text} - {score[1].text}" if len(score) > 1 else "لم تبدأ"
                time = m.find('span', class_='time').text.strip()
                
                matches_section += f'''
                <div class="yk-match-row">
                    <div class="yk-team">{t1}</div>
                    <div class="yk-score">
                        <span class="yk-val">{score_txt}</span>
                        <span class="yk-time">{time}</span>
                    </div>
                    <div class="yk-team">{t2}</div>
                    <a href="{my_link}" target="_blank" class="yk-btn">تفاصيل</a>
                </div>'''

        # 3. بناء الصفحة النهائية
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | يلا كورة الترا</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --yk-blue: #004d9c; --bg: #f4f4f4; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; margin: 0; padding-top: 70px; }}
        
        nav {{ background: #fff; border-bottom: 4px solid var(--yk-blue); position: fixed; top: 0; width: 100%; height: 65px; display: flex; align-items: center; padding: 0 5%; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); box-sizing: border-box; }}
        .logo {{ font-size: 24px; font-weight: 900; color: var(--yk-blue); text-decoration: none; }}
        
        .section-title {{ background: var(--yk-blue); color: #fff; padding: 15px; font-weight: 900; text-align: center; margin-top: 20px; }}
        
        /* قسم الأخبار العلوي */
        .news-container {{ max-width: 900px; margin: 0 auto; padding: 10px; }}
        .k-item {{ background: #fff; margin-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .k-wrap {{ text-decoration: none; color: inherit; display: flex; }}
        .k-img {{ width: 120px; height: 85px; }}
        .k-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .k-info {{ padding: 10px; }}
        .k-info h2 {{ font-size: 15px; margin: 0; color: #333; }}
        
        /* قسم يلا كورة السفلي */
        .yk-container {{ max-width: 900px; margin: 20px auto; padding: 10px; }}
        .yk-league-head {{ background: #333; color: #fff; padding: 10px; font-size: 14px; font-weight: bold; }}
        .yk-match-row {{ background: #fff; display: flex; align-items: center; justify-content: space-between; padding: 12px; border-bottom: 1px solid #eee; }}
        .yk-team {{ width: 30%; font-weight: bold; font-size: 13px; }}
        .yk-score {{ text-align: center; width: 30%; }}
        .yk-val {{ display: block; background: #fdf2c4; font-weight: 900; padding: 4px; border-radius: 4px; color: #d32f2f; }}
        .yk-time {{ font-size: 10px; color: #888; }}
        .yk-btn {{ background: var(--yk-blue); color: #fff; text-decoration: none; font-size: 11px; padding: 4px 8px; border-radius: 4px; }}
        
        .footer-logo {{ text-align: center; padding: 40px; background: #222; color: #fff; margin-top: 30px; }}
    </style>
</head>
<body>
    <nav><a href="#" class="logo">Yalla<span>Kora 24</span></a></nav>
    
    <div class="news-container">
        <div class="section-title">آخر الأخبار الرياضية</div>
        {news_html}
    </div>

    <div class="yk-container">
        <div class="section-title">مركز المباريات (يلا كورة)</div>
        {matches_section}
    </div>

    <div class="footer-logo">
        <img src="https://logodownload.org/wp-content/uploads/2019/07/kooora-logo.png" style="width:100px; filter: brightness(0) invert(1);"><br>
        <p>جميع الحقوق محفوظة لـ ستاديوم 24</p>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_ultra_hybrid()
