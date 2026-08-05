import asyncio
import os
import random
import sys
import time
import requests
import uuid

START_TIME = time.time()
SIGNATURE = "༺𝕛𝕒𝕥𝕚𝕟 अब्बू ☽༻"
SIGNATURE_CHANCE = 0.15 

def get_payload():
    base_text = "𝕜𝕒𝕣𝕥𝕚𝕜-𝕛𝕒𝕪+𝕝𝕦𝕧-𝕧𝕖𝕣𝕣𝕦-𝕣𝕒𝕜𝕤𝕙𝕚𝕥 ᴛʀʏ. ᴍᴀ ғʟᴏᴡᴇʀ."
    fire_part = "ʏᴀ ғɪʀᴇ 🔥??"
    flowers = ["🌸", "🌹", "🌺", "🌻", "🌼", "🌷"]
    line = f"{base_text} {random.choice(flowers)} {fire_part}"
    return ("\n" * 25).join([line] * 3)

# Setup spoofed session headers to mimic real Android App execution
def create_authenticated_session(sid):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Instagram 269.0.0.18.75 Android (30/11; 480dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100)",
        "X-IG-App-ID": "936619743392459",
        "X-IG-Capabilities": "36r/3g==",
        "X-IG-Connection-Type": "WIFI",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    })
    session.cookies.set("sessionid", sid, domain=".instagram.com")
    return session

# --- 🛡️ API NAME GUARDIAN ---
async def run_name_guardian(sid, tid, sig):
    print("🛡️ [GUARDIAN] Initializing API Name Guardian...", flush=True)
    session = create_authenticated_session(sid)
    
    while True:
        try:
            wait_time = random.uniform(180, 300)
            await asyncio.sleep(wait_time)
            
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200:
                current_title = resp.json().get("thread", {}).get("thread_title")
                if current_title != sig:
                    print(f"🚨 [GUARDIAN] Name changed to '{current_title}'. Re-securing...", flush=True)
                    csrf = session.cookies.get("csrftoken", "")
                    session.post(
                        f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/",
                        data={"title": sig, "_csrftoken": csrf, "_uuid": str(uuid.uuid4())},
                        headers={"X-CSRFToken": csrf}
                    )
                    print("🔒 [GUARDIAN] Name re-secured.", flush=True)
        except Exception as e: 
            print(f"⚠️ [GUARDIAN] Error: {e}", flush=True)

# --- 🔥 HIGH-SPEED API STRIKE ENGINE ---
async def run_api_engine(engine_id, sid, tid):
    print(f"💥 [Engine {engine_id}] Waking up. High-Speed API Engine Online...", flush=True)
    session = create_authenticated_session(sid)
    msg_count = 0

    while True:
        if time.time() - START_TIME > 18000:
            print(f"⏰ [Engine {engine_id}] 5-hour limit reached.", flush=True)
            sys.exit(0)

        try:
            text_to_send = SIGNATURE if random.random() < SIGNATURE_CHANCE else get_payload()
            msg_type = "SIGNATURE" if text_to_send == SIGNATURE else "PAYLOAD"
            icon = "☠️" if msg_type == "SIGNATURE" else "🚀"

            payload = {
                "text": text_to_send,
                "thread_ids": f"[{tid}]",
                "action": "send_item",
                "client_context": str(uuid.uuid4()),
                "_uuid": str(uuid.uuid4())
            }

            url = f"https://www.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
            resp = session.post(url, data=payload)

            if resp.status_code == 200:
                msg_count += 1
                print(f"{icon} [Engine {engine_id}] SENT [{msg_type}] | Strike {msg_count}", flush=True)
                # Anti-ban micro delay
                await asyncio.sleep(random.uniform(0.8, 1.5))
            elif resp.status_code == 429:
                print(f"⚠️ [Engine {engine_id}] Rate Limited (429). Backing off 60s...", flush=True)
                await asyncio.sleep(60)
            else:
                print(f"⚠️ [Engine {engine_id}] Failed with Status {resp.status_code}: {resp.text[:100]}", flush=True)
                await asyncio.sleep(5)

        except Exception as e:
            print(f"⚠️ [Engine {engine_id}] Connection exception: {e}", flush=True)
            await asyncio.sleep(5)

async def main():
    sid = os.environ.get("SESSION_ID")
    url = os.environ.get("GROUP_URL")
    
    print("🔥 INITIALIZING PHOENIX HIGH-SPEED MATRIX 🔥", flush=True)
    
    tid = url.strip('/').split('/')[-1] if url else ""
    if not tid or not sid:
        print("❌ [SYSTEM] Missing SESSION_ID or GROUP_URL.", flush=True)
        return

    # Matrix execution
    tasks = [run_api_engine(i + 1, sid, tid) for i in range(2)]
    tasks.append(run_name_guardian(sid, tid, SIGNATURE))
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
                    
