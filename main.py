# -*- coding: utf-8 -*-
import asyncio
import os
import re
import random
import sys
import time
import requests
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from pyvirtualdisplay import Display

# --- ⚙️ SYSTEM CONFIGURATION ---
TABS_PER_MACHINE = 3 
sys.stdout.reconfigure(encoding='utf-8')

# --- 🚀 TELEGRAM REMOTE CONTROLLER CONFIGS ---
TG_TOKEN = "8608684111:AAFPQT_uz1oKHKC5jW9CqIzhZvT_SEzuvMY"
TG_CHAT_ID = "6837248644"

START_TIME = time.time()
TOTAL_SPAM_SENT = 500
CURRENT_STATUS_REPORT = "Initializing Engine..."
LATEST_PAGE_CONTEXT = None  

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ Telegram Push Error: {e}")

def send_telegram_photo(photo_path, caption):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TG_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
            requests.post(url, files=files, data=data, timeout=15)
    except Exception as e:
        print(f"❌ Telegram Photo Send Error: {e}")

def send_telegram_video(video_path, caption):
    """AUTOMATIC VIDEO SENDER: Yeh bina kisi manual intervention ke video file bot par upload kar dega"""
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendVideo"
        with open(video_path, 'rb') as video:
            files = {'video': video}
            data = {'chat_id': TG_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
            res = requests.post(url, files=files, data=data, timeout=45)
            if res.status_code == 200:
                print(f"✅ Video automatically delivered to Telegram from path: {video_path}")
            else:
                print(f"❌ Bot upload failed with status code: {res.status_code}")
    except Exception as e:
        print(f"❌ Automatic Telegram Video Send Error: {e}")

send_telegram_alert("🔱 *Phoenix Premium Ghost Engine Activated*\nAll systems initialized on GitHub Architecture servers!\nMonitoring & Remote Commands Listener is now *LIVE*.")

def get_current_role(thread_idx):
    elapsed_hours = int((time.time() - START_TIME) // 3600)
    if elapsed_hours % 2 == 0:
        return "FAST" if thread_idx == 1 else "SLOW"
    else:
        return "SLOW" if thread_idx == 1 else "FAST"

async def intercept_and_block_network(route):
    url = route.request.url.lower()
    resource_type = route.request.resource_type
    if (resource_type in ["image", "font", "media", "stylesheet"]) or \
       ("logging" in url) or ("analytics" in url) or ("metrics" in url) or ("graph.instagram.com" in url):
        await route.abort()
    else:
        await route.continue_()

async def telegram_command_listener():
    global TOTAL_SPAM_SENT, CURRENT_STATUS_REPORT, LATEST_PAGE_CONTEXT
    offset = 0
    print("📡 [System] Telegram Async Command Listener Hooked successfully.")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates?offset={offset}&timeout=10"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=12).json())
            
            if response.get("ok") and response.get("result"):
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    text = message.get("text", "").strip()
                    chat_id = str(message.get("chat", {}).get("id", ""))
                    
                    if chat_id != TG_CHAT_ID:
                        continue
                    
                    if text == "/status":
                        uptime_min = int((time.time() - START_TIME) // 60)
                        status_dashboard = (
                            f"📊 *CURRENT CLUSTER DASHBOARD*\n\n"
                            f"▪️ *Engine Condition:* Active & Running\n"
                            f"▪️ *Total Spam Batches Sent:* `{TOTAL_SPAM_SENT}` msgs\n"
                            f"▪️ *Server Uptime:* `{uptime_min}` minutes\n"
                            f"▪️ *Current Action Thread:* {CURRENT_STATUS_REPORT}"
                        )
                        send_telegram_alert(status_dashboard)
                        
                    elif text == "/screenshot":
                        if LATEST_PAGE_CONTEXT and not LATEST_PAGE_CONTEXT.is_closed():
                            screenshot_path = "live_state.png"
                            try:
                                await LATEST_PAGE_CONTEXT.screenshot(path=screenshot_path)
                                send_telegram_photo(screenshot_path, "📸 *Live Core Engine Visual Proof*\nThis is what is currently running inside the hidden browser window.")
                                if os.path.exists(screenshot_path):
                                    os.remove(screenshot_path)
                            except Exception as screenshot_err:
                                send_telegram_alert(f"❌ Could not capture viewport state: `{screenshot_err}`")
                        else:
                            send_telegram_alert("❌ *Screenshot Refused:* No active webpage instance running at this exact second. Try again in a bit.")
                            
        except Exception as listener_err:
            print(f"Telegram Listener loop event: {listener_err}")
            
        await asyncio.sleep(3)

async def run_advanced_human_behavior(context, machine_id, thread_idx, run_duration_seconds):
    global CURRENT_STATUS_REPORT, LATEST_PAGE_CONTEXT
    print(f"🎬 [ID {thread_idx}] Entering Deep Human Cooldown Profiling...")
    try:
        page = await context.new_page()
        LATEST_PAGE_CONTEXT = page
        await page.route("**/*", intercept_and_block_network)
        await page.goto("https://www.instagram.com/reels/", wait_until="load", timeout=30000)
        
        start_time = time.time()
        while time.time() - start_time < run_duration_seconds:
            CURRENT_STATUS_REPORT = f"ID {thread_idx} surfing Reels to build Trust Score."
            await page.wait_for_timeout(random.uniform(4000, 8000))
            
            dice_roll = random.random()
            if dice_roll < 0.3:  
                try: await page.mouse.dblclick(x=random.randint(150, 250), y=random.randint(100, 200))
                except: pass
            elif dice_roll < 0.5:  
                try:
                    await page.goto("https://www.instagram.com/", wait_until="commit")
                    await page.wait_for_timeout(random.uniform(3000, 5000))
                    await page.goto("https://www.instagram.com/reels/", wait_until="commit")
                except: pass
                
            await page.keyboard.press("ArrowDown")
            
        await page.close()
    except Exception as e:
        print(f"⚠️ [ID {thread_idx}] Cooldown exception skipped: {e}")

async def exact_one_minute_human_behavior(context, machine_id, thread_idx):
    try:
        reels_page = await context.new_page()
        await reels_page.goto("https://www.instagram.com/reels/", wait_until="commit", timeout=20000)
        start_time = time.time()
        while time.time() - start_time < 60:
            await reels_page.wait_for_timeout(random.uniform(3000, 5000))
            await reels_page.keyboard.press("ArrowDown")
        await reels_page.close()
    except: pass

async def run_strike(thread_idx, cookie, target_id, target_name, machine_id):
    global TOTAL_SPAM_SENT, CURRENT_STATUS_REPORT, LATEST_PAGE_CONTEXT
    async with async_playwright() as p:
        user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
        ]
        profile_path = os.path.join(os.getcwd(), f"n_{thread_idx}_{machine_id}")
        video_dir = os.path.join(os.getcwd(), f"recordings_{thread_idx}_{machine_id}")
        os.makedirs(video_dir, exist_ok=True)
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=True,
            user_agent=random.choice(user_agents),
            viewport={'width': 400, 'height': 800}, 
            record_video_dir=video_dir,              # 🎥 RECORDING STATE ENABLED AUTOMATICALLY
            record_video_size={'width': 400, 'height': 800},
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        await Stealth().apply_stealth_async(context)

        await context.add_init_script("""
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => Math.floor(Math.random() * 4) + 4 });
            Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
        """)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{
            'name': 'sessionid', 'value': sid.strip(), 
            'domain': '.instagram.com', 'path': '/', 'secure': True, 'httpOnly': True
        }])

        strike_script = """
            (name, delay, maxSpam) => {
                const getBlock = () => {
                    const emojis = ["💙", "❤️", "💚", "💛", "💜", "🖤", "🤍", "🤎", "🧡", "💖"];
                    const phrases = [
                        "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ 𝙼𝐀𝙳𝐀𝚁𝐂𝙷𝐎𝙳🍃✮",
                        "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ 𝙱𝐀𝚄𝐍𝙰🌿✮",
                        "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ 𝐓ᴇʀɪ ᴍᴀ 𝑺ᴀᴛʀᴀɴɢɪ 𝐑ᴀɴᴅ ♪",
                        "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ Tᴇʀᴀ Bᴀᴀᴘ x𝐀 ɴ ᴋ ɪ ᴛ ——➤(🎀)"];
                    const baseLine = phrases[Math.floor(Math.random() * phrases.length)];
                    const currentEmoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const dynamicMarker = Math.random().toString(36).substring(2, 5); 
                    const line = baseLine + " " + currentEmoji + " [" + dynamicMarker + "] ࿐";
                    let text = "";
                    for(let i = 0; i < 10; i++) { text += line + "\\n\\n\\n\\n"; }
                    return text;
                }
                window.currentSpamCount = 0;
                const pulse = () => {
                    if (window.currentSpamCount >= maxSpam) return;
                    const box = document.querySelector('div[role="textbox"]') || document.querySelector('[contenteditable="true"]');
                    if (box) {
                        const text = getBlock();
                        const dataTransfer = new DataTransfer();
                        dataTransfer.setData('text/plain', text);
                        const pasteEvent = new ClipboardEvent('paste', { clipboardData: dataTransfer, bubbles: true, cancelable: true });
                        box.focus();
                        box.dispatchEvent(pasteEvent);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        setTimeout(() => {
                            let sendBtn = Array.from(document.querySelectorAll('div[role="button"], button')).find(el => el.textContent.trim() === 'Send');
                            if (!sendBtn) sendBtn = document.querySelector('div[aria-label="Send"]');
                            if (sendBtn) { sendBtn.click(); window.currentSpamCount++; }
                        }, 5); 
                    }
                    setTimeout(() => { pulse(); }, delay);
                }
                pulse();
            }
        """

        while True:
            try:
                role = get_current_role(thread_idx)
                
                if role == "FAST":
                    pulse_delay = 50  
                    target_spam_limit = random.randint(300, 500)
                    
                    send_telegram_alert(f"🚀 *[Machine {machine_id}] ID {thread_idx}* started FAST Injection mode. Capture engine recording automatically.")

                    pages = []
                    for i in range(TABS_PER_MACHINE):
                        pg = await context.new_page()
                        LATEST_PAGE_CONTEXT = pg  
                        await pg.route("**/*", intercept_and_block_network)
                        try:
                            await pg.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="commit", timeout=20000)
                            await pg.wait_for_timeout(3000)
                            await pg.evaluate(strike_script, [target_name, pulse_delay, target_spam_limit])
                            pages.append(pg)
                        except Exception as e:
                            print(f"⚠️ Tab launch error: {e}")

                    reached = False
                    start_monitor = time.time()
                    while not reached and (time.time() - start_monitor < 900):
                        CURRENT_STATUS_REPORT = f"ID {thread_idx} performing rapid injection loops."
                        await asyncio.sleep(5)
                        for pg in pages:
                            try:
                                count = await pg.evaluate("window.currentSpamCount")
                                if count and count >= target_spam_limit:
                                    reached = True
                                    break
                            except: pass
                    
                    for pg in pages: 
                        try:
                            count = await pg.evaluate("window.currentSpamCount")
                            if count: TOTAL_SPAM_SENT += count
                        except: pass

                    # 🎬 Extract video pointers before killing the tab viewports
                    video_files = []
                    for pg in pages:
                        try:
                            v_file = await pg.video.path()
                            if v_file:
                                video_files.append(v_file)
                        except: pass

                    # Terminate tabs to complete file generation
                    for pg in pages: 
                        try: await pg.close()
                        except: pass
                    
                    # 🚀 AUTOMATIC FILE SYSTEM CHECK & AUTO-SEND PUSH LOGIC
                    await asyncio.sleep(3)  # Safe buffer delay to let filesystem flush mp4 streams
                    for idx, path in enumerate(video_files):
                        if os.path.exists(path) and os.path.getsize(path) > 0:
                            send_telegram_video(
                                path, 
                                f"🎥 *Automatic Engine Capture - Tab {idx+1}*\n[Machine {machine_id}] Thread {thread_idx} automatically recorded and delivered proof video of the injection flow inside target GC."
                            )
                            try:
                                os.remove(path) # Cleanup to avoid space crash
                            except: pass
                    
                    await exact_one_minute_human_behavior(context, machine_id, thread_idx)
                    send_telegram_alert(f"✅ *[Machine {machine_id}] ID {thread_idx}* batch loop done. Resting context.")
                    await asyncio.sleep(random.randint(10, 25))

                else:
                    cooldown_session_duration = random.randint(180, 360) 
                    send_telegram_alert(f"💤 *[Machine {machine_id}] ID {thread_idx}* resting in SLOW mode for {cooldown_session_duration}s.")
                    await run_advanced_human_behavior(context, machine_id, thread_idx, cooldown_session_duration)
                    await asyncio.sleep(random.randint(60, 120))

            except Exception as e:
                send_telegram_alert(f"⚠️ *[Machine {machine_id}] Engine error state loop rebooting in 15s...*")
                await asyncio.sleep(15)

        await context.close()

async def main():
    cookie1 = os.environ.get("INSTA_COOKIE_1")
    cookie2 = os.environ.get("INSTA_COOKIE_2")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    m_id = os.environ.get("MACHINE_ID", "1")
    
    asyncio.create_task(telegram_command_listener())
    
    display = Display(visible=0, size=(1024, 768))
    display.start()
    try:
        if cookie1 and cookie2 and target_id:
            await asyncio.gather(
                run_strike(1, cookie1, target_id, target_name, m_id),
                run_strike(2, cookie2, target_id, target_name, m_id)
            )
    finally:
        display.stop()

if __name__ == "__main__":
    asyncio.run(main())
    
