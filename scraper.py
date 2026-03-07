import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_infinity_scraper():
    base_url = "https://www.yallakora.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي المعتمد في ملفاتك
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. سحب أخبار "يلا كورة" الحصرية
        news_res = requests.get(f"{base_url}/news", headers=headers, timeout=15)
        news_res.encoding = 'utf-8'
        news_soup = BeautifulSoup(news_res.content, 'lxml')
        news_html = ""
        
        for item in news_soup.find_all('div', class_='desc')[:12]:
            title = item.find('h3').text.strip() if item.find('h3') else ""
            img_tag = item.find_previous('img')
            img = img_tag.get('data-src') or img_tag.get('src') if img_tag else "https://via.placeholder.com/400x250"
            
            news_html += f'''
            <div class="news-card">
                <a href="{my_link}" target="_blank">
                    <div class="img-container">
                        <img src="{img}" loading="lazy">
                        <span class="news-tag">LIVE</span>
                    </div>
                    <div class="news-info">
                        <h3>{title}</h3>
                        <div class="news-meta">🏟️ كرة قدم عالمية | ⏱️ {datetime.now().strftime('%H:%M')}</div>
                    </div>
                </a>
            </div>'''

        # 2. سحب المباريات الحية
        match_res = requests.get(f"{base_url}/match-center", headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        
        for league in match_soup.find_all('div', class_='matchCard')[:4]:
            l_name = league.find('h2').text.strip()
            matches_html += f'<div class="league-separator">{l_name}</div>'
            for m in league.find_all('div', class_='allMatchesList')[:2]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text} - {res[1].text}" if len(res) > 1 else "VS"
                time = m.find('span', class_='time').text.strip()
                matches_html += f'''
                <div class="match-item">
                    <div class="m-team">{t1}</div>
                    <div class="m-result">
                        <div class="m-score">{score}</div>
                        <div class="m-time">{time}</div>
                    </div>
                    <div class="m-team">{t2}</div>
                    <a href="{my_link}" target="_blank" class="m-details">متابعة</a>
                </div>'''

        # 3. بناء الواجهة (The Infinity UI)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infinity Stadium 24</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {{ --gold: #c5a059; --dark-bg: #0b0e11; --card-bg: #15191d; --text: #e1e1e1; }}
        body {{ background: var(--dark-bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 50px; }}
        
        /* Glassmorphism Navbar */
        nav {{ background: rgba(21, 25, 29, 0.95); backdrop-filter: blur(10px); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; border-bottom: 2px solid var(--gold); }}
        .logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; text-transform: uppercase; }}
        .logo span {{ color: var(--gold); }}

        /* Main Grid Layout */
        .container {{ max-width: 1200px; margin: 20px auto; display: grid; grid-template-columns: 1fr 380px; gap: 25px; padding: 0 15px; }}
        
        /* News Section */
        .news-title {{ font-size: 22px; font-weight: 900; border-right: 5px solid var(--gold); padding-right: 15px; margin-bottom: 20px; }}
        .news-card {{ background: var(--card-bg); border-radius: 15px; margin-bottom: 15px; overflow: hidden; transition: 0.3s; border: 1px solid #232a31; }}
        .news-card:hover {{ transform: scale(1.02); border-color: var(--gold); }}
        .news-card a {{ text-decoration: none; color: inherit; display: flex; }}
        .img-container {{ width: 180px; height: 120px; position: relative; flex-shrink: 0; }}
        .img-container img {{ width: 100%; height: 100%; object-fit: cover; }}
        .news-tag {{ position: absolute; top: 8px; right: 8px; background: #e02f2f; color: white; padding: 2px 8px; font-size: 10px; font-weight: bold; border-radius: 4px; }}
        .news-info {{ padding: 15px; display: flex; flex-direction: column; justify-content: center; }}
        .news-info h3 {{ font-size: 16px; margin: 0 0 10px 0; line-height: 1.5; color: #fff; }}
        .news-meta {{ font-size: 11px; color: #888; }}

        /* Live Score Sidebar */
        .sidebar {{ background: var(--card-bg); border-radius: 20px; padding: 20px; border: 1px solid #232a31; align-self: start; }}
        .league-separator {{ background: var(--gold); color: #000; padding: 5px 15px; font-size: 12px; font-weight: bold; margin: 20px 0 10px 0; border-radius: 5px; }}
        .match-item {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #232a31; }}
        .m-team {{ width: 35%; font-size: 12px; font-weight: bold; text-align: center; color: #fff; }}
        .m-result {{ width: 30%; text-align: center; }}
        .m-score {{ background: #232a31; color: var(--gold); font-weight: 900; padding: 5px; border-radius: 8px; font-size: 14px; margin-bottom: 4px; }}
        .m-time {{ font-size: 10px; color: #888; }}
        .m-details {{ display: block; background: var(--gold); color: #000; text-decoration: none; font-size: 10px; font-weight: bold; padding: 4px; border-radius: 5px; margin-top: 5px; }}

        /* Footer Black Pearl */
        footer {{ background: #000; padding: 60px 20px; text-align: center; margin-top: 50px; border-top: 2px solid var(--gold); }}
        .f-logo {{ font-size: 32px; font-weight: 900; color: #fff; margin-bottom: 20px; }}
        .f-socials a {{ color: var(--gold); font-size: 24px; margin: 0 15px; }}
        .f-apps img {{ width: 130px; margin: 15px 10px; border: 1px solid #333; border-radius: 8px; }}

        @media (max-width: 900px) {{
            .container {{ grid-template-columns: 1fr; }}
            .sidebar {{ order: -1; }}
            .img-container {{ width: 130px; height: 90px; }}
        }}
    </style>
</head>
<body>
    <nav>
        <a href="#" class="logo">INFINITY<span>24</span></a>
        <div style="color: var(--gold); font-size: 12px; font-weight: bold;"><i class="fas fa-circle" style="color: #e02f2f; font-size: 8px;"></i> مباشر الآن</div>
    </nav>

    <div class="container">
        <div class="news-section">
            <div class="news-title">أحدث التقارير الرياضية</div>
            {news_html}
        </div>

        <div class="sidebar">
            <h2 style="margin:0; font-size: 20px; color: var(--gold);"><i class="fas fa-bolt"></i> مركز النتائج الحية</h2>
            {matches_html}
        </div>
    </div>

    <footer>
        <div class="f-logo">INFINITY STADIUM</div>
        <div class="f-socials">
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-x-twitter"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
        </div>
        <div class="f-apps">
            <img src="https://yallakora.com/images/badget-app-store.png">
            <img src="https://yallakora.com/images/badget-google-play.png">
        </div>
        <p style="font-size: 12px; color: #444; margin-top: 30px;">تم التطوير بواسطة ذكاء ستاديوم المتقدم 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_infinity_scraper()
