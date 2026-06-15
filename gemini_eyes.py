import sys
import urllib.request
import json
import urllib.error
import time

def extract_logic(text, api_key):
    clean_key = api_key.strip()
    
    # TERA SAHI MODEL: Gemini 2.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={clean_key}"
    
    prompt = """You are a logical data extractor. Read the text and extract fundamental concepts and their relationships. 
    You must output ONLY valid JSON. 
    Format:
    {
      "new_nodes": [{"concept": "Name", "dimension": "Category"}],
      "new_links": [{"source": "Concept A", "target": "Concept B", "relation": "Implies"}]
    }
    Use relationships: 'Implies', 'Contradicts', 'TransformsInto', or 'Equivalent'."""
    
    data = {
        "contents": [{"parts": [{"text": prompt}, {"text": text}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print(result['candidates'][0]['content']['parts'][0]['text'])
                return # Success! Loop se bahar aa jao
                
        except urllib.error.HTTPError as e:
            # Agar 503 (Server Overload) aaye, toh thoda wait karke retry karo
            if e.code == 503:
                if attempt < max_retries - 1:
                    time.sleep(2) # 2 second wait karo
                    continue # Wapas try karo
                    
            error_body = e.read().decode('utf-8')
            print(f'{{"error": "Google API Error {e.code}: {error_body}"}}', file=sys.stderr)
            sys.exit(1)
            
        except Exception as e:
            print(f'{{"error": "{str(e)}"}}', file=sys.stderr)
            sys.exit(1)
            
    # Agar 3 baar me bhi Google ka server na uthe
    print('{"error": "Failed after 3 retries. Google 2.5 servers are heavily overloaded right now."}', file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        extract_logic(sys.argv[1], sys.argv[2])