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

# --- خوارزمية Gorgon الأصلية (كاملة وبدون أي تعديل) ---
class Gorgon:
    def __init__(self):
        self.key = "97551682"
        self.aid = "1233"
        self.iv  = "7263291a"

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

    def vgeta(self, num, data):
        ttxp = (num << 3) | 2
        return self.Hrr(ttxp) + self.Hrr(len(data)) + data

    def Quick(self, num, s):
        s = s.encode() if isinstance(s, str) else s
        return self.vgeta(num, s)

    def Enc(self, num, TikTok, url=None):
        if TikTok is None and url:
            TikTok = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
        if TikTok is None: return b""
        if isinstance(TikTok, dict):
            TikTok = json.dumps(TikTok, separators=(",", ":"))
        elif not isinstance(TikTok, str):
            TikTok = str(TikTok)
        return self.Quick(num, TikTok)

    def build(self, params=None, cookies=None, data=None, payload=None, url=None):
        AHMED = b""
        AHMED += self.Enc(1, params, url)
        AHMED += self.Enc(2, cookies)
        AHMED += self.Enc(3, data or payload)
        return AHMED

    def Encoder(self, params=None, cookies=None, data=None, payload=None, url=None):
        builded = self.build(params, cookies, data, payload, url)
        msg = builded + self.iv.encode() + self.aid.encode()
        h = hmac.new(self.key.encode(), msg, hashlib.md5).hexdigest()       
        a = f"{random.randint(0, 0xFFFF):04x}"
        b = f"{random.randint(0, 0xFFFF):04x}"
        c = f"{random.randint(0, 0xFFFF):04x}"
        final = f"8404{a}{b}0000{h}{c}"
        return final

# --- تنسيق واجهة الويب الاحترافية ---
st.set_page_config(page_title="علــش @GX1GX1", page_icon="⚔️", layout="centered")

st.markdown("""
    <style>
    /* خلفية داكنة فخمة */
    .stApp { background: #0e1117; color: white; }
    
    /* حركة النبض للصورة */
    @keyframes pulse-gold {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }

    .user-avatar {
        display: block; margin: 20px auto;
        border: 4px solid #FFD700; border-radius: 50%;
        animation: pulse-gold 2.5s infinite;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }

    /* تنسيق زر "بدأ" */
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(45deg, #FFD700, #DAA520);
        color: black; font-weight: 900; border: none; height: 3.5em;
        transition: 0.4s;
    }
    .stButton>button:hover { transform: translateY(-3px); filter: brightness(1.1); }

    /* تنسيق حقل الإدخال والعداد */
    .stTextInput>div>div>input { background-color: #1a1a1a; color: #FFD700; border: 1px solid #DAA520; }
    div[data-testid="stMetricValue"] { color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# عرض الصورة الشخصية فقط (بدون اللوغو النصي)
st.markdown(f'<img src="https://i.ibb.co/cXgRkRTf/6e37bd54624a0d987f097ff5bb04a58e.jpg" class="user-avatar" width="170">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>عـلــش | @GX1GX1</h1>", unsafe_allow_html=True)
st.write("---")

# الإدخال والتشغيل
url_input = st.text_input("أدخل الرابط", placeholder="URL⮕")

if st.button("بدأ"):
    if url_input:
        counter_display = st.empty()
        status_info = st.empty()
        
        class AppRunner:
            def __init__(self, url):
                self.encoder = Gorgon()
                self.url = url
                self.count = 0

            async def start_worker(self, session, vid):
                while True:
                    params = {
                        "manifest_version_code": "350302",
                        "device_id": str(random.randint(10**18, 10**19)),
                        "aid": "1340", "ts": str(int(random.random() * 10**10))
                    }
                    payload = {'item_id': vid, 'aweme_type': "0"}
                    g_hex = self.encoder.Encoder(params=params, data=payload)
                    headers = {'User-Agent': "com.zhiliaoapp.musically.go", 'x-gorgon': g_hex}
                    try:
                        async with session.post("https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/", data=payload, headers=headers, params=params) as r:
                            if r.status == 200:
                                self.count += 1
                                counter_display.metric("إجمالي الطلبات الناجحة", f"🚀 {self.count}")
                    except: pass
                    await asyncio.sleep(0.01)

            async def main(self):
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(self.url, allow_redirects=True) as r:
                            match = re.search(r'/video/(\d+)', str(r.url))
                            if match:
                                vid = match.group(1)
                                status_info.success(f"تم الربط: {vid}")
                                tasks = [asyncio.create_task(self.start_worker(session, vid)) for _ in range(15)]
                                await asyncio.gather(*tasks)
                    except: st.error("حدث خطأ!")

        runner = AppRunner(url_input)
        asyncio.run(runner.main())
