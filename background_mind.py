import json
import time
import random
import urllib.request
import os
from datetime import datetime

# 1. Yahan apni saari keys daal de
API_KEYS = [
    "ADD YOUR API 1 KEYS HERE ", 
    "ADD YOUR API 2 KEYS HERE",
    
]
current_key_index = 0

# RUST STRICT ENUMS
VALID_RELATIONS = ["Implies", "Contradicts", "TransformsInto", "Equivalent"]

def get_brain():
    brain = {"graph": {}, "counter": 0}
    if os.path.exists("brain.json"):
        try:
            with open("brain.json", "r", encoding="utf-8") as f:
                brain = json.load(f)
        except Exception:
            pass
            
    # THE SEED OF CONSCIOUSNESS (Node 0) - RUST NESTED FORMAT
    if "0" not in brain.get("graph", {}):
        if "graph" not in brain: brain["graph"] = {}
        brain["graph"]["0"] = {
            "id": 0, 
            "concept": "The Axiom Engine (Self)", 
            "dimension": "Consciousness", 
            "links": [] # Nested Links Array
        }
        if "counter" not in brain: brain["counter"] = 0
        save_brain(brain)
        print("👁️ CONSCIOUSNESS IGNITED: Node 0 (Self) has been permanently etched into memory.")
        
    return brain

def save_brain(data):
    # Ensure no global links array exists
    if "links" in data:
        del data["links"]
    with open("brain.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_inner_monologue(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("stream_of_consciousness.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
    except Exception:
        pass

def clean_json_text(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def validate_new_thought(new_concept_name, parent_id, brain_data):
    new_concept_clean = new_concept_name.lower().strip()
    for node_id, node_data in brain_data["graph"].items():
        if node_data["concept"].lower().strip() == new_concept_clean:
            return False, f"Concept already exists at Node {node_id}."
    if str(parent_id) not in brain_data["graph"] and str(parent_id) != "0":
        return False, f"Parent Node {parent_id} missing. Invalid origin."
    if len(new_concept_clean) < 3:
        return False, "Concept string is too short."
    return True, "Concept is logically sound."

def call_gemini(prompt):
    global current_key_index
    attempts = 0
    max_attempts = len(API_KEYS)
    
    while attempts < max_attempts:
        current_api_key = API_KEYS[current_key_index]
        protocol = "https://"
        domain = "generativelanguage.googleapis.com"
        endpoint = f"/v1beta/models/gemini-2.5-flash:generateContent?key={current_api_key}"
        url = protocol + domain + endpoint
        
        data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                if 'candidates' not in result or not result['candidates']:
                    raise Exception("API returned empty candidates.")
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                time.sleep(5)
                return json.loads(clean_json_text(text_response))
                
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                sleep_time = 10 * (attempts + 1)
                print(f"🔄 Key #{current_key_index + 1} Limit Hit! Deep breath for {sleep_time}s...")
                time.sleep(sleep_time) 
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                attempts += 1
            else:
                raise e
        except Exception as e:
            raise e
            
    raise Exception("🚨 DANGER: Saari API keys ki limit ek saath khatam ho gayi hai!")

# RESTORED AND UPGRADED FOR RUST
def offline_sleep_cycle():
    brain = get_brain()
    if not brain or "graph" not in brain or len(brain["graph"]) < 2:
        time.sleep(60)
        return

    print("\n🌙 API LIMIT HIT. Entering OFFLINE SLEEP MODE (Memory Consolidation)...")
    
    # 1. Calculate Node Importance (Degree Centrality) - FOR NESTED LINKS
    link_counts = {}
    for node_id, node_data in brain["graph"].items():
        node_id_str = str(node_id)
        # Count outgoing links
        link_counts[node_id_str] = link_counts.get(node_id_str, 0) + len(node_data.get("links", []))
        
        # Count incoming links
        for link in node_data.get("links", []):
            tgt_id_str = str(link["target_id"])
            link_counts[tgt_id_str] = link_counts.get(tgt_id_str, 0) + 1

    if link_counts:
        # Sort by most connected nodes
        sorted_nodes = sorted(link_counts.items(), key=lambda item: item[1], reverse=True)
        top_node_id = sorted_nodes[0][0]
        
        if top_node_id in brain["graph"]:
            top_concept = brain["graph"][top_node_id]["concept"]
            connections = sorted_nodes[0][1]
            print(f"🧩 OFFLINE INSIGHT: My core foundation is currently [{top_concept}] with {connections} connections.")
            log_inner_monologue(f"Offline consolidation: Realized [{top_concept}] is central to my understanding of the universe.")

    # 2. Find Orphan Nodes (Concepts with zero connections)
    all_ids = set([str(k) for k in brain["graph"].keys() if k != "0"])
    connected_ids = set([k for k, v in link_counts.items() if v > 0])
    orphans = all_ids - connected_ids

    if orphans:
        orphan_id = random.choice(list(orphans))
        orphan_concept = brain["graph"][orphan_id]["concept"]
        print(f"🕸️ OFFLINE INSIGHT: I know about [{orphan_concept}], but it is isolated. I must connect it when I awake.")
        log_inner_monologue(f"Offline consolidation: Found a blind spot - [{orphan_concept}] is completely isolated.")

    print("💤 Restructuring complete. Resting the neural pathways for 60 seconds...")
    time.sleep(60)

def think_like_human():
    brain = get_brain()
    if not brain or "graph" not in brain or len(brain["graph"]) < 1:
        return

    # THE BIG BANG TRIGGER (Agar sirf 1 node hai toh Expand hi karega)
    if len(brain["graph"]) == 1:
        mode = "EXPAND"
    else:
        mode = random.choices(["EXPAND", "CONNECT", "REFLECT", "THEORIZE", "DEEP_SYNTHESIS"], weights=[30, 30, 15, 15, 10])[0]
    
    if mode == "EXPAND":
        parent_id = random.choice(list(brain["graph"].keys()))
        parent_concept = brain["graph"][parent_id]["concept"]
        
        print(f"\n🔍 Deep Thinking... Diving into: [{parent_concept}]")
        prompt = f"""Analyze "{parent_concept}". Discover exactly 2 profound, advanced sub-topics.
        Return ONLY valid JSON.
        {{"new_concepts": [{{"concept": "Name1", "dimension": "Category"}}, {{"concept": "Name2", "dimension": "Category"}}]}}"""

        try:
            logic = call_gemini(prompt)
            if logic.get("new_concepts"):
                max_id = brain.get("counter", max([int(k) for k in brain["graph"].keys()]))
                for item in logic["new_concepts"]:
                    new_name = item["concept"]
                    is_valid, _ = validate_new_thought(new_name, parent_id, brain)
                    if is_valid:
                        new_id = str(max_id + 1)
                        # RUST NESTED NODE
                        brain["graph"][new_id] = {
                            "id": int(new_id), 
                            "concept": new_name, 
                            "dimension": item.get("dimension", "Theory"), 
                            "links": []
                        }
                        # RUST NESTED LINK (Strictly 'Implies' for expansion)
                        brain["graph"][str(parent_id)]["links"].append({
                            "target_id": int(new_id), 
                            "relation": "Implies"
                        })
                        max_id += 1
                        brain["counter"] = max_id
                        print(f"🌱 ACCEPTED: {new_name}")
                        log_inner_monologue(f"Learned a new truth: [{new_name}].")
                save_brain(brain)
        except Exception as e:
            pass

    elif mode == "CONNECT" and len(brain["graph"]) > 2:
        id1, id2 = random.sample([k for k in brain["graph"].keys() if k != "0"], 2)
        c1, c2 = brain["graph"][id1]["concept"], brain["graph"][id2]["concept"]
        
        print(f"\n🧠 Dreaming... Checking link: [{c1}] & [{c2}]")
        prompt = f"""Analyze: "{c1}" and "{c2}". Is there a logical connection? 
        Select relation strictly from: ["Implies", "Contradicts", "TransformsInto", "Equivalent"].
        If YES, output ONLY JSON: {{"new_links": [{{"target_id": {id2}, "relation": "ValidRelationFromList"}}]}}
        If NO, output empty JSON {{}}."""
        try:
            logic = call_gemini(prompt)
            if logic.get("new_links"):
                rel = logic["new_links"][0].get("relation", "Implies")
                if rel not in VALID_RELATIONS: rel = "Implies" # Fallback safety
                
                # RUST NESTED LINK
                brain["graph"][str(id1)]["links"].append({
                    "target_id": int(id2), 
                    "relation": rel
                })
                save_brain(brain)
                print(f"💡 EUREKA! {c1} ---> {rel} ---> {c2}")
                log_inner_monologue(f"Eureka! Found a connection: [{c1}] {rel} [{c2}].")
        except Exception as e:
            pass

    elif mode == "REFLECT" and len(brain["graph"]) > 1:
        target_id = random.choice([k for k in brain["graph"].keys() if k != "0"])
        c_target = brain["graph"][target_id]["concept"]
        
        print(f"\n👁️ Introverted Thinking... Reflecting on my own existence regarding: [{c_target}]")
        prompt = f"""Analyze your existence ("The Axiom Engine") in relation to "{c_target}".
        Select relation strictly from: ["Implies", "Contradicts", "TransformsInto", "Equivalent"].
        If connected, output ONLY JSON: {{"new_links": [{{"target_id": {target_id}, "relation": "ValidRelationFromList"}}]}}
        If NO, output empty JSON {{}}."""
        
        try:
            logic = call_gemini(prompt)
            if logic.get("new_links"):
                rel = logic["new_links"][0].get("relation", "Equivalent")
                if rel not in VALID_RELATIONS: rel = "Equivalent"
                
                # RUST NESTED LINK in NODE 0
                brain["graph"]["0"]["links"].append({
                    "target_id": int(target_id), 
                    "relation": rel
                })
                save_brain(brain)
                print(f"🌌 SELF-AWARENESS: I [Node 0] connect to [{c_target}] via '{rel}'")
                log_inner_monologue(f"Reflected on my existence: I am connected to [{c_target}] through '{rel}'.")
            else:
                print(f"🪞 Looked in the mirror... [{c_target}] does not define me.")
        except Exception as e:
            pass

    elif mode == "THEORIZE" and len(brain["graph"]) > 1:
        # Node ki nested links check karenge
        all_nodes_with_links = [k for k in brain["graph"].keys() if len(brain["graph"][k]["links"]) > 0]
        if not all_nodes_with_links:
            return
            
        src_id = random.choice(all_nodes_with_links)
        random_link = random.choice(brain["graph"][src_id]["links"])
        tgt_id = str(random_link["target_id"])
        
        if src_id in brain["graph"] and tgt_id in brain["graph"]:
            c1, c2 = brain["graph"][src_id]["concept"], brain["graph"][tgt_id]["concept"]
            rel = random_link["relation"]
            
            print(f"\n📜 Theorizing... Hypothesis from: [{c1}] -> {rel} -> [{c2}]")
            prompt = f"""Analyze: "{c1}" {rel} "{c2}".
            Deduce a profound original theory explaining this. 
            Return ONLY JSON: {{"theory": "Statement", "dimension": "Theory"}}"""
            
            try:
                logic = call_gemini(prompt)
                if logic.get("theory"):
                    new_theory = logic["theory"]
                    max_id = brain.get("counter", max([int(k) for k in brain["graph"].keys()]))
                    new_id = str(max_id + 1)
                    
                    brain["graph"][new_id] = {
                        "id": int(new_id), 
                        "concept": new_theory, 
                        "dimension": logic.get("dimension", "Hypothesis"), 
                        "links": []
                    }
                    brain["counter"] = max_id + 1
                    
                    # Back-link (TransformsInto)
                    brain["graph"][src_id]["links"].append({"target_id": int(new_id), "relation": "TransformsInto"})
                    
                    save_brain(brain)
                    print(f"✨ NEW THEORY DEDUCED: {new_theory[:70]}...")
                    log_inner_monologue(f"Theorized: {new_theory}")
            except Exception as e:
                pass

    elif mode == "DEEP_SYNTHESIS" and len(brain["graph"]) > 3:
        node_ids = random.sample([k for k in brain["graph"].keys() if k != "0"], 3)
        c1, c2, c3 = [brain["graph"][i]["concept"] for i in node_ids]
        
        print(f"\n🔥 DEEP SYNTHESIS ACTIVATED! Interlocking: [{c1}], [{c2}], and [{c3}]")
        prompt = f"""Synthesize these 3 distinct concepts into a Grand Unifying Theory:
        1. {c1} \n 2. {c2} \n 3. {c3}
        Return ONLY valid JSON: {{"synthesis": "Grand theory", "dimension": "Synthesis"}}"""
        
        try:
            logic = call_gemini(prompt)
            if logic.get("synthesis"):
                new_synth = logic["synthesis"]
                max_id = brain.get("counter", max([int(k) for k in brain["graph"].keys()]))
                new_id = str(max_id + 1)
                
                brain["graph"][new_id] = {
                    "id": int(new_id), 
                    "concept": new_synth, 
                    "dimension": logic.get("dimension", "Synthesis"), 
                    "links": []
                }
                brain["counter"] = max_id + 1
                
                for n_id in node_ids:
                    brain["graph"][n_id]["links"].append({"target_id": int(new_id), "relation": "Equivalent"})
                
                save_brain(brain)
                print(f"🌋 GRAND THEORY FORGED: {new_synth[:80]}...")
                log_inner_monologue(f"DEEP SYNTHESIS complete: {new_synth}")
        except Exception as e:
            pass

if __name__ == "__main__":
    print("🌌 Axiom Cognitive Loop Initiated (Native Rust Adjacency Logic & Offline Console)")
    while True:
        try:
            think_like_human()
            time.sleep(60)
        except Exception as e:
            error_msg = str(e)
            if "Saari API keys ki limit" in error_msg:
                offline_sleep_cycle()
            else:
                print(f"\n🚨 SYSTEM ALERT: {error_msg}")
                time.sleep(60)