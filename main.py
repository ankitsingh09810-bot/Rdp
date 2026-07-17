# -*- coding: utf-8 -*-
import asyncio
import os
import re
import random
import sys
import time
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from pyvirtualdisplay import Display

# --- ⚙️ SHIELD PILLAR SETTINGS ---
TABS_PER_MACHINE = 2    
sys.stdout.reconfigure(encoding='utf-8')

# Script start time to calculate hours for swapping roles
START_TIME = time.time()

def get_current_role(thread_idx):
    """
    Har 1 ghante (3600 seconds) baad roles switch honge.
    Thread 1 pehle ghante FAST chalega, Thread 2 strictly SLOW (Human Behavior Cooldown).
    Dusre ghante roles swap ho jayenge.
    """
    elapsed_hours = int((time.time() - START_TIME) // 3600)
    if elapsed_hours % 2 == 0:
        return "FAST" if thread_idx == 1 else "SLOW"
    else:
        return "SLOW" if thread_idx == 1 else "FAST"

# --- 🎬 CONTINUOUS HUMAN BEHAVIOR FOR COOLDOWN ID ---
async def run_continuous_human_behavior(context, machine_id, thread_idx, run_duration_seconds):
    """
    Jab ID SLOW/COOLDOWN mode me hogi, toh yeh function run hoga.
    Yeh specify kiye gaye duration tak non-stop Instagram Reels dekhega, scroll karega aur likes karega.
    """
    print(f"🎬 [ID {thread_idx} | M {machine_id}] Active Role: SLOW Cooldown. Running Continuous Human Behavior...")
    try:
        reels_page = await context.new_page()
        await reels_page.goto("https://www.instagram.com/reels/", wait_until="load", timeout=25000)
        
        start_time = time.time()
        current_reel = 1
        
        while time.time() - start_time < run_duration_seconds:
            # Real viewing delay per reel (3 to 6 seconds stay duration)
            await reels_page.wait_for_timeout(random.uniform(3000, 6000))
            
            # 45% chance to like the reel
            if random.random() < 0.45:
                try:
                    await reels_page.mouse.dblclick(x=200, y=150)
                    print(f"❤️ [ID {thread_idx} | M {machine_id}] | Cooldown Reel {current_reel}: Liked.")
                except:
                    pass
                await reels_page.wait_for_timeout(random.uniform(600, 1500))
            
            # Scroll down to next reel
            await reels_page.keyboard.press("ArrowDown")
            current_reel += 1
            
        await reels_page.close()
        print(f"✅ [ID {thread_idx} | M {machine_id}] Cooldown Human Session Complete.")
    except Exception as e:
        print(f"⚠️ [ID {thread_idx} | M {machine_id}] Human behavior session ran into a minor issue: {e}")

# --- 🎬 SHORT COOLDOWN AFTER SPAM ---
async def exact_one_minute_human_behavior(context, machine_id, thread_idx):
    """
    Spam loop complete hone ke baad exact 60 seconds tak continuous reels dekhega.
    """
    print(f"🎬 [ID {thread_idx} | M {machine_id}] Cycle Target Reached! Launching Mandatory 1-Minute Cooldown...")
    try:
        reels_page = await context.new_page()
        await reels_page.goto("https://www.instagram.com/reels/", wait_until="load", timeout=25000)
        
        start_time = time.time()
        current_reel = 1
        
        while time.time() - start_time < 60:
            await reels_page.wait_for_timeout(random.uniform(2000, 5000))
            if random.random() < 0.4:
                try:
                    await reels_page.mouse.dblclick(x=200, y=150)
                except:
                    pass
                await reels_page.wait_for_timeout(random.uniform(500, 1200))
            await reels_page.keyboard.press("ArrowDown")
            current_reel += 1
            
        await reels_page.close()
        print(f"✅ [ID {thread_idx} | M {machine_id}] 1-Min Buffer Complete.")
    except Exception as e:
        print(f"⚠️ [ID {thread_idx} | M {machine_id}] Cooldown bypassed: {e}")

# --- 🔱 MAIN EXECUTION ENGINE ---
async def run_strike(thread_idx, cookie, target_id, target_name, machine_id):
    async with async_playwright() as p:
        user_agent = "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
        profile_path = os.path.join(os.getcwd(), f"n_{thread_idx}_{machine_id}")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=True,
            user_agent=user_agent,
            viewport={'width': 400, 'height': 300},
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu",
                "--blink-settings=imagesEnabled=false"
            ]
        )

        await Stealth().apply_stealth_async(context)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{
            'name': 'sessionid', 'value': sid.strip(), 
            'domain': '.instagram.com', 'path': '/', 'secure': True, 'httpOnly': True
        }])

        # ⚡ HIGH-SPEED TARGET COUNTER INJECTION SCRIPT (Optimized to 50ms)
        strike_script = """
            (name, delay, maxSpam) => {
                const getBlock = () => {
                    const emojis = ["💙", "❤️", "💚", "💛", "💜", "🖤", "🤍", "🤎", "🧡", "💖"];
                    const currentEmoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const line = "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ 𝚃𝙼𝙺🇨 " + currentEmoji + "་༘࿐";
                    
                    let text = "";
                    for(let i = 0; i < 10; i++) { 
                        text += line + "\\n\\n\\n\\n"; 
                    }
                    return text;
                }

                window.currentSpamCount = 0;
                const pulse = () => {
                    if (window.currentSpamCount >= maxSpam) {
                        console.log("LIMIT_REACHED");
                        return;
                    }

                    const box = document.querySelector('div[role="textbox"]') || 
                                document.querySelector('[contenteditable="true"]') ||
                                document.querySelector('textarea');
                                
                    if (box) {
                        const text = getBlock();
                        const dataTransfer = new DataTransfer();
                        dataTransfer.setData('text/plain', text);
                        
                        const pasteEvent = new ClipboardEvent('paste', {
                            clipboardData: dataTransfer,
                            bubbles: true,
                            cancelable: true
                        });
                        
                        box.focus();
                        box.dispatchEvent(pasteEvent);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        box.dispatchEvent(new Event('change', { bubbles: true }));
                        
                        setTimeout(() => {
                            let sendBtn = Array.from(document.querySelectorAll('div[role="button"], button')).find(el => 
                                el.textContent.trim() === 'Send' || el.innerText.trim() === 'Send'
                            );
                            
                            if (!sendBtn) {
                                sendBtn = document.querySelector('div[aria-label="Send"]') || 
                                          document.querySelector('form button[type="button"]');
                            }
                            
                            if (sendBtn) {
                                sendBtn.click();
                                window.currentSpamCount++;
                            }
                        }, 10); // Super fast 10ms click trigger after pasting
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
                    pulse_delay = 50  # Upgraded: Exact 50ms fast delay
                    target_spam_limit = random.randint(300, 500)
                    print(f"🚀 [ID {thread_idx} | M {machine_id}] Mode: FAST (Spam) | Target: {target_spam_limit} Msgs | Delay: {pulse_delay}ms.")

                    pages = []
                    for i in range(TABS_PER_MACHINE):
                        pg = await context.new_page()
                        try:
                            await pg.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="commit", timeout=20000)
                            await pg.wait_for_timeout(3000)
                            await pg.evaluate(strike_script, [target_name, pulse_delay, target_spam_limit])
                            pages.append(pg)
                        except Exception as e:
                            print(f"⚠️ [ID {thread_idx}] Tab load warning: {e}")

                    # Monitor Loop
                    reached = False
                    start_monitor = time.time()
                    while not reached and (time.time() - start_monitor < 900):
                        await asyncio.sleep(5)
                        for pg in pages:
                            try:
                                count = await pg.evaluate("window.currentSpamCount")
                                if count and count >= target_spam_limit:
                                    reached = True
                                    break
                            except:
                                pass
                    
                    # Clean up active spam tabs
                    for pg in pages: 
                        try: await pg.close()
                        except: pass
                    
                    # Short Cooldown after spam run
                    await exact_one_minute_human_behavior(context, machine_id, thread_idx)
                    
                    cycle_rest = random.randint(10, 25)
                    print(f"💤 [ID {thread_idx}] Fast cycle done. Resting for {cycle_rest}s...")
                    await asyncio.sleep(cycle_rest)

                else:
                    # STRICT SLOW MODE: Runs pure human behavior on Reels
                    # Randomly executes reels viewing sessions of 3 to 6 minutes duration
                    cooldown_session_duration = random.randint(180, 360) 
                    await run_continuous_human_behavior(context, machine_id, thread_idx, cooldown_session_duration)
                    
                    # Rest between human sessions
                    post_cooldown_rest = random.randint(60, 120)
                    print(f"💤 [ID {thread_idx}] Cooldown session done. Rest for {post_cooldown_rest}s...")
                    await asyncio.sleep(post_cooldown_rest)

            except Exception as e:
                print(f"⚠️ [ID {thread_idx} | M {machine_id}] Session Warning: {e}. Re-syncing in 15s...")
                await asyncio.sleep(15)

        await context.close()

async def main():
    cookie1 = os.environ.get("INSTA_COOKIE_1")
    cookie2 = os.environ.get("INSTA_COOKIE_2")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    m_id = os.environ.get("MACHINE_ID", "1")
    
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    try:
        if cookie1 and cookie2 and target_id:
            await asyncio.gather(
                run_strike(1, cookie1, target_id, target_name, m_id),   # ID 1
                run_strike(2, cookie2, target_id, target_name, m_id)    # ID 2
            )
    finally:
        display.stop()

if __name__ == "__main__":
    asyncio.run(main())
            
