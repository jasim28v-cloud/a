import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_vortex_scraper():
    base_url = "https://www.yallakora.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. سحب الأخبار الحصرية بتنسيق عالي الجودة
        news_res = requests.get(f"{base_url}/news", headers=headers, timeout=15)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'lxml')
        news_html = ""
        
        for item in news_soup.find_all('div', class_='desc')[:12]:
            title = item.find('h3').text.strip() if item.find('h3') else ""
            img_tag = item.find_previous('img')
            img = img_tag.get('data-src') or img_tag.get('src') if img_tag else "https://via.placeholder.com/400x250"
            
            news_html += f'''
            <div class="v-card">
                <a href="{my_link}" target="_blank">
                    <div class="v-img-wrapper">
                        <img src="{img}" loading="lazy">
                        <div class="v-badge">حصري</div>
                    </div>
                    <div class="v-body">
                        <h3>{title}</h3>
                        <div class="v-meta">⏱️ {datetime.now().strftime('%H:%M')} | ستاديوم 24</div>
                    </div>
                </a>
            </div>'''

        # 2. سحب المباريات بتنسيق المركز الرياضي المتطور
        match_res = requests.get(f"{base_url}/match-center", headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        
        for league in match_soup.find_all('div', class_='matchCard')[:5]:
            l_name = league.find('h2').text.strip()
            matches_html += f'<div class="l-tag">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:2]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text} - {res[1].text}" if len(res) > 1 else "VS"
                time = m.find('span', class_='time').text.strip()
                matches_html += f'''
                <div class="m-row">
                    <div class="m-team-name">{t1}</div>
                    <div class="m-center">
                        <div class="m-score-box">{score}</div>
                        <div class="m-time-text">{time}</div>
                    </div>
                    <div class="m-team-name">{t2}</div>
                    <a href="{my_link}" target="_blank" class="m-btn-live">مباشر</a>
                </div>'''

        # 3. بناء واجهة Vortex 26 الفاخرة
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vortex 26 | ستاديوم</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {{ --v-gold: #c5a059; --v-dark: #0a0c10; --v-card: #12151c; --v-accent: #007bff; }}
        body {{ background: var(--v-dark); color: #fff; font-family: 'Cairo', sans-serif; margin: 0; padding: 0; }}
        
        /* Modern Glass Header */
        header {{ background: rgba(18, 21, 28, 0.9); backdrop-filter: blur(15px); padding: 15px 8%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 2000; border-bottom: 2px solid var(--v-gold); }}
        .v-logo {{ font-size: 28px; font-weight: 900; letter-spacing: -1px; text-decoration: none; color: #fff; }}
        .v-logo span {{ color: var(--v-gold); }}

        /* Dynamic Container */
        .v-container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 1fr 400px; gap: 30px; padding: 0 20px; }}
        
        /* News Grid */
        .section-header {{ font-size: 24px; font-weight: 900; margin-bottom: 25px; border-right: 6px solid var(--v-gold); padding-right: 15px; }}
        .v-card {{ background: var(--v-card); border-radius: 12px; margin-bottom: 20px; overflow: hidden; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); border: 1px solid #1f2530; }}
        .v-card:hover {{ transform: translateY(-5px); border-color: var(--v-gold); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .v-card a {{ text-decoration: none; color: inherit; display: flex; }}
        .v-img-wrapper {{ width: 200px; height: 130px; position: relative; flex-shrink: 0; }}
        .v-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .v-badge {{ position: absolute; top: 10px; right: 10px; background: var(--v-gold); color: #000; padding: 2px 10px; font-size: 10px; font-weight: 900; border-radius: 4px; }}
        .v-body {{ padding: 20px; display: flex; flex-direction: column; justify-content: center; }}
        .v-body h3 {{ font-size: 17px; margin: 0 0 10px 0; line-height: 1.6; color: #f0f0f0; }}
        .v-meta {{ font-size: 11px; color: #7a8292; font-weight: bold; }}

        /* Sidebar & Match Center */
        .v-sidebar {{ background: var(--v-card); border-radius: 20px; padding: 25px; border: 1px solid #1f2530; align-self: start; position: sticky; top: 100px; }}
        .l-tag {{ background: rgba(197, 160, 89, 0.1); color: var(--v-gold); padding: 8px 15px; font-size: 13px; font-weight: 900; margin: 25px 0 15px 0; border-radius: 8px; text-align: center; border: 1px solid var(--v-gold); }}
        .m-row {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 0; border-bottom: 1px solid #1f2530; }}
        .m-team-name {{ width: 35%; font-size: 13px; font-weight: bold; text-align: center; color: #fff; }}
        .m-center {{ width: 30%; text-align: center; }}
        .m-score-box {{ background: #1f2530; color: var(--v-gold); font-weight: 900; padding: 6px; border-radius: 8px; font-size: 15px; margin-bottom: 5px; }}
        .m-time-text {{ font-size: 10px; color: #7a8292; }}
        .m-btn-live {{ display: block; background: var(--v-gold); color: #000; text-decoration: none; font-size: 11px; font-weight: 900; padding: 5px; border-radius: 6px; margin-top: 8px; transition: 0.3s; }}
        .m-btn-live:hover {{ background: #fff; }}

        /* Luxury Footer */
        footer {{ background: #050608; padding: 80px 20px; text-align: center; margin-top: 60px; border-top: 3px solid var(--v-gold); }}
        .f-logo {{ font-size: 36px; font-weight: 900; color: #fff; margin-bottom: 15px; }}
        .f-socials {{ margin: 30px 0; }}
        .f-socials a {{ color: var(--v-gold); font-size: 28px; margin: 0 20px; transition: 0.3s; }}
        .f-socials a:hover {{ color: #fff; transform: scale(1.2); }}

        @media (max-width: 1000px) {{
            .v-container {{ grid-template-columns: 1fr; }}
            .v-sidebar {{ position: static; }}
            .v-img-wrapper {{ width: 140px; height: 100px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="v-logo">VORTEX<span>26</span></a>
        <div style="color: #00ff88; font-size: 13px; font-weight: bold;"><i class="fas fa-satellite-dish"></i> تغطية مباشرة</div>
    </header>

    <div class="v-container">
        <div class="v-main">
            <div class="section-header">أبرز الأخبار الآن</div>
            {news_html}
        </div>

        <div class="v-sidebar">
            <div style="font-size: 20px; font-weight: 900; color: var(--v-gold);"><i class="fas fa-trophy"></i> مركز المباريات</div>
            {matches_html}
        </div>
    </div>

    <footer>
        <div class="f-logo">VORTEX STADIUM</div>
        <div class="f-socials">
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-x-twitter"></i></a>
        </div>
        <p style="font-size: 13px; color: #4b5563;">© 2026 جميع الحقوق محفوظة لمنصة Vortex العالمية</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_vortex_scraper()
