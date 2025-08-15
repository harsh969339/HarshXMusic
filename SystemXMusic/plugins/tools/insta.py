# MADE BY SYSTEM (@APNA_SYSTEM) #dont change anything 

import re
import html
import asyncio
import aiohttp
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import quote
from SystemMusic import app

D_ANI = ["🔍 Analyzing...", "🔗 Connecting...", "📊 Fetching...", "⚡ Extracting..."]
P_ANI = [f"📥 [{i*'█'}{(8-i)*'▱'}] {i*12.5}%" for i in range(9)]
U_ANI = ["📤 Preparing...", "📤 Uploading..."]
S_EMOJI = ["🎉", "✨", "🔥"]

async def fetch_instagram_data(insta_url: str):
    if not insta_url or 'instagram.com' not in insta_url:
        return {'status': 'error', 'message': 'Invalid Instagram URL'}

    encoded_url = quote(insta_url)
    target_url = f"https://snapdownloader.com/tools/instagram-reels-downloader/download?url={encoded_url}"

    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://snapdownloader.com/'
            }
            async with session.get(target_url, headers=headers, timeout=30) as resp:
                if resp.status != 200:
                    return {'status': 'error', 'message': f'HTTP Error: {resp.status}'}
                response = await resp.text()
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Network error: {str(e)}'}
        except asyncio.TimeoutError:
            return {'status': 'error', 'message': 'Request timed out'}

    patterns = [
        r'"video_url":"([^"]+\.mp4[^"]*)"',
        r'src="([^"]+\.mp4[^"]*)"',
        r'<a[^>]+href="([^"]+\.mp4[^"]*)"[^>]*>'
    ]
    
    video_url = None
    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            video_url = html.unescape(match.group(1))
            break

    if video_url:
        return {
            'status': 'success',
            'video': video_url,
            'quality': 'HD'
        }
    else:
        return {'status': 'error', 'message': 'Unable to extract video URL'}

async def ani_msg(m: Message, a: list, d: float = 0.5):
    am = None
    for f in a:
        if am is None:
            am = await m.reply_text(f)
        else:
            await am.edit_text(f)
        await asyncio.sleep(d)
    return am

async def del_msgs(ms: list, d: int = 8):
    await asyncio.sleep(d)
    for m in ms:
        try:
            if m and not m.empty:
                await m.delete()
        except:
            pass

def is_insta_url(t: str) -> bool:
    return bool(t and re.search(r'(?:https?://)?(?:www\.)?(?:instagram\.com|instagr\.am)/(?:p|reel|tv)/[\w-]+/?', t, re.I))

@app.on_message(filters.text & (filters.private | filters.group))
async def auto_insta(c: Client, m: Message):
    if not is_insta_url(m.text):
        return
    u = re.search(r'https?://[^\s]+', m.text).group(0)
    ms = [m]
    try:
        am = await ani_msg(m, D_ANI, 0.4)
        if am:
            ms.append(am)
        pm = await ani_msg(m, P_ANI, 0.3)
        if pm:
            ms.append(pm)
        r = await fetch_instagram_data(u)
        if r['status'] == 'success':
            um = await ani_msg(m, U_ANI, 0.4)
            if um:
                ms.append(um)
            e = random.choice(S_EMOJI)
            await m.reply_video(r['video'], caption=e, supports_streaming=True)
            sm = await m.reply_text(f"{e} Done! {r['quality']}")
            ms.append(sm)
        else:
            em = await m.reply_text(f"❌ {r['message']}")
            ms.append(em)
    except Exception as e:
        em = await m.reply_text(f"🚨 Error: {str(e)[:50]}...")
        ms.append(em)
    finally:
        asyncio.create_task(del_msgs(ms))
