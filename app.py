
from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import time
import requests
from datetime import datetime

# 👉 ใส่ Webhook ของคุณให้ถูกต้อง
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

# ✅ ฟังก์ชันแจ้งเตือน Slack
def send_slack_message(msg: str):
    data = {"text": msg}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=data)
        print(f"[Slack] Sent: {msg} | Status: {response.status_code}")
    except Exception as e:
        print(f"[Slack] Error: {e}")

# ✅ ฟังก์ชัน background ที่จะทำงานทุก 5 นาที
def background_loop():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_slack_message(f"📡 Background: แจ้งเตือนอัตโนมัติ {now}")
        time.sleep(5 * 60)  # ทุก 5 นาที

# ✅ Lifespan handler สำหรับ FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # สร้าง Thread และเริ่มทำงาน Background
    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()
    print("✅ Background thread started.")
    yield  # แอปเริ่มทำงาน
    # (ไม่มี shutdown logic)

# ✅ สร้าง FastAPI ด้วย lifespan
app = FastAPI(lifespan=lifespan)

# ✅ Root URL
@app.get("/")
def read_root():
    return {"msg": "✅ ระบบพร้อมทำงาน และแจ้งเตือน Slack อัตโนมัติทุก 5 นาที"}

# ✅ URL /click สำหรับกดแล้วแจ้งเตือนทันที
@app.get("/click")
def click_event():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_slack_message(f"👆 [CLICK] มีคนกด /click เวลา: {now}")
    return {"status": "ส่งแจ้งเตือนแล้ว", "timestamp": now}
