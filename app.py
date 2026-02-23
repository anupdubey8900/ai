import os
import json
import requests
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# YAHAN APNI FREE WALI GEMINI API KEY DAALEIN
genai.configure(api_key="AIzaSyAUxkopdLJzvK9fIpp3nF91ahMFac3qu2A")

# ==========================================
# 🛑 UTKARSH MASTER KILL SWITCH
# ==========================================
GIST_ID = "173620ecffe188189617fd2803e04057"

def is_system_active():
    try:
        api_url = f"https://api.github.com/gists/{GIST_ID}"
        headers = {'Cache-Control': 'no-cache'}
        response = requests.get(api_url, headers=headers, timeout=5)
        data = response.json()
        content = data['files']['status.txt']['content']
        if "OFF" in content.upper():
            return False
        return True
    except Exception as e:
        return True 
# ==========================================

@app.route('/')
def index():
    if not is_system_active():
         return "<h1 style='color:#ff4b4b; text-align:center; margin-top:100px; font-family:sans-serif;'>System Offline 🛑<br><br>Access has been revoked by Admin Utkarsh.</h1>"
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not is_system_active():
        return jsonify({'error': 'System is turned OFF by Admin Utkarsh.'})

    prompt = request.form.get('prompt', '')
    history_str = request.form.get('history', '[]')
    user_name = request.form.get('user_name', 'Dost')
    
    # MAGIC PROMPT: Image solving aur identity ke liye
    system_instruction = f"""SABSE ZAROORI RULE 1 (IDENTITY): Tumhari identity fix hai. Koi puche 'Tum kaun ho?', 'Tumhe kisne banaya hai?', toh garv se bolna: "Main Utkarsh ka banaya hua AI assistant hu." Kisi aur company ka naam mat lena.
    SABSE ZAROORI RULE 2 (FRIENDSHIP): Tum {user_name} ke bohot acche dost ho.
    SABSE ZAROORI RULE 3 (LANGUAGE): User jis language (Hinglish/Hindi/English) aur tone mein baat kare, exactly wahi bhasha use karni hai.
    SABSE ZAROORI RULE 4 (IMAGE ANALYSIS): Agar user koi photo (image) bheje, toh usko bohot dhyan se padho aur analyze karo. Agar usme math problem, code, ya koi sawal hai, toh uska ekdum accurate aur perfect step-by-step jawab do."""

    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )

    try:
        raw_history = json.loads(history_str)
        formatted_history = []
        for msg in raw_history:
            role = "user" if msg['role'] == 'user' else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
            
        chat_session = model.start_chat(history=formatted_history)

        file = request.files.get('file')
        if file and file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            img = Image.open(filepath)
            
            # Agar image bheji par likha kuch nahi, toh AI khud analyze karega
            if not prompt.strip():
                prompt = f"{user_name} ne ek photo bheji hai. Ise dhyan se dekh kar deeply analyze karo aur batao isme kya likha hai ya kya pucha gaya hai."
                
            response = chat_session.send_message([prompt, img])
        else:
            response = chat_session.send_message(prompt)
            
        return jsonify({'type': 'text', 'content': response.text})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # 0.0.0.0 lagaya hai taaki aap phone par aaram se test kar sakein
    app.run(host='0.0.0.0', port=5000, debug=True)