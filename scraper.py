import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_ultra_scraper():
    # مصادر البحث المزدوجة
    news_rss = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي المعتمد
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. البحث وجلب الأخبار من RT
        news_res = requests.get(news_rss, headers=headers)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'xml')
        items = news_soup.find_all('item')
        
        news_html = ""
        for item in items[:12]:
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/150"
            news_html += f'''
            <div class="yk-news-card">
                <a href="{my_link}" target="_blank">
                    <div class="yk-news-content">
                        <h3>{title}</h3>
                        <span>أخبار الرياضة | ⏱️ الآن</span>
                    </div>
                    <img src="{img}" loading="lazy">
                </a>
            </div>'''

        # 2. البحث وجلب جدول المباريات من يلا كورة
        match_res = requests.get(matches_url, headers=headers)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        leagues = match_soup.find_all('div', class_='matchCard')
        
        matches_section = ""
        for league in leagues[:4]:
            l_name = league.find('h2').text.strip() if league.find('h2') else "بطولة دولية"
            matches_section += f'<div class="yk-l-header">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:3]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                score_spans = m.find('div', class_='MResult').find_all('span')
                score_txt = f"{score_spans[0].text} - {score_spans[1].text}" if len(score_spans) > 1 else "لم تبدأ"
                time = m.find('span', class_='time').text.strip()
                matches_section += f'''
                <div class="yk-m-box">
                    <div class="yk-t-name">{t1}</div>
                    <div class="yk-m-info">
                        <span class="yk-score">{score_txt}</span>
                        <span class="yk-time">{time}</span>
                        <a href="{my_link}" target="_blank" class="yk-m-details">التفاصيل</a>
                    </div>
                    <div class="yk-t-name">{t2}</div>
                </div>'''

        # 3. بناء الواجهة النهائية (YallaKora Style)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YallaKora 24 - مركز المباريات</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{ background: #f4f4f4; font-family: sans-serif; margin: 0; padding-top: 60px; }}
        header {{ background: #fff; padding: 10px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #004d9c; position: fixed; top: 0; width: 100%; z-index: 1000; box-sizing: border-box; }}
        .yk-logo {{ font-size: 24px; font-weight: bold; color: #004d9c; text-decoration: none; }}
        
        .section-head {{ background: #004d9c; color: #fff; padding: 12px; font-weight: bold; text-align: center; margin-top: 10px; }}
        
        .yk-news-card {{ background: #fff; border-bottom: 1px solid #eee; padding: 12px; }}
        .yk-news-card a {{ text-decoration: none; display: flex; justify-content: space-between; align-items: center; }}
        .yk-news-content {{ width: 70%; }}
        .yk-news-content h3 {{ font-size: 15px; color: #333; margin: 0; line-height: 1.5; }}
        .yk-news-card img {{ width: 90px; height: 65px; object-fit: cover; border-radius: 4px; }}

        .yk-l-header {{ background: #222; color: #fff; padding: 10px 15px; font-size: 13px; font-weight: bold; }}
        .yk-m-box {{ background: #fff; display: flex; align-items: center; justify-content: space-between; padding: 15px; border-bottom: 1px solid #eee; }}
        .yk-t-name {{ width: 30%; font-weight: bold; font-size: 13px; text-align: center; }}
        .yk-m-info {{ text-align: center; width: 30%; }}
        .yk-score {{ display: block; background: #fdf2c4; font-weight: bold; padding: 4px; border-radius: 4px; color: #d32f2f; }}
        .yk-time {{ font-size: 10px; color: #888; display: block; margin: 3px 0; }}
        .yk-m-details {{ font-size: 10px; color: #fff; background: #004d9c; padding: 3px 10px; border-radius: 20px; text-decoration: none; font-weight: bold; }}

        footer {{ background: #000; color: #fff; padding: 40px 20px; text-align: center; margin-top: 20px; }}
        .f-apps img {{ width: 110px; margin: 10px 5px; }}
        .f-socials a {{ color: #fff; font-size: 22px; margin: 0 12px; }}
    </style>
</head>
<body>
    <header><a href="#" class="yk-logo">YallaKora 24</a></header>
    
    <div class="section-head">آخر الأخبار الرياضية</div>
    {news_html}

    <div class="section-head">جدول مباريات اليوم</div>
    {matches_section}

    <footer>
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 20px;">YallaKora</div>
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
        <p style="font-size: 12px; color: #888; margin-top: 20px;">© جميع الحقوق محفوظة لـ ملاعِب لايف 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_ultra_scraper()
