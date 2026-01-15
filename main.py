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

# --- خوارزمية Gorgon (كودك الأصلي بدون حذف أي حرف) ---
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
            if n:
                out.append(b | 0x80)
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
        if TikTok is None:
            return b""
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

# --- واجهة التطبيق (تم تعديل العرض فقط ليعمل على الويب) ---
st.set_page_config(page_title="علــش @GX1GX1", layout="centered")

# عرض اللوغو الأصلي الخاص بك
st.code(r'''::::::::::.:::.:::::::::::::::::::::::::::::.::.:::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::......    ...::::::::::::::::::::
:::::::::::::::::::.                ....:::::::::::::::
::::::::::::::::.                      .:::::::::::::::
::::::::::::::..                        .::::::::::::::
:::::::::::::.                          .::::::::::::::
:::::::::::.                            .::::::::::::::
:::::::::::.                     .     ::::::::::::::::
::::::::::.                      ..    :::::::....:::::
::::::::::.                 ..: ...    :::::........:::
::::::::::...               :-:  :-:.  .::::........:::
:::::::::::::..  .          .-.  :---::.::::::....:::::
:::::::::::::::..:                -----:...::::::::::::
::::::::::::::::::..               ::.     .:::::::::::
::::::::::::::::::::..                      .::::::::::
:::::::::::::::::::::::   ..:                 ..:::::::
::::::::::::::::::::::::::::.                    .:::::
:::::::::::::::::::::::::::.                       .:::
::::::..:....::::::::::::.                          .::
::::::..:....::::::::::.                            .::
::::....:....::::::::.                              .::
:::::..:::..::::::::.                                ::
:::::::::::::::::::.                                .::
''')

st.markdown("### علــش @GX1GX1")
st.write("---")

# بديل input() في الويب
url_input = st.text_input("رابطـ الفيـديو URL⮕")

if st.button("بدء التشغيل ✅"):
    if url_input:
        status_log = st.empty()
        counter_log = st.empty()
        
        # الكلاس الأساسي الخاص بك مع دمج الوظائف
        class SayidWeb:
            def __init__(self, url):
                self.gg_encoder = Gorgon()
                self.url_input = url
                self.threads = 20 # تم تقليله لضمان استقرار السيرفر المجاني
                self.API = "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/"
                self.counter = 0
                self.lock = asyncio.Lock()

            def gen_dynamic_params(self):
                # جميع البيانات الأصلية الخاصة بك كما هي
                params = {
                    "manifest_version_code": "350302",
                    "_rticket": str(int(random.random() * 10**16)),
                    "app_language": "en",
                    "app_type": "normal",
                    "iid": str(random.randint(7000000000000000000, 9000000000000000000)),
                    "channel": "googleplay",
                    "device_type": "RMX3941",
                    "language": "en",
                    "host_abi": "arm64-v8a",
                    "locale": "en",
                    "resolution": "1080*2290",
                    "openudid": str(uuid.uuid4().hex[:16]),
                    "update_version_code": "350302",
                    "ac2": "wifi5g",
                    "cdid": str(uuid.uuid4()),
                    "sys_region": "US",
                    "os_api": "34",
                    "timezone_name": "America/New_York",
                    "dpi": "480",
                    "carrier_region": "US",
                    "ac": "wifi",
                    "device_id": str(random.randint(7000000000000000000, 9000000000000000000)),
                    "os_version": "12",
                    "timezone_offset": "10800",
                    "version_code": "350302",
                    "app_name": "musically_go",
                    "ab_version": "35.3.2",
                    "version_name": "35.3.2",
                    "device_brand": "realme",
                    "op_region": "US",
                    "ssmix": "a",
                    "device_platform": "android",
                    "build_number": "35.3.2",
                    "region": "US",
                    "aid": "1340",
                    "ts": str(int(random.random() * 10**10))
                }
                return params

            async def worker(self, session, video_id):
                while True:
                    params = self.gen_dynamic_params()
                    payload = {
                        'pre_item_playtime': "",
                        'first_install_time': "1737204216",
                        'item_id': video_id,
                        'is_ad': "false",
                        'follow_status': "0",
                        'sync_origin': "false",
                        'follower_status': "0",
                        'action_time': str(int(random.random() * 10**10)),
                        'tab_type': "3",
                        'play_delta': "1",
                        'aweme_type': "0"
                    }
                    gorgon_hex = self.gg_encoder.Encoder(params=params, data=payload)
                    headers = {
                        'User-Agent': "com.zhiliaoapp.musically.go",
                        'Accept-Encoding': "gzip",
                        'x-gorgon': gorgon_hex,
                        'x-khronos': str(int(random.random() * 10**10)),
                        'Cookie': "store-idc=alisg; install_id=7516928038623151879; ttreq=1$5f3bc0fcb73296e39d74f6d161b1e2dfed2914e2;"
                    }
                    try:
                        async with session.post(self.API, data=payload, headers=headers, params=params) as response:
                            if response.status == 200:
                                json_data = await response.json()
                                if json_data.get("status_code") == 0:
                                    async with self.lock:
                                        self.counter += 1
                                        # بديل print() في الويب لعرض العداد
                                        counter_log.metric("الـسـرعة (عدد الطلبات)", self.counter)
                    except:
                        continue
                    await asyncio.sleep(0.01) # ضروري لاستقرار صفحة الويب

            async def main_run(self):
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(self.url_input, allow_redirects=True) as response:
                            full_url = str(response.url)
                        match = re.search(r'/video/(\d+)', full_url)
                        if match:
                            video_id = match.group(1)
                            status_log.success(f"تم الربط بنجاح! ID الفيديو: {video_id}")
                            tasks = [asyncio.create_task(self.worker(session, video_id)) for _ in range(self.threads)]
                            await asyncio.gather(*tasks)
                        else:
                            st.error("رابط غير صحيح!")
                    except Exception as e:
                        st.error(f"Error: {e}")

        # تشغيل الكلاس
        app = SayidWeb(url_input)
        asyncio.run(app.main_run())
    else:
        st.warning("يرجى إدخال الرابط أولاً")

