import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# 從環境變數取得 Telegram Token & Chat ID
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

tomorrow = datetime.now() + timedelta(days=1)
date_display = tomorrow.strftime('%Y-%m-%d')

# 漢程網資料
url = 'https://m.life.httpcn.com/wxchuanyi/'
res = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

sections = soup.select('.box_warp .today_box')

def extract_colors(text_block):
    lines = text_block.get_text(strip=True).split('：')
    return lines[1].replace('、', ', ') if len(lines) > 1 else "無"

daji_color = extract_colors(sections[0])
ciji_color = extract_colors(sections[1])
jiyi_color = extract_colors(sections[4])

message = f"""📅 明日穿衣顏色建議（{date_display}）： 
🎨 大吉色：{daji_color}
🎨 次吉色：{ciji_color}
⛔️ 忌穿顏色：{jiyi_color}"""

# 發送到 Telegram
send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message
}
requests.post(send_url, data=payload)
