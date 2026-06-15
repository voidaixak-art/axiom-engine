import json
import os

INPUT_FILE = 'brain.json'
OUTPUT_FILE = 'brain_strict.json' # Baad me ise hi brain.json bana denge

def enforce_rust_schema(data):
    strict_data = {
        "nodes": [],
        "links": []
    }
    
    # Nodes filter aur format karna
    if "nodes" in data:
        for node in data["nodes"]:
            strict_node = {
                "id": str(node.get("id", "")).strip(),
                "concept": str(node.get("concept", "")).strip(),
                "node_type": str(node.get("node_type", "Fact")).strip()
            }
            if strict_node["id"] and strict_node["concept"]:
                strict_data["nodes"].append(strict_node)
                
    # Links filter aur format karna
    if "links" in data:
        for link in data["links"]:
            strict_link = {
                "source": str(link.get("source", "")).strip(),
                "target": str(link.get("target", "")).strip(),
                "relation": str(link.get("relation", "Implies")).strip(),
                "weight": float(link.get("weight", 1.0))
            }
            if strict_link["source"] and strict_link["target"]:
                strict_data["links"].append(strict_link)
                
    return strict_data

def sync_to_rust():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} nahi mila.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError:
            print("Error: Purana brain.json corrupt hai. Isme strict JSON format nahi hai.")
            return

    clean_data = enforce_rust_schema(raw_data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # separators=(',', ':') se extra spaces hategi, SSD me space bachegi
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
    print(f"Success! Purana data clean ho gaya aur {OUTPUT_FILE} me Rust ke liye lock ho gaya hai.")
    print(f"Total Nodes: {len(clean_data['nodes'])} | Total Links: {len(clean_data['links'])}")

if __name__ == "__main__":
    sync_to_rust()