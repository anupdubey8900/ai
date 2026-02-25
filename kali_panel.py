import asyncio
import time
import os
import re
import base64
from flask import Flask, render_template_string, request, jsonify
from telethon.sync import TelegramClient
from flask_cloudflared import run_with_cloudflared

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
API_ID = 36229140                              
API_HASH = "3b003ebf73e5e9ccdd72c5cb57af9221"  
SESSION_NAME = 'kali_mirror_session'         
TARGET_BOT = 'Kali_Maker_Bot'                  

app = Flask(__name__)
app = Flask(__name__)
run_with_cloudflared(app)  # Ye line apke liye auto-link banayegi!

# ==========================================
# 🎨 UI CODE (PREMIUM WHITE + ANDROID FIXES)
# ==========================================
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Utkarsh | Live System</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f1f5f9; 
            color: #0f172a;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden; padding: 20px;
        }

        .dashboard-wrapper {
            width: 100%; max-width: 1200px; height: 100%; max-height: 850px;
            display: flex; gap: 20px; background: transparent;
        }

        /* ⬅️ LEFT PANEL */
        .left-panel {
            width: 380px; background: #ffffff; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
            display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0;
        }

        .panel-header { padding: 25px 25px 15px 25px; border-bottom: 1px solid #f1f5f9; }
        .brand-title { font-size: 20px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 10px; }
        .brand-icon { background: #3b82f6; color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }

        .controls-area {
            padding: 25px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 25px;
        }
        .controls-area::-webkit-scrollbar { width: 4px; }
        .controls-area::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

        .input-group { display: flex; flex-direction: column; gap: 10px; }
        .section-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
        
        .custom-input {
            width: 100%; background: #f8fafc; border: 2px solid #e2e8f0; color: #0f172a;
            padding: 14px 15px; border-radius: 12px; font-family: inherit; font-size: 14px;
            outline: none; transition: 0.3s; font-weight: 500;
        }
        .custom-input:focus { border-color: #3b82f6; background: #fff; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }
        
        .btn-send {
            width: 100%; background: #0f172a; color: #fff; border: none; padding: 14px;
            border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.3s;
        }
        .btn-send:hover { background: #3b82f6; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }

        .dynamic-buttons-container { display: flex; flex-direction: column; gap: 10px; }
        .btn-row { display: flex; gap: 10px; width: 100%; flex-wrap: wrap; }
        
        .action-btn {
            flex: 1; min-width: 45%; background: #ffffff; border: 1px solid #cbd5e1;
            color: #334155; padding: 12px 10px; font-family: inherit; font-size: 13px;
            font-weight: 600; cursor: pointer; transition: 0.2s; border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02); display: flex; align-items: center; justify-content: center; gap: 6px;
        }
        .action-btn:hover { background: #eff6ff; border-color: #3b82f6; color: #2563eb; transform: translateY(-1px); }

        .btn-restart {
            margin: 20px 25px; background: #f1f5f9; color: #ef4444; border: 1px solid #fecaca;
            padding: 12px; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer;
            transition: 0.3s; display: flex; align-items: center; justify-content: center; gap: 8px;
        }
        .btn-restart:hover { background: #fee2e2; color: #b91c1c; }

        /* ➡️ RIGHT PANEL */
        .right-panel {
            flex: 1; background: #ffffff; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
            display: flex; flex-direction: column; position: relative; overflow: hidden;
        }

        .result-header {
            padding: 15px 30px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; background: #fafbfc;
        }
        .result-title { font-size: 15px; font-weight: 700; color: #334155; display: flex; align-items: center; gap: 8px; }
        
        .header-actions { display: flex; align-items: center; gap: 15px; }

        .btn-copy {
            background: #e0f2fe; color: #2563eb; border: 1px solid #bfdbfe;
            padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 700;
            cursor: pointer; transition: 0.2s; display: flex; align-items: center; gap: 5px;
        }
        .btn-copy:hover { background: #bfdbfe; }
        .btn-copy.success { background: #dcfce7; color: #166534; border-color: #bbf7d0; }

        .status-badge { background: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 6px;}
        .status-badge.loading { background: #fef9c3; color: #854d0e; }
        .status-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; }
        .status-badge.loading .status-dot { background: #eab308; animation: pulse 1s infinite; }

        .result-body { flex: 1; padding: 30px; overflow-y: auto; background: #f8fafc; }
        
        .result-card {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
            padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            font-family: inherit; font-size: 14px; line-height: 1.8; color: #1e293b; 
            white-space: pre-wrap; word-wrap: break-word; border-left: 4px solid #3b82f6;
        }
        
        .normal-block { margin-bottom: 25px; padding-bottom: 25px; border-bottom: 1px dashed #cbd5e1; }
        .normal-block:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        
        .success-banner {
            background: #10b981; color: white; padding: 8px 15px; border-radius: 12px 12px 0 0;
            font-weight: 700; text-align: center; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;
            margin-top: 10px; display: flex; justify-content: center; align-items: center; gap: 8px;
        }
        .success-block {
            background: #f0fdf4; border: 2px solid #10b981; border-top: none; 
            border-radius: 0 0 12px 12px; padding: 20px; margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15); font-weight: 500;
        }

        .result-card a { color: #3b82f6; text-decoration: none; font-weight: 600; background: #eff6ff; padding: 2px 6px; border-radius: 4px; border: 1px dashed #bfdbfe;}
        .result-card a:hover { color: #2563eb; background: #dbeafe; text-decoration: underline; }

        .media-box { margin: 15px 0; text-align: center; }
        .media-box img { max-width: 100%; border-radius: 12px; border: 2px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }

        .loader-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.7); backdrop-filter: blur(5px);
            display: none; justify-content: center; align-items: center; flex-direction: column; z-index: 10;
        }
        .spinner { width: 45px; height: 45px; border: 4px solid #e2e8f0; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 15px; }

        @keyframes spin { 100% { transform: rotate(360deg); } }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

        /* 📱 MOBILE RESPONSIVE (FIXED SCROLL & LAYOUT) */
        @media (max-width: 850px) {
            body { padding: 0; background: #f8fafc; }
            .dashboard-wrapper { flex-direction: column; gap: 0; height: 100vh; max-height: 100vh; border-radius: 0; }
            
            .left-panel { 
                width: 100%; border-radius: 0; border: none; border-bottom: 2px solid #e2e8f0; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.05); z-index: 5; 
                max-height: 55vh; display: flex; flex-direction: column; flex-shrink: 0;
            }
            .panel-header { padding: 15px 20px 10px 20px; }
            .brand-title { font-size: 18px; }
            .controls-area { padding: 10px 20px; gap: 15px; overflow-y: auto; }
            .btn-restart { display: flex; margin: 10px 20px 15px 20px; padding: 12px; font-size: 13px; font-weight: 700; flex-shrink: 0;} 

            .right-panel { border-radius: 0; border: none; box-shadow: none; flex: 1; display: flex; flex-direction: column; }
            .result-header { padding: 15px 20px; flex-wrap: wrap; gap: 10px;}
            .result-body { padding: 15px; padding-bottom: 40px; overflow-y: auto; }
            .result-card { font-size: 13px; padding: 15px; }
        }
    </style>
</head>
<body>

    <div class="dashboard-wrapper">
        <div class="left-panel">
            <div class="panel-header">
                <div class="brand-title"><div class="brand-icon">⚡</div> Utkarsh Protocol</div>
            </div>

            <div class="controls-area">
                <div class="input-group">
                    <span class="section-label">1. Target Input</span>
                    <input type="text" id="userInput" class="custom-input" placeholder="Enter Target Link / Number..." autocomplete="off">
                    <button class="btn-send" onclick="sendText()">Send Data</button>
                </div>

                <div class="input-group">
                    <span class="section-label">2. Select Action</span>
                    <div class="dynamic-buttons-container" id="dynamicButtons">
                        <div style="color: #94a3b8; font-size: 13px; text-align: center; padding: 20px 0;">Syncing Interface...</div>
                    </div>
                </div>
            </div>
            <button class="btn-restart" onclick="interact('start', '')">🔄 Restart Session</button>
        </div>

        <div class="right-panel">
            <div class="result-header">
                <div class="result-title">📄 Extracted Result</div>
                <div class="header-actions">
                    <button class="btn-copy" id="copyBtn" onclick="copyResult()">📋 Copy Data</button>
                    <div class="status-badge" id="statusBadge"><div class="status-dot"></div> <span id="statusText">Listening Live...</span></div>
                </div>
            </div>

            <div class="result-body" id="resultBody">
                <div class="result-card" id="rawTextData" style="color:#64748b; text-align:center; border-left-color: #cbd5e1;">
                    Fetching current session data...
                </div>
            </div>

            <div class="loader-overlay" id="loader">
                <div class="spinner"></div>
                <div style="color: #3b82f6; font-weight: 700; font-size: 14px;">Sending Command...</div>
            </div>
        </div>
    </div>

    <script>
        let currentMsgId = null;
        let pollTimer = null;
        let lastCopyText = ""; 

        window.onload = () => { 
            fetchLatest(true); 
            pollTimer = setInterval(() => fetchLatest(false), 2000);
        };

        function fetchLatest(showLoader) {
            if(showLoader) document.getElementById('loader').style.display = 'flex';
            
            fetch('/api/get_latest')
            .then(res => res.json())
            .then(data => {
                if(showLoader) document.getElementById('loader').style.display = 'none';
                
                if(data.msg_id && data.msg_id !== currentMsgId) {
                    currentMsgId = data.msg_id;
                    renderBotState(data);
                    
                    let badge = document.getElementById('statusBadge');
                    badge.className = 'status-badge loading';
                    document.getElementById('statusText').innerText = 'New Data Received!';
                    setTimeout(() => {
                        badge.className = 'status-badge';
                        document.getElementById('statusText').innerText = 'Listening Live...';
                    }, 2000);
                }
            })
            .catch(e => console.log("Sync Error"));
        }

        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); sendText(); }
        });

        function sendText() {
            let val = document.getElementById('userInput').value.trim();
            if(!val) return;
            document.getElementById('userInput').value = '';
            interact('text', val);
        }

        // 💥 UNIVERSAL COPY FUNCTION (Works on all Androids 100%)
        function fallbackCopyTextToClipboard(text) {
            var textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                var successful = document.execCommand('copy');
                if(successful) alert('✅ Copied Successfully!');
                else alert('❌ Failed to copy link.');
            } catch (err) {
                alert('❌ Failed to copy link.');
            }
            document.body.removeChild(textArea);
        }

        function smartCopy(text) {
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(() => {
                    alert('✅ Copied Successfully!');
                }).catch(err => {
                    fallbackCopyTextToClipboard(text);
                });
            } else {
                fallbackCopyTextToClipboard(text);
            }
        }

        function clickButton(btnText, url = null) {
            // FIX: Smart Link Copier Mobile Support
            if (btnText.toLowerCase().includes('copy')) {
                let urls = lastCopyText.match(/https?:\\/\\/[^\\s]+/g);
                if (urls && urls.length > 0) {
                    smartCopy(urls[0]); // Copies only the URL
                } else {
                    smartCopy(lastCopyText); // Copies all text if URL not found
                }
                return; 
            }

            if(url && url !== "null" && url !== "") {
                window.open(url, '_blank'); 
            } else {
                interact('button', btnText);
            }
        }

        function interact(actionType, payloadText) {
            clearInterval(pollTimer);
            document.getElementById('loader').style.display = 'flex';
            
            fetch('/api/interact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: actionType, payload: payloadText })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('loader').style.display = 'none';
                if(data.msg_id) currentMsgId = data.msg_id;
                renderBotState(data);
                pollTimer = setInterval(() => fetchLatest(false), 2000);
            })
            .catch(err => {
                document.getElementById('loader').style.display = 'none';
                pollTimer = setInterval(() => fetchLatest(false), 2000);
            });
        }

        function linkify(inputText) {
            var replacePattern1 = /(\\b(https?|ftp):\\/\\/[-A-Z0-9+&@#\\/%?=~_|!:,.;]*[-A-Z0-9+&@#\\/%=~_|])/gim;
            return inputText.replace(replacePattern1, '<a href="$1" target="_blank" title="Click to Open">$1</a>');
        }

        // FULL DATA COPY FUNCTION
        function copyResult() {
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(lastCopyText).then(() => showCopySuccess());
            } else {
                fallbackCopyTextToClipboard(lastCopyText);
                showCopySuccess();
            }
        }

        function showCopySuccess() {
            let btn = document.getElementById('copyBtn');
            btn.innerHTML = '✅ Copied!';
            btn.className = 'btn-copy success';
            setTimeout(() => {
                btn.innerHTML = '📋 Copy Data';
                btn.className = 'btn-copy';
            }, 2000);
        }

        function renderBotState(data) {
            let htmlText = '';
            lastCopyText = ''; 

            if(data.items && data.items.length > 0) {
                data.items.forEach(item => {
                    if (item.type === 'text') {
                        lastCopyText += item.content + '\\n\\n';
                        let formattedLine = linkify(item.content).replace(/\\n/g, '<br>');
                        
                        let keywords = ["Visitor Information Captured", "New Login Detected", "GPS Coordinates", "Target:", "Account:", "Password:"];
                        let isTargetData = keywords.some(k => item.content.includes(k));
                        
                        if(isTargetData) {
                            htmlText += `<div class="success-banner">🎯 NEW TARGET INFORMATION 🎯</div>
                                         <div class="normal-block success-block">${formattedLine}</div>`;
                        } else {
                            htmlText += `<div class="normal-block">${formattedLine}</div>`;
                        }
                    } else if (item.type === 'photo') {
                        // Direct base64 image rendering
                        htmlText += `<div class="media-box"><img src="${item.content}" alt="Captured Media"></div>`;
                    }
                });
            } else {
                htmlText = '<div class="normal-block text-center text-gray-500">No Data Available.</div>';
            }

            document.getElementById('resultBody').innerHTML = `<div class="result-card" id="rawTextData">${htmlText}</div>`;
            
            let btnHtml = '';
            if(data.buttons && data.buttons.length > 0) {
                data.buttons.forEach(row => {
                    btnHtml += `<div class="btn-row">`;
                    row.forEach(btn => {
                        let icon = '⚡';
                        if(btn.text.includes('Monitor')) icon = '📱';
                        if(btn.text.includes('Account') || btn.text.includes('Social')) icon = '🔐';
                        if(btn.text.includes('Contact') || btn.text.includes('Location')) icon = '📞';
                        if(btn.text.includes('WhatsApp')) icon = '📟';
                        if(btn.text.includes('Information')) icon = '👤';
                        if(btn.text.includes('Back') || btn.text.includes('Menu')) icon = '◀️';
                        if(btn.text.includes('Copy')) icon = '📋';
                        
                        let cleanText = btn.text.replace(/📱|🔐|📞|📟|👤|◀️|📋/g, '').trim();
                        let btnUrl = btn.url ? btn.url : null;
                        
                        btnHtml += `<button class="action-btn" onclick="clickButton('${btn.text}', '${btnUrl}')">${icon} ${cleanText}</button>`;
                    });
                    btnHtml += `</div>`;
                });
            } else {
                btnHtml = '<div style="color: #94a3b8; font-size: 13px; text-align: center; padding: 10px 0;">No Action Buttons Available.</div>';
            }
            document.getElementById('dynamicButtons').innerHTML = btnHtml;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

# ==========================================
# 🚀 CORE ENGINE: FETCH MULTIPLE MESSAGES + BASE64 IMAGES
# ==========================================
def replace_names(text):
    text = re.sub(r'(?i)(Developed by:|First Version :)\s*@[A-Za-z0-9_]+', r'\1 made by anup', text)
    text = text.replace("@Kaliboy002", "made by anup")
    text = text.replace("@Kali_Linux_Robot", "made by anup")
    text = text.replace("@Kali_Maker_Bot", "made by anup")
    
    text = text.replace("Developed by: made by anup", "made by anup")
    text = text.replace("First Version : made by anup", "made by anup")
    return text

def get_latest_bot_state(client):
    # Limit badha di taaki bada data miss na ho
    msgs = client.get_messages(TARGET_BOT, limit=20)
    
    bot_cluster = []
    for m in msgs:
        if m.out: 
            break
        bot_cluster.append(m)
        
    if not bot_cluster:
        bot_cluster = [m for m in msgs if not m.out][:2]

    if not bot_cluster:
        return {"items": [], "buttons": [], "msg_id": None}

    bot_cluster.reverse()

    items = []
    msg_id = bot_cluster[-1].id  
    buttons = []

    for m in bot_cluster:
        if m.message:
            txt = replace_names(m.message)
            items.append({"type": "text", "content": txt})
            
        if m.photo:
            # FIX: Base64 encoding. Ab file save nahi hogi, direct data HTML me jayega (100% Works on Android)
            try:
                img_bytes = client.download_media(m.media, file=bytes)
                if img_bytes:
                    base64_encoded = base64.b64encode(img_bytes).decode('utf-8')
                    base64_img = f"data:image/jpeg;base64,{base64_encoded}"
                    items.append({"type": "photo", "content": base64_img})
            except Exception as e:
                print(f"Image Download Error: {e}")
            
        if m.buttons:
            buttons = [] 
            for row in m.buttons:
                buttons.append([{"text": b.text, "url": b.url if hasattr(b, 'url') else None} for b in row])

    return {
        "items": items, 
        "buttons": buttons, 
        "msg_id": msg_id
    }

# ==========================================
# 🚀 AUTO-SYNC ENDPOINT
# ==========================================
@app.route('/api/get_latest', methods=['GET'])
def get_latest():
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        with TelegramClient(SESSION_NAME, API_ID, API_HASH, loop=new_loop) as client:
            state = get_latest_bot_state(client)
            return jsonify(state)
    except Exception as e:
        return jsonify({"msg_id": None})
    finally:
        new_loop.close()

# ==========================================
# 🚀 INTERACTION ENDPOINT
# ==========================================
@app.route('/api/interact', methods=['POST'])
def interact():
    data = request.json
    action_type = data.get('type')  
    payload = data.get('payload', '')

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    
    result = {"items": [], "buttons": [], "msg_id": None}

    try:
        with TelegramClient(SESSION_NAME, API_ID, API_HASH, loop=new_loop) as client:
            
            if action_type == 'start':
                client.send_message(TARGET_BOT, '/start')
                time.sleep(1.5)
                
            elif action_type == 'text':
                client.send_message(TARGET_BOT, payload)
                time.sleep(1.5)
                
            elif action_type == 'button':
                msgs = client.get_messages(TARGET_BOT, limit=10)
                clicked = False
                for m in msgs:
                    if m.buttons:
                        for row in m.buttons:
                            for btn in row:
                                if payload in btn.text or btn.text in payload:
                                    m.click(text=btn.text) 
                                    clicked = True
                                    break
                            if clicked: break
                    if clicked: break
                time.sleep(1.5)

            result = get_latest_bot_state(client)

    except Exception as e:
        pass
    finally:
        new_loop.close()
        
    return jsonify(result)

# ==========================================
# 🔐 TERMINAL LOGIN SYSTEM
# ==========================================
async def login_system():
    print("\n" + "="*50)
    print("   🛡️ PREMIUM PROTOCOL INITIALIZING 🛡️   ")
    print("="*50 + "\n")
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("⚠️ FIRST TIME SETUP: LOGIN REQUIRED!")
        phone = input("👉 Enter Telegram Number (e.g. +919876543210): ")
        await client.send_code_request(phone)
        
        print("\n📩 OTP sent to your Telegram App!")
        otp = input("👉 Enter the OTP: ")
        
        try:
            await client.sign_in(phone, otp)
            print("\n✅ LOGIN SUCCESSFUL! Session Saved.")
        except Exception as e:
            print(f"\n❌ LOGIN FAILED: {e}")
            await client.disconnect()
            os._exit(1)
    else:
        print("✅ Telegram Session Active. Auto-Sync Ready.")
        
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(login_system())
    
    print("\n" + "="*50)
    print("🚀 FULL DATA MIRROR ENGINE RUNNING!")
    print("👉 OPEN BROWSER AND TYPE: http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)