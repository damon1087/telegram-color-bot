import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# === 替換成你自己的 Bot Token 和 Chat ID ===
BOT_TOKEN = '7549661136:AAHBzu6M1HAssF1F75ucPUe_2szhu00X5HA'
CHAT_ID = '71682699'

# === 計算明天日期 ===
tomorrow = datetime.now() + timedelta(days=1)
date_display = tomorrow.strftime('%Y-%m-%d')

# === 抓取漢程網穿衣顏色 ===
url = 'https://m.life.httpcn.com/wxchuanyi/'
res = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

# 找出前2個與第5個穿衣顏色區塊
sections = soup.select('.box_warp .today_box')

def extract_colors(text_block):
    lines = text_block.get_text(strip=True).split('：')
    return lines[1].replace('、', ', ') if len(lines) > 1 else "無"

daji_color = extract_colors(sections[0])
ciji_color = extract_colors(sections[1])
jiyi_color = extract_colors(sections[4])

# === 組合訊息內容 ===
message = f"""📅 明日穿衣顏色建議（{date_display}）： 
🎨 大吉色：{daji_color}
🎨 次吉色：{ciji_color}
⛔️ 忌穿顏色：{jiyi_color}"""

# === 傳送到 Telegram ===
send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message
}
requests.post(send_url, data=payload)
