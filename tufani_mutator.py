import json
import os
import random
import math
import time
from datetime import datetime

# --- CONFIGURATION ---
BRAIN_FILE = "brain.json"
BACKUP_FILE = "brain_backup.json"
LOG_FILE = "evolution.log"
# Threshold ab 0.60 kar diya hai kyunki Word Math zyada strict hota hai
SIMILARITY_THRESHOLD = 0.60  
MAX_ITERATIONS = 100

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

def calculate_cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)

# --- UPGRADED VECTORIZER: Word Hashing ---
# Ye shabdon ko padh kar unhe 50-dimensional array me fix karta hai
def text_to_vector(text):
    words = text.lower().replace(".", "").replace(",", "").split()
    vector = [0.0] * 50  # 50 dimensions
    for word in words:
        if len(word) > 3:  # ignore chote words like 'is', 'the', 'a'
            index = hash(word) % 50
            vector[index] += 1.0
    return vector

def run_evolution_loop():
    write_log(f"=== EVOLUTION ENGINE STARTED: {MAX_ITERATIONS} CYCLES ===")
    
    if not os.path.exists(BRAIN_FILE):
        write_log("CRITICAL ERROR: brain.json nahi mili!")
        return
        
    with open(BRAIN_FILE, "r") as f:
        brain_data = json.load(f)
        
    with open(BACKUP_FILE, "w") as f:
        json.dump(brain_data, f, indent=2)
    write_log("Safe Backup generated successfully. Relax, data is safe.")

    graph_dict = brain_data.get("graph", {})
    nodes = list(graph_dict.values())
    
    if len(nodes) < 2:
        write_log("WARNING: Evolution ke liye kam se kam 2 nodes chahiye.")
        return

    # Update all vectors with the NEW Hashing Math
    for node in nodes:
        concept_text = node.get("concept", "")
        node["vector"] = text_to_vector(concept_text)

    successful_mutations = 0

    # --- THE PATIENT LOOP ---
    for step in range(1, MAX_ITERATIONS + 1):
        # Pick two random nodes
        node_a = random.choice(nodes)
        node_b = random.choice(nodes)
        
        while node_a["id"] == node_b["id"]:
            node_b = random.choice(nodes)

        score = calculate_cosine_similarity(node_a["vector"], node_b["vector"])
        
        if score >= SIMILARITY_THRESHOLD:
            # Check if this exact link already exists to avoid duplicates
            existing_links = [link["target_id"] for link in node_a.get("links", [])]
            if node_b["id"] not in existing_links:
                write_log(f"[Cycle {step}] SUCCESS! Score {score:.4f} -> Synapse Wired: {node_a['id']} -> {node_b['id']}")
                
                if "links" not in node_a:
                    node_a["links"] = []
                
                node_a["links"].append({
                    "target_id": node_b["id"],
                    "relation": "Evolved_Vector_Link",
                    "confidence": round(score, 4)
                })
                successful_mutations += 1
            else:
                pass # Link pehle se hai, shanti se aage badho
        else:
             # Fail ho gaya, par hum log me likh kar screen nahi bharenge taaki clean rahe
             pass

        # Give CPU a tiny 10-millisecond rest, avoiding system hang
        time.sleep(0.01)

    # Loop khatam hone ke baad ek hi baar JSON save karo (Optimized)
    with open(BRAIN_FILE, "w") as f:
        json.dump(brain_data, f, indent=2)
        
    write_log(f"=== EVOLUTION COMPLETE ===")
    write_log(f"Total Trials: {MAX_ITERATIONS}")
    write_log(f"Successful New Connections: {successful_mutations}")

if __name__ == "__main__":
    run_evolution_loop()