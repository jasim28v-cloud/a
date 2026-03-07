import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_stadium_ultra():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        # الرابط الربحي الترا (Direct Link)
        my_link = "Https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')

        # 1. توليد جدول مباريات "وهمي" احترافي (لجذب النقرات)
        matches_list = [
            {"l": "الدوري الإسباني", "t1": "ريال مدريد", "t2": "برشلونة", "s": "21:00"},
            {"l": "الدوري الإنجليزي", "t1": "ليفربول", "t2": "مان سيتي", "s": "18:30"},
            {"l": "دوري أبطال أوروبا", "t1": "بايرن ميونخ", "t2": "باريس", "s": "مباشر"}
        ]
        
        matches_html = ""
        for m in matches_list:
            matches_html += f'''
            <div class="m-item">
                <span class="m-lg">{m['l']}</span>
                <div class="m-teams">
                    <span>{m['t1']}</span>
                    <span class="m-vs">{m['s']}</span>
                    <span>{m['t2']}</span>
                </div>
                <a href="{my_link}" target="_blank" class="m-link">التفاصيل</a>
            </div>'''

        # 2. معالجة الأخبار بتنسيق Prime Ultra
        news_html = ""
        for i, item in enumerate(items[:25]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            
            # قالب الخبر "طبق الأصل" كووورة
            news_html += f'''
            <div class="k-item">
                <a href="{my_link}" target="_blank" class="k-wrap">
                    <div class="k-img"><img src="{img}" alt="news"></div>
                    <div class="k-info">
                        <h2>{title}</h2>
                        <div class="k-meta">
                            <span class="k-cat">كرة قدم عالمية</span>
                            <span class="k-time">⏱️ منذ قليل</span>
                        </div>
                    </div>
                </a>
            </div>'''
            
            # بنر إعلاني "برايم" في منتصف الأخبار
            if i == 3:
                news_html += f'''
                <div class="k-ad-prime">
                    <a href="{my_link}" target="_blank">
                        <div class="ad-tag">حصري</div>
                        <h3>شاهد البث المباشر لمباريات اليوم بجودة عالية 📺</h3>
                        <p>اضغط هنا للدخول لصفحة البث المباشر</p>
                    </a>
                </div>'''

        # 3. بناء صفحة HTML الترا
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | كووورة الترا</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --main: #ffcc00; --bg: #efefef; --dark: #333; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; margin: 0; padding-top: 110px; }}
        
        /* Navbar Prime */
        nav {{ background: #fff; border-bottom: 4px solid var(--main); position: fixed; top: 0; width: 100%; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .nav-top {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 5%; }}
        .logo {{ font-size: 30px; font-weight: 900; color: #000; text-decoration: none; font-style: italic; }}
        .logo span {{ color: var(--main); }}
        .live-btn {{ background: red; color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 12px; animation: blink 1s infinite; }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}

        /* Matches Ultra Strip */
        .m-strip {{ background: #fff; display: flex; overflow-x: auto; padding: 10px; gap: 10px; border-bottom: 1px solid #ddd; }}
        .m-item {{ min-width: 160px; background: #fafafa; border: 1px solid #eee; border-radius: 4px; padding: 8px; text-align: center; }}
        .m-lg {{ font-size: 10px; color: #999; display: block; }}
        .m-teams {{ font-size: 12px; font-weight: bold; margin: 5px 0; display: flex; justify-content: space-between; align-items: center; }}
        .m-vs {{ background: #fff2c4; padding: 2px 5px; font-size: 10px; border-radius: 3px; }}
        .m-link {{ font-size: 11px; color: #0066cc; text-decoration: none; font-weight: bold; }}

        /* News Layout Ultra */
        .container {{ max-width: 900px; margin: 0 auto; padding: 10px; }}
        .k-item {{ background: #fff; margin-bottom: 10px; border-bottom: 1px solid #ddd; transition: 0.3s; }}
        .k-wrap {{ text-decoration: none; color: inherit; display: flex; }}
        .k-img {{ width: 140px; height: 95px; flex-shrink: 0; }}
        .k-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .k-info {{ padding: 10px; flex-grow: 1; }}
        .k-info h2 {{ font-size: 16px; margin: 0 0 8px 0; color: #003366; line-height: 1.4; }}
        .k-meta {{ font-size: 11px; color: #888; display: flex; gap: 15px; }}
        .k-cat {{ color: #d4a017; font-weight: bold; }}

        /* Ad Prime Ultra */
        .k-ad-prime {{ background: #fffbe6; border: 2px dashed var(--main); margin: 15px 0; padding: 20px; text-align: center; border-radius: 8px; }}
        .k-ad-prime a {{ text-decoration: none; color: #333; }}
        .ad-tag {{ background: var(--main); display: inline-block; padding: 2px 12px; border-radius: 20px; font-size: 10px; font-weight: 900; }}
        .k-ad-prime h3 {{ margin: 10px 0; color: #d32f2f; }}

        @media (max-width: 600px) {{ .k-img {{ width: 110px; height: 80px; }} .k-info h2 {{ font-size: 14px; }} }}
    </style>
</head>
<body>
    <nav>
        <div class="nav-top">
            <a href="#" class="logo">K<span>OOORA</span> 24</a>
            <div class="live-btn">● مباشر الآن</div>
        </div>
        <div class="m-strip">{matches_html}</div>
    </nav>
    <div class="container">{news_html}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_stadium_ultra()
