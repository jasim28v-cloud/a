import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_sky_style_scraper():
    news_rss = "https://www.skynewsarabia.com/feeds/rss/sport.xml"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        news_res = requests.get(news_rss, headers=headers, timeout=15)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'xml')
        items = news_soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:15]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x450"
            card_style = "sky-main-hero" if i == 0 else "sky-sub-card"
            news_html += f'''
            <div class="{card_style}">
                <a href="{my_link}" target="_blank">
                    <img src="{img}" loading="lazy">
                    <div class="sky-overlay">
                        <span class="sky-tag">أخبار الرياضة</span>
                        <h3>{title}</h3>
                    </div>
                </a>
            </div>'''

        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        leagues = match_soup.find_all('div', class_='matchCard')
        
        matches_html = ""
        for league in leagues[:3]:
            l_name = league.find('h2').text.strip() if league.find('h2') else "بطولة"
            matches_html += f'<div class="sky-league-title">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:2]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text} - {res[1].text}" if len(res) > 1 else "vs"
                matches_html += f'''
                <div class="sky-match-row">
                    <span>{t1}</span>
                    <span class="sky-score">{score}</span>
                    <span>{t2}</span>
                </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سكاي نيوز عربية | رياضة</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #fff; font-family: 'Noto Kufi Arabic', sans-serif; margin: 0; }}
        
        /* تصميم الهيدر بنفس شكل سكاي نيوز في الصورة */
        .sky-header {{ background: #fff; border-bottom: 1px solid #eee; padding: 10px 5%; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 1000; }}
        .sky-logo {{ display: flex; align-items: center; text-decoration: none; }}
        .sky-logo-black {{ background: #000; color: #fff; padding: 5px 10px; font-weight: 900; font-size: 22px; margin-left: 5px; }}
        .sky-logo-red {{ color: #ed1c24; font-weight: 900; font-size: 22px; }}
        .sky-live-btn {{ background: #ed1c24; color: #fff; padding: 3px 15px; font-weight: bold; font-size: 14px; border-radius: 3px; }}

        .sky-main-hero {{ width: 100%; position: relative; height: 60vh; overflow: hidden; border-bottom: 8px solid #ed1c24; }}
        .sky-main-hero img {{ width: 100%; height: 100%; object-fit: cover; }}
        .sky-overlay {{ position: absolute; bottom: 0; width: 100%; padding: 30px 5%; background: linear-gradient(transparent, rgba(0,0,0,0.8)); color: #fff; }}
        .sky-tag {{ background: #ed1c24; color: #fff; padding: 2px 10px; font-size: 12px; font-weight: bold; margin-bottom: 10px; display: inline-block; }}
        .sky-overlay h3 {{ font-size: 24px; margin: 5px 0; }}

        .sky-sub-card {{ padding: 15px; border-bottom: 1px solid #eee; display: flex; gap: 15px; }}
        .sky-sub-card img {{ width: 120px; height: 80px; object-fit: cover; }}
        .sky-sub-card h3 {{ font-size: 16px; margin: 0; color: #333; }}

        .sky-league-title {{ background: #f8f8f8; padding: 10px; font-weight: bold; color: #ed1c24; border-right: 4px solid #ed1c24; margin-top: 20px; }}
        .sky-match-row {{ display: flex; justify-content: space-between; padding: 15px; border-bottom: 1px solid #eee; align-items: center; font-size: 14px; }}
        .sky-score {{ font-weight: 900; background: #333; color: #fff; padding: 2px 10px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="sky-header">
        <div class="sky-logo">
            <span class="sky-logo-black">sky</span>
            <span class="sky-logo-red">news عربية</span>
        </div>
        <div class="sky-live-btn">مباشر</div>
    </div>

    {news_html[:news_html.find('</div>', news_html.find('sky-main-hero'))+6]}
    
    <div style="padding: 20px;">
        <h2 style="border-bottom: 2px solid #ed1c24; display: inline-block;">مركز المباريات</h2>
        {matches_html}
    </div>

    <div class="more-news">
        {news_html[news_html.find('</div>', news_html.find('sky-main-hero'))+6:]}
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_sky_style_scraper()
