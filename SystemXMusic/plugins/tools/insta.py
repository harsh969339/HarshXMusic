# MADE BY SYSTEM (@APNA_SYSTEM) #dont change anything 

import re
import html
import aiohttp
from pyrogram import Client, filters
from urllib.parse import quote
from SystemXMusic import app

async def fetch_instagram_data(insta_url: str):
    if not insta_url:
        return {'status': 'error', 'message': 'Missing Instagram URL'}

    encoded_url = quote(insta_url)
    target_url = f"https://snapdownloader.com/tools/instagram-reels-downloader/download?url={encoded_url}"

    async with aiohttp.ClientSession() as session:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            async with session.get(target_url, headers=headers, timeout=30) as resp:
                if resp.status != 200:
                    return {'status': 'error', 'message': 'Failed to fetch data'}
                response = await resp.text()
        except Exception as e:
            return {'status': 'error', 'message': f'Error fetching data: {str(e)}'}

    video_match = re.search(r'<a[^>]+href="([^"]+\.mp4[^"]*)"[^>]*>', response)
    video_url = html.unescape(video_match.group(1)) if video_match else ''

    if video_url:
        return {
            'status': 'success',
            'video': video_url
        }
    else:
        return {'status': 'error', 'message': 'Unable to extract video'}

@app.on_message(filters.command(["insta", "instagram"]))
async def instagram_downloader(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide an Instagram URL!\nExample: /insta https://www.instagram.com/reel/...")
        return

    url = message.command[1]
    await message.reply_text("Processing your Instagram URL...")

    result = await fetch_instagram_data(url)

    if result['status'] == 'success':
        try:
            await message.reply_video(
                video=result['video'],
                caption="Downloaded from Instagram!"
            )
        except Exception as e:
            await message.reply_text(f"Failed to send video: {str(e)}")
    else:
        await message.reply_text(f"Error: {result['message']}")
