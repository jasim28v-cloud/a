import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_grid_scraper():
    # استخدام كورة كول و يلا كورة للمحتوى الرياضي المركز
    news_rss = "https://www.kooora4goal.com/feed/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. سحب الأخبار (نظام المربعات)
        news_res = requests.get(news_rss, headers=headers, timeout=20)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'xml')
        items = news_soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = "https://via.placeholder.com/400x400"
            if item.find('enclosure'):
                img = item.find('enclosure').get('url')
            
            news_grid_html += f'''
            <div class="news-square">
                <a href="{my_link}" target="_blank">
                    <div class="square-img">
                        <img src="{img}" alt="sports news" loading="lazy">
                        <div class="square-tag">حصري</div>
                    </div>
                    <div class="square-body">
                        <h3>{title}</h3>
                        <div class="square-meta">⏱️ {datetime.now().strftime('%H:%M')} | أخبار الرياضة</div>
                    </div>
                </a>
            </div>'''

        # 2. سحب المباريات (نظام يلا كورة الفخم)
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        
        for league in match_soup.find_all('div', class_='matchCard')[:3]:
            l_name = league.find('h2').text.strip()
            matches_html += f'<div class="league-title">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:2]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text} - {res[1].text}" if len(res) > 1 else "VS"
                matches_html += f'''
                <div class="match-box">
                    <div class="m-team">{t1}</div>
                    <div class="m-score">{score}</div>
                    <div class="m-team">{t2}</div>
                    <a href="{my_link}" target="_blank" class="m-btn">تفاصيل</a>
                </div>'''

        # 3. التصميم النهائي (Vortex Square UI)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEX 26 | الرياضة العالمية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --main-bg: #0d0f14; --card-bg: #161a21; --accent: #c5a059; --red: #ed1c24; }}
        body {{ background: var(--main-bg); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; }}
        
        /* Header Style from Sky/Vortex */
        header {{ background: var(--card-bg); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--accent); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--accent); }}
        .live-status {{ color: #00ff88; font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 5px; }}

        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        
        /* Match Center Section */
        .match-section {{ background: var(--card-bg); border-radius: 15px; padding: 20px; margin-bottom: 30px; border: 1px solid #252a33; }}
        .league-title {{ background: rgba(197, 160, 89, 0.1); color: var(--accent); padding: 8px 15px; border-radius: 5px; font-weight: 900; margin: 15px 0 10px; font-size: 14px; border-right: 4px solid var(--accent); }}
        .match-box {{ display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #252a33; }}
        .m-team {{ width: 35%; text-align: center; font-weight: bold; font-size: 13px; }}
        .m-score {{ background: #1f242d; color: var(--accent); padding: 5px 15px; border-radius: 5px; font-weight: 900; }}
        .m-btn {{ background: var(--accent); color: #000; text-decoration: none; font-size: 10px; padding: 3px 10px; border-radius: 4px; font-weight: bold; }}

        /* News Grid (Square Style) */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .news-square {{ background: var(--card-bg); border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #1f242d; }}
        .news-square:hover {{ transform: translateY(-5px); border-color: var(--accent); }}
        .news-square a {{ text-decoration: none; color: inherit; }}
        .square-img {{ position: relative; width: 100%; height: 200px; }}
        .square-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .square-tag {{ position: absolute; top: 10px; right: 10px; background: var(--accent); color: #000; font-size: 10px; font-weight: 900; padding: 2px 8px; border-radius: 3px; }}
        .square-body {{ padding: 15px; }}
        .square-body h3 {{ font-size: 15px; margin: 0 0 10px; line-height: 1.6; height: 48px; overflow: hidden; color: #f0f0f0; }}
        .square-meta {{ font-size: 11px; color: #717b8a; }}

        footer {{ background: #000; padding: 40px; text-align: center; border-top: 2px solid var(--accent); margin-top: 50px; }}
        
        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: repeat(auto-fill, minmax(100%, 1fr)); }}
            .m-team {{ font-size: 11px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX<span>26</span></a>
        <div class="live-status">● تغطية مباشرة</div>
    </header>

    <div class="container">
        <h2 style="border-right: 5px solid var(--accent); padding-right: 15px; margin-bottom: 20px;">🏆 مركز النتائج والمباريات</h2>
        <div class="match-section">
            {matches_html}
        </div>

        <h2 style="border-right: 5px solid var(--red); padding-right: 15px; margin: 40px 0 20px;">📰 آخر الأخبار الرياضية</h2>
        <div class="news-grid">
            {news_grid_html}
        </div>
    </div>

    <footer>
        <div style="font-size: 24px; font-weight: 900;">VORTEX STADIUM 24</div>
        <p style="font-size: 12px; color: #555;">أقوى تغطية رياضية عالمية بنظام النخبة</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_vortex_grid_scraper()
