import streamlit as st
import json
import hashlib
import random
import hmac
import asyncio
import aiohttp
import re
import uuid
import os
from urllib.parse import urlparse, parse_qs

# --- خوارزمية Gorgon الأصلية ---
class Gorgon:
    def __init__(self):
        self.key, self.aid, self.iv = "97551682", "1233", "7263291a"
    def Hrr(self, n):
        out = []
        while True:
            b = n & 0x7F
            n >>= 7
            if n: out.append(b | 0x80)
            else:
                out.append(b)
                break
        return bytes(out)
    def vgeta(self, num, data): return self.Hrr((num << 3) | 2) + self.Hrr(len(data)) + data
    def Quick(self, num, s): return self.vgeta(num, s.encode() if isinstance(s, str) else s)
    def Enc(self, num, TikTok, url=None):
        if TikTok is None and url: TikTok = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
        if TikTok is None: return b""
        if isinstance(TikTok, dict): TikTok = json.dumps(TikTok, separators=(",", ":"))
        return self.Quick(num, TikTok)
    def Encoder(self, params=None, data=None):
        builded = self.Enc(1, params) + self.Enc(2, None) + self.Enc(3, data)
        msg = builded + self.iv.encode() + self.aid.encode()
        h = hmac.new(self.key.encode(), msg, hashlib.md5).hexdigest()       
        return f"8404{random.randint(0, 0xFFFF):04x}{random.randint(0, 0xFFFF):04x}0000{h}{random.randint(0, 0xFFFF):04x}"

# --- تصميم الواجهة الاحترافية ---
st.set_page_config(page_title="علــش @GX1GX1", page_icon="⚔️", layout="centered")

# إضافة تأثيرات CSS للألوان والخلفية
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# وضع صورة الإمام علي (ع) في المنتصف
# يمكنك استبدال الرابط برابط صورة أخرى إذا رغبت
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Calligraphy_Ali_bin_Abi_Talib.svg/1200px-Calligraphy_Ali_bin_Abi_Talib.svg.png", width=200)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>علــش @GX1GX1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>اللهم صل على محمد وآل محمد</p>", unsafe_allow_html=True)
st.write("---")

url_input = st.text_input("رابطـ الفيـديو URL⮕", placeholder="الصق الرابط هنا...")

if st.button("بدء التشغيل والتوكل على الله ✨"):
    if url_input:
        status_box = st.empty()
        counter_box = st.empty()
        
        class SayidWeb:
            def __init__(self, url):
                self.gg_encoder = Gorgon()
                self.url_input = url
                self.counter = 0
                self.lock = asyncio.Lock()

            async def worker(self, session, video_id):
                while True:
                    params = {
                        "device_id": str(random.randint(10**18, 10**19)),
                        "aid": "1340", "ts": str(int(random.random() * 10**10))
                    }
                    payload = {'item_id': video_id, 'aweme_type': "0"}
                    headers = {
                        'User-Agent': "com.zhiliaoapp.musically.go",
                        'x-gorgon': self.gg_encoder.Encoder(params=params, data=payload)
                    }
                    try:
                        async with session.post("https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/", json=payload, headers=headers, params=params) as resp:
                            if resp.status == 200:
                                async with self.lock:
                                    self.counter += 1
                                    counter_box.metric("عدد الطلبات المكتملة", f"🔥 {self.counter}")
                    except: pass
                    await asyncio.sleep(0.05)

            async def main_run(self):
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(self.url_input, allow_redirects=True) as resp:
                            match = re.search(r'/video/(\d+)', str(resp.url))
                            if match:
                                vid = match.group(1)
                                status_box.success(f"تم بنجاح! ID الفيديو: {vid}")
                                tasks = [asyncio.create_task(self.worker(session, vid)) for _ in range(15)]
                                await asyncio.gather(*tasks)
                            else: st.error("تأكد من صحة الرابط!")
                    except Exception as e: st.error(f"Error: {e}")

        app = SayidWeb(url_input)
        asyncio.run(app.main_run())
    else:
        st.warning("أدخل الرابط أولاً")
