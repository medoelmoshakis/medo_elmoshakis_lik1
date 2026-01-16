import streamlit as st
import json
import hashlib
import random
import hmac
import asyncio
import aiohttp
import re
import uuid
from urllib.parse import urlparse, parse_qs

# --- خوارزمية Gorgon الأصلية (بدون أي تعديل) ---
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

# --- واجهة المستخدم الاحترافية ---
st.set_page_config(page_title="علــش @GX1GX1", page_icon="⚔️", layout="centered")

# إضافة تأثيرات CSS متقدمة
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp {
        background: radial-gradient(circle, #1a1a1a 0%, #080808 100%);
        color: #FFFFFF;
    }
    
    /* حركة النبض للصورة */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(218, 165, 32, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(218, 165, 32, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(218, 165, 32, 0); }
    }

    .img-container {
        display: flex;
        justify-content: center;
        margin: 20px auto;
        border: 4px solid #DAA520;
        border-radius: 50%;
        width: 180px;
        height: 180px;
        overflow: hidden;
        animation: pulse 3s infinite;
    }

    /* تنسيق زر "بدأ" */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: black;
        font-weight: 900;
        font-size: 1.2rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.4);
        background: linear-gradient(135deg, #B8860B 0%, #FFD700 100%);
    }

    /* تنسيق حقل الإدخال */
    .stTextInput>div>div>input {
        background-color: #262626;
        color: #FFD700;
        border: 1px solid #DAA520;
        text-align: center;
        border-radius: 10px;
    }

    /* تنسيق العداد */
    div[data-testid="stMetricValue"] {
        color: #FFD700;
        font-family: 'Courier New', Courier, monospace;
        background: rgba(218, 165, 32, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# عرض الصورة بتأثير الإطار المتحرك
st.markdown('<div class="img-container">', unsafe_allow_html=True)
st.image("https://i.ibb.co/cXgRkRTf/6e37bd54624a0d987f097ff5bb04a58e.jpg", width=180)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>عـلــش | @GX1GX1</h1>", unsafe_allow_html=True)
st.write("---")

# خانة الإدخال المعدلة
url_input = st.text_input("أدخل الرابط", placeholder="الصق رابط تيك توك هنا...")

# زر بدأ المعدل
if st.button("بدأ"):
    if url_input:
        status_box = st.empty()
        counter_box = st.empty()
        
        async def worker(session, video_id, gg):
            if 'count' not in st.session_state: st.session_state.count = 0
            while True:
                params = {"device_id": str(random.randint(10**18, 10**19)), "aid": "1340"}
                payload = {'item_id': video_id, 'aweme_type': "0"}
                headers = {'User-Agent': "com.zhiliaoapp.musically.go", 'x-gorgon': gg.Encoder(params=params, data=payload)}
                try:
                    async with session.post("https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/", json=payload, headers=headers, params=params) as resp:
                        if resp.status == 200:
                            st.session_state.count += 1
                            counter_box.metric("إجمالي الطلبات", f"🚀 {st.session_state.count}")
                except: pass
                await asyncio.sleep(0.01)

        async def main():
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url_input, allow_redirects=True) as r:
                        match = re.search(r'/video/(\d+)', str(r.url))
                        if match:
                            vid = match.group(1)
                            status_box.markdown(f"<p style='color: #00ff00; text-align: center;'>✅ تم الاتصال بـ ID: {vid}</p>", unsafe_allow_html=True)
                            gg = Gorgon()
                            tasks = [asyncio.create_task(worker(session, vid, gg)) for _ in range(15)]
                            await asyncio.gather(*tasks)
                        else:
                            st.error("الرابط غير مدعوم!")
                except:
                    st.error("حدث خطأ في الاتصال!")

        asyncio.run(main())
    else:
        st.warning("يرجى وضع رابط أولاً!")
