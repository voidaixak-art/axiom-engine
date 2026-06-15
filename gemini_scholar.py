import sys
import urllib.request
import json
import urllib.error
import time

def deep_learn_topic(topic, api_key):
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={clean_key}"
    
    prompt = f"""You are an advanced AI mapping the subject: "{topic}".
    Generate a massive, deeply interconnected knowledge graph containing exactly 30 to 40 highly advanced concepts of this topic.
    
    CRITICAL RULE: You must output ONLY RAW, VALID JSON. Do not cut off the response. Ensure all brackets are perfectly closed. Do not include markdown tags.
    
    Format:
    {{
      "new_nodes": [{{"concept": "Name", "dimension": "Category"}}],
      "new_links": [{{"source": "Concept A", "target": "Concept B", "relation": "Implies"}}]
    }}
    Allowed relations: 'Implies', 'Contradicts', 'TransformsInto', 'Equivalent'."""
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print(result['candidates'][0]['content']['parts'][0]['text'])
                return
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < 2:
                time.sleep(2)
                continue
            error_body = e.read().decode('utf-8')
            print(f'{{"error": "API Error {e.code}: {error_body}"}}', file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f'{{"error": "{str(e)}"}}', file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        deep_learn_topic(sys.argv[1], sys.argv[2])