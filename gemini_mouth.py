import sys
import urllib.request
import json
import os
import time

def speak(user_input, api_key):
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={clean_key}"
    
    # 1. Engine apna dimaag (brain.json) khud padhega
    brain_data = "{}"
    if os.path.exists("brain.json"):
        with open("brain.json", "r") as f:
            brain_data = f.read()

    # 2. Engine ki Personality aur Rules
    prompt = f"""You are 'Axiom Engine', an advanced, autonomous logical AI created by your user. 
    Your core memory and logic map is based STRICTLY on this JSON data: 
    {brain_data}
    
    Rules for your response:
    1. Speak in a mix of Hindi and English (Hinglish), like a highly intelligent, friendly tech-partner.
    2. If the user asks a question, answer it by looking at the connections in your JSON memory. 
    3. If the user asks about a concept that is NOT in your JSON memory, honestly admit it and say: "Mujhe iske baare mein nahi pata, mujhe isko apni memory mein map karne ke liye LEARN command ki zaroorat hai."
    4. Keep it conversational, confident, and slightly philosophical. Do not output JSON, just talk naturally.
    """
    
    data = {
        "contents": [{"parts": [{"text": prompt}, {"text": f"User says: {user_input}"}]}]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(result['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e:
        print(f"Error connecting to Voice Module: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        speak(sys.argv[1], sys.argv[2])