import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_sky_rt_fusion():
    # العودة لمصدر RT رياضة لضمان ظهور الصور بنسبة 100%
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي الذهبي
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_html = ""
        for i, item in enumerate(items[:18]):
            title = item.title.text
            # جلب الصورة من RT
            img = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x450"
            
            # التصميم السينمائي للخبر الأول والبقية كروت احترافية
            if i == 0:
                news_html += f'''
                <div class="sky-hero-main">
                    <a href="{my_link}" target="_blank">
                        <img src="{img}" alt="Breaking News">
                        <div class="sky-hero-text">
                            <span class="sky-label-live">عاجل</span>
                            <h3>{title}</h3>
                        </div>
                    </a>
                </div>'''
            else:
                news_html += f'''
                <div class="sky-item-card">
                    <a href="{my_link}" target="_blank">
                        <div class="sky-card-flex">
                            <div class="sky-card-img">
                                <img src="{img}" alt="news">
                            </div>
                            <div class="sky-card-info">
                                <h3>{title}</h3>
                                <span class="sky-meta">أخبار الرياضة | RT</span>
                            </div>
                        </div>
                    </a>
                </div>'''

        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم نيوز | أخبار الرياضة</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #fff; font-family: 'Noto Kufi Arabic', sans-serif; margin: 0; padding: 0; }}
        
        /* الهيدر المطابق لسكاي نيوز في الصورة */
        .header-sky {{ background: #fff; border-bottom: 2px solid #ed1c24; padding: 12px 5%; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 15px rgba(0,0,0,0.05); }}
        .brand-sky {{ display: flex; align-items: center; text-decoration: none; }}
        .brand-black {{ background: #000; color: #fff; padding: 4px 12px; font-weight: 900; font-size: 26px; letter-spacing: -1px; }}
        .brand-red {{ color: #ed1c24; font-weight: 900; font-size: 26px; padding-right: 6px; }}
        .live-tag {{ background: #ed1c24; color: #fff; padding: 4px 18px; font-weight: bold; font-size: 14px; border-radius: 2px; animation: pulse 1.5s infinite; }}
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} 100% {{ opacity: 1; }} }}

        /* الخبر الرئيسي (عرض الشاشة) */
        .sky-hero-main {{ position: relative; width: 100%; height: 55vh; overflow: hidden; }}
        .sky-hero-main img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .sky-hero-main:hover img {{ transform: scale(1.03); }}
        .sky-hero-text {{ position: absolute; bottom: 0; width: 100%; padding: 40px 5%; background: linear-gradient(transparent, rgba(0,0,0,0.9)); color: #fff; box-sizing: border-box; }}
        .sky-hero-text h3 {{ font-size: 26px; margin: 10px 0; font-weight: 900; line-height: 1.5; }}
        .sky-label-live {{ background: #ed1c24; padding: 2px 10px; font-size: 12px; font-weight: bold; border-radius: 2px; }}

        /* قائمة الأخبار (التصميم الأفقي مثل الصورة) */
        .sky-list {{ max-width: 1100px; margin: 20px auto; padding: 0 15px; }}
        .sky-item-card {{ border-bottom: 1px solid #f0f0f0; padding: 15px 0; }}
        .sky-item-card a {{ text-decoration: none; }}
        .sky-card-flex {{ display: flex; gap: 20px; align-items: flex-start; }}
        .sky-card-img {{ width: 180px; height: 110px; flex-shrink: 0; overflow: hidden; border-radius: 4px; }}
        .sky-card-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .sky-card-info h3 {{ font-size: 17px; color: #222; margin: 0 0 10px; line-height: 1.5; font-weight: 700; transition: 0.3s; }}
        .sky-card-info:hover h3 {{ color: #ed1c24; }}
        .sky-meta {{ font-size: 12px; color: #888; display: block; }}

        @media (max-width: 768px) {{
            .sky-hero-main {{ height: 40vh; }}
            .sky-hero-text h3 {{ font-size: 19px; }}
            .sky-card-img {{ width: 120px; height: 80px; }}
            .sky-card-info h3 {{ font-size: 14px; }}
        }}
    </style>
</head>
<body>
    <div class="header-sky">
        <a href="#" class="brand-sky">
            <span class="brand-black">stadium</span>
            <span class="brand-red">news 24</span>
        </a>
        <div class="live-tag">مباشر</div>
    </div>

    {news_html[:news_html.find('</div>', news_html.find('sky-hero-main'))+6]}

    <div class="sky-list">
        <h2 style="border-right: 5px solid #ed1c24; padding-right: 15px; font-size: 20px; margin-bottom: 25px;">آخر الأخبار الرياضية</h2>
        {news_html[news_html.find('</div>', news_html.find('sky-hero-main'))+6:]}
    </div>

    <footer style="background: #111; color: #fff; padding: 50px 20px; text-align: center; border-top: 5px solid #ed1c24;">
        <div style="font-size: 26px; font-weight: 900; margin-bottom: 10px;">stadium news 24</div>
        <p style="font-size: 12px; opacity: 0.6;">تغطية عالمية شاملة بمصداقية عالية</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_sky_rt_fusion()
