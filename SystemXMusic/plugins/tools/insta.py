# MADE BY SYSTEM (@APNA_SYSTEM) #dont change anything 

import re,html,asyncio,aiohttp,random
from pyrogram import Client,filters
from pyrogram.types import Message
from urllib.parse import quote
from SystemXMusic import app

D_ANI=["🔍 Analyzing...","🔗 Connecting...","📊 Fetching...","⚡ Extracting..."]
P_ANI=[f"📥 [{i*'█'}{(8-i)*'▱'}] {i*12.5}%" for i in range(9)]
U_ANI=["📤 Preparing...","📤 Uploading..."]
S_EMOJI=["🎉","✨","🔥"]

async def fetch_insta(url):
 if not url or 'instagram.com' not in url:
  return {'status':'error','message':'Invalid URL'}
 async with aiohttp.ClientSession() as s:
  try:
   async with s.get(f"https://snapdownloader.com/tools/instagram-reels-downloader/download?url={quote(url)}",headers={'User-Agent':'Mozilla/5.0 Chrome/91'},timeout=10) as r:
    if r.status==200:
     t=await r.text()
     for p in [r'"video_url":"([^"]+\.mp4[^"]*)"',r'src="([^"]+\.mp4[^"]*)"']:
      if m:=re.search(p,t):
       return {'status':'success','video':html.unescape(m.group(1)),'quality':'HD'}
  except:
   pass
 return {'status':'error','message':'Extraction failed'}

async def ani_msg(m:Message,a:list,d:float=.5):
 am=None
 for f in a:
  if am is None:
   am=await m.reply_text(f)
  else:
   await am.edit_text(f)
  await asyncio.sleep(d)
 return am

async def del_msgs(ms:list,d:int=8):
 await asyncio.sleep(d)
 for m in ms:
  try:
   if m and not m.empty:
    await m.delete()
  except:
   pass

def is_insta_url(t:str)->bool:
 return bool(t and re.search(r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/[\w-]+/?',t,re.I))

@app.on_message(filters.text&(filters.private|filters.group))
async def auto_insta(c:Client,m:Message):
 if not is_insta_url(m.text):
  return
 u=re.search(r'https?://[^\s]+',m.text).group(0)
 ms=[m]
 try:
  am=await ani_msg(m,D_ANI,.4)
  if am:ms.append(am)
  pm=await ani_msg(m,P_ANI,.3)
  if pm:ms.append(pm)
  r=await fetch_insta(u)
  if r['status']=='success':
   um=await ani_msg(m,U_ANI,.4)
   if um:ms.append(um)
   e=random.choice(S_EMOJI)
   await m.reply_video(r['video'],caption=e,supports_streaming=True)
   sm=await m.reply_text(f"{e} Done! {r['quality']}")
   ms.append(sm)
  else:
   em=await m.reply_text(f"❌ {r['message']}")
   ms.append(em)
 except Exception as e:
  em=await m.reply_text(f"🚨 Error: {str(e)[:50]}...")
  ms.append(em)
 finally:
  asyncio.create_task(del_msgs(ms))

@app.on_message(filters.command(["insta","ig"]))
async def manual_insta(c:Client,m:Message):
 if len(m.command)<2:
  hm=await m.reply_text("📱 Send URL or /insta [URL]")
  asyncio.create_task(del_msgs([m,hm],10))
  return
 fm=type('obj',(),{'text':m.command[1],'reply_text':m.reply_text,'reply_video':m.reply_video})
 await auto_insta(c,fm)
 asyncio.create_task(del_msgs([m],5))
