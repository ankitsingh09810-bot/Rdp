          # -*- coding: utf-8 -*-
import asyncio
import os
import re
import random
import sys
import time
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# --- ⚙️ SHIELD PILLAR SETTINGS ---
TABS_PER_MACHINE = 2    
PULSE_DELAY = 50      # Steady injection speed
sys.stdout.reconfigure(encoding='utf-8')

# --- 🎬 MANDATORY HUMAN BEHAVIOR (1 MINUTE BURST) ---
async def exact_one_minute_human_behavior(context, machine_id):
    """
    Spam loop complete hone ke baad exact 60 seconds tak continuous
    reels simulation chala kar account trust score ko stabilize karta hai.
    """
    print(f"🎬 [Machine {machine_id}] Target Reached! Launching Mandatory 1-Minute Human Behavior...")
    try:
        reels_page = await context.new_page()
        # Custom route handlers load network weight badhane ke liye (Bypasses patterns)
        await reels_page.goto("https://www.instagram.com/reels/", wait_until="load", timeout=25000)
        
        start_time = time.time()
        current_reel = 1
        
        # Loop exact 60 seconds tak chalega
        while time.time() - start_time < 60:
            # Real viewing delay per reel (2 to 5 seconds stay duration)
            await reels_page.wait_for_timeout(random.uniform(2000, 5000))
            
            # Random dynamic engagement (Like system)
            if random.random() < 0.4:
                try:
                    await reels_page.mouse.dblclick(x=200, y=150)
                    print(f"❤️ [Machine {machine_id}] | Verification Reel {current_reel}: Liked.")
                except:
                    pass
                await reels_page.wait_for_timeout(random.uniform(500, 1200))
            
            # Action event simulation for next reel
            await reels_page.keyboard.press("ArrowDown")
            current_reel += 1
            
        await reels_page.close()
        print(f"✅ [Machine {machine_id}] Trust Score Balanced. Returning to primary sequence.")
    except Exception as e:
        print(f"⚠️ [Machine {machine_id}] Shield behavior bypassed due to page timeout.")

# --- 🔱 MAIN EXECUTION ENGINE ---
async def run_strike(node_id, cookie, target_id, target_name):
    async with async_playwright() as p:
        user_agent = "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
        profile_path = os.path.join(os.getcwd(), f"n_{node_id}")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=True,
            user_agent=user_agent,
            viewport={'width': 400, 'height': 300},
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu"
            ]
        )

        await Stealth().apply_stealth_async(context)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{
            'name': 'sessionid', 'value': sid.strip(), 
            'domain': '.instagram.com', 'path': '/', 'secure': True, 'httpOnly': True
        }])

        # ⚡ TARGET COUNTER INJECTION SCRIPT
        # Yeh script exact targets meet hone par automatic pulse engine ko break kar deti hai
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
                    // Agar limit crash ho jaye, to control loop ko stop kar do
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
                        }, 200);
                    }
                    setTimeout(() => { pulse(); }, delay);
                }
                pulse();
            }
        """

        # Purana complex timers hata kar direct session execution loop lagaya hai
        session_running = True
        while session_running:
            pages = []
            # Har machine ke liye 300 se 500 ke beech ek custom burst target select hoga
            target_spam_limit = random.randint(300, 500)
            print(f"🚀 [Machine {node_id}] Initiating Burst Phase. Target: {target_spam_limit} Messages.")

            for i in range(TABS_PER_MACHINE):
                pg = await context.new_page()
                try:
                    await pg.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="commit", timeout=15000)
                    await pg.wait_for_timeout(3000)
                    # Window context target value dynamically inject karna
                    await pg.evaluate(strike_script, [target_name, PULSE_DELAY, target_spam_limit])
                    pages.append(pg)
                except: 
                    pass

            # Monitor Loop: Jab tak target hits nahi hote tab tak pages ko open rakhna
            reached = False
            start_monitor = time.time()
            
            while not reached:
                await asyncio.sleep(5)
                # Max duration protection (10 minutes max execution safety)
                if time.time() - start_monitor > 600:
                    break
                    
                for pg in pages:
                    try:
                        # Console frame ya direct state evaluation se checks verification karna
                        count = await pg.evaluate("window.currentSpamCount")
                        if count and count >= target_spam_limit:
                            reached = True
                            break
                    except:
                        pass
            
            # Primary spam windows close karna taaki pure cooldown environment setup ho sake
            for pg in pages: 
                try: await pg.close()
                except: pass
            
            # --- 🛡️ SHIELD TRIGGER PHASE ---
            # Jaise hi text block count limit match hoga, 1-minute solid human session execute hoga
            await exact_one_minute_human_behavior(context, node_id)

        await context.close()

async def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    m_id = os.environ.get("MACHINE_ID", "1")
    if cookie and target_id:
        await run_strike(m_id, cookie, target_id, target_name)

if __name__ == "__main__":
    asyncio.run(main())
        
