import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_kooora_clone():
    rss_url = "https://arabic.rt.com/rss/sport/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي
        my_link = "Https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')

        # كود HTML بتصميم كووورة الأصلي
        html_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>كووورة - Stadium 24</title>
    <style>
        body {{ background-color: #efefef; font-family: tahoma, arial, sans-serif; margin: 0; padding: 0; }}
        header {{ background-color: #fff; border-bottom: 5px solid #ffcc00; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; }}
        .logo {{ font-weight: bold; font-size: 28px; color: #ffcc00; text-decoration: none; font-style: italic; }}
        .logo span {{ color: #000; }}
        
        /* شريط المباريات */
        .matches-container {{ background: #fff; margin: 10px auto; max-width: 1000px; border: 1px solid #ccc; display: flex; overflow-x: auto; }}
        .match-box {{ min-width: 150px; border-left: 1px solid #eee; padding: 10px; text-align: center; font-size: 12px; }}
        .match-box .league {{ color: #999; font-size: 10px; display: block; }}
        .match-box .score {{ background: #fdf2c4; font-weight: bold; padding: 2px 5px; margin: 5px 0; display: inline-block; }}
        
        /* القائمة الرئيسية */
        nav {{ background: #333; color: #fff; padding: 8px 20px; font-size: 13px; font-weight: bold; }}
        nav span {{ margin-left: 20px; cursor: pointer; }}
        .live-icon {{ color: #ffcc00; }}

        /* الأخبار */
        .content-wrapper {{ max-width: 1000px; margin: 10px auto; display: flex; gap: 10px; }}
        .main-news {{ background: #fff; flex: 3; border: 1px solid #ccc; padding: 10px; }}
        .news-entry {{ border-bottom: 1px solid #eee; padding: 10px 0; display: flex; gap: 10px; }}
        .news-entry img {{ width: 150px; height: 100px; object-fit: cover; border: 1px solid #ddd; }}
        .news-entry h3 {{ margin: 0; font-size: 16px; color: #003366; }}
        .news-entry a {{ text-decoration: none; }}
        
        /* الإعلانات */
        .ad-banner {{ background: #fffde7; border: 1px solid #ffe58f; padding: 10px; text-align: center; margin-bottom: 10px; font-size: 14px; font-weight: bold; }}
        .ad-link {{ color: #d4a017; text-decoration: none; }}

        @media (max-width: 600px) {{
            .content-wrapper {{ flex-direction: column; }}
            .news-entry img {{ width: 100px; height: 70px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">K<span>OOORA</span></a>
        <div style="font-size: 12px;">{datetime.now().strftime("%d مارس 2026")}</div>
    </header>
    
    <nav>
        <span class="live-icon">● مباشر</span>
        <span>مباريات اليوم</span>
        <span>أخبار</span>
        <span>مسابقات</span>
    </nav>

    <div class="matches-container">
        <div class="match-box"><span class="league">الدوري الإسباني</span><div>ريال مدريد</div><span class="score">2 - 0</span><div>سيلتا فيغو</div></div>
        <div class="match-box"><span class="league">الدوري الإنجليزي</span><div>ليفربول</div><span class="score">1 - 1</span><div>مان سيتي</div></div>
        <div class="match-box"><span class="league">الدوري الإيطالي</span><div>يوفنتوس</div><span class="score">0 - 0</span><div>إنتر ميلان</div></div>
    </div>

    <div class="content-wrapper">
        <div class="main-news">
            <div class="ad-banner">
                <a href="{my_link}" target="_blank" class="ad-link">إعلان: حمل تطبيق كووورة الرسمي للحصول على التنبيهات مجاناً</a>
            </div>
            
            {" ".join([f'''
            <div class="news-entry">
                <img src="{item.find('enclosure').get('url') if item.find('enclosure') else ''}">
                <div>
                    <a href="{my_link}" target="_blank"><h3>{item.title.text}</h3></a>
                    <p style="font-size: 12px; color: #666;">{item.pubDate.text if item.pubDate else ''}</p>
                </div>
            </div>
            ''' for item in items[:15]])}
        </div>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_kooora_clone()
