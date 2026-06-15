// src/cli.rs
use crate::engine::{AxiomEngine, Relation};
use crate::storage::StorageManager;
use crate::llm_bridge; 
use std::collections::HashMap;
use std::io::{self, Write};
use std::fs;

pub fn run_interface(mut brain: AxiomEngine, filename: &str) {
    println!("=== AXIOM ENGINE v0.4 (Fractal Scholar Kernel Active) ===");
    print_help();

    loop {
        print!("\n> ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let cmd = input.trim();

        match cmd {
            "help" => print_help(),
            
            "list" => {
                println!("\n--- Current Axiom Graph ---");
                if brain.graph.is_empty() { println!("Graph is empty. Add nodes."); }
                for (id, node) in &brain.graph {
                    println!("[ID: {}] {} (Dim: {})", id, node.concept, node.dimension);
                }
            },

            // === THE NEURAL DASHBOARD COMMANDS (NEW) ===
            "stats" => {
                let file_data = fs::read_to_string(filename).unwrap_or_else(|_| "{}".to_string());
                if let Ok(json) = serde_json::from_str::<serde_json::Value>(&file_data) {
                    let node_count = json["graph"].as_object().map_or(0, |m| m.len());
                    let link_count = json["links"].as_array().map_or(0, |a| a.len());
                    
                    println!("\n📊 AXIOM ENGINE - NEURAL STATS");
                    println!("===============================");
                    println!("🟢 Total Concepts (Nodes) : {}", node_count);
                    println!("🔗 Total Connections (Links): {}", link_count);
                    
                    if node_count > 0 {
                        let density = (link_count as f64) / (node_count as f64);
                        println!("🧠 Neural Density        : {:.2} links per node\n", density);
                    }
                } else {
                    println!("[ERROR] Could not read stats. Check if brain.json exists.");
                }
            },

            "links" => {
                println!("\n🔗 AXIOM ENGINE - ACTIVE SYNAPSES (LINKS)");
                println!("=========================================");
                let file_data = fs::read_to_string(filename).unwrap_or_else(|_| "{}".to_string());
                if let Ok(json) = serde_json::from_str::<serde_json::Value>(&file_data) {
                    if let Some(links) = json["links"].as_array() {
                        if links.is_empty() {
                            println!("No links formed yet. Give the engine some time to think.");
                        } else {
                            for link in links {
                                let source_id = link["source"].as_i64().unwrap_or(0).to_string();
                                let target_id = link["target"].as_i64().unwrap_or(0).to_string();
                                let relation = link["relation"].as_str().unwrap_or("Connected To");

                                let source_name = json["graph"][&source_id]["concept"].as_str().unwrap_or("Unknown Node");
                                let target_name = json["graph"][&target_id]["concept"].as_str().unwrap_or("Unknown Node");

                                println!("▶ [{}] ---({})---> [{}]", source_name, relation, target_name);
                            }
                        }
                    } else {
                        println!("No links found in the current graph.");
                    }
                } else {
                    println!("[ERROR] Could not parse links from brain.json.");
                }
                println!();
            },

            // === THE CONVERSATIONAL COMMAND ===
            "chat" => {
                let text = prompt("You: ");
                let api_key = "ADD YOUR API KEY HERE";
                llm_bridge::chat_with_engine(&text, api_key);
            },

            // === THE MACRO-LEARNING COMMAND ===
            "deep_learn" => {
                let topic = prompt("Enter the broad Subject/Topic (e.g., 'Linear Algebra', 'Quantum Mechanics'): ");
                println!("📚 Dimaag poora subject scan kar raha hai... It might take a few seconds.");

                let api_key = "ADD YOUR API KEY HERE";

                if let Some(logic_json) = llm_bridge::ask_gemini_deep_learn(&topic, api_key) {
                    
                    let mut name_to_id: HashMap<String, u64> = HashMap::new();
                    for (id, node) in &brain.graph {
                        name_to_id.insert(node.concept.clone(), *id);
                    }
                    
                    let mut count = 0; 

                    if let Some(nodes) = logic_json["new_nodes"].as_array() {
                        for n in nodes {
                            let concept = n["concept"].as_str().unwrap_or("").to_string();
                            let dim = n["dimension"].as_str().unwrap_or("General").to_string();
                            
                            if !name_to_id.contains_key(&concept) {
                                let new_id = brain.add_node(&concept, &dim);
                                name_to_id.insert(concept.clone(), new_id);
                                count += 1;
                            }
                        }
                    }

                    if let Some(links) = logic_json["new_links"].as_array() {
                        for l in links {
                            let source_name = l["source"].as_str().unwrap_or("");
                            let target_name = l["target"].as_str().unwrap_or("");
                            let rel_str = l["relation"].as_str().unwrap_or("Implies");

                            let rel = match rel_str {
                                "Contradicts" => Relation::Contradicts,
                                "TransformsInto" => Relation::TransformsInto,
                                "Equivalent" => Relation::Equivalent,
                                _ => Relation::Implies,
                            };

                            if let (Some(&s_id), Some(&t_id)) = (name_to_id.get(source_name), name_to_id.get(target_name)) {
                                brain.add_link(s_id, t_id, rel);
                            }
                        }
                    }
                    
                    StorageManager::save(&brain, filename).unwrap();
                    println!("[SUCCESS] Massive Knowledge Downloaded! Added {} new core concepts to brain.json.", count);

                } else {
                    println!("[FAILURE] Could not map the subject.");
                }
            },

            // === THE ZOOM-IN COMMAND ===
            "expand" => {
                let id_str = prompt("Enter Node ID to expand and deep-dive into: ");
                if let Ok(target_id) = id_str.parse::<u64>() {
                    if let Some(node) = brain.graph.get(&target_id) {
                        let concept_name = node.concept.clone();
                        println!("🔬 Zooming into '{}'. Downloading deep knowledge...", concept_name);
                        
                        let api_key = "ADD YOUR API KEY HERE";
                        
                        if let Some(logic_json) = llm_bridge::ask_gemini_deep_learn(&concept_name, api_key) {
                            let mut name_to_id: HashMap<String, u64> = HashMap::new();
                            for (id, existing_node) in &brain.graph {
                                name_to_id.insert(existing_node.concept.clone(), *id);
                            }
                            
                            let mut count = 0;
                            if let Some(nodes) = logic_json["new_nodes"].as_array() {
                                for n in nodes {
                                    let c = n["concept"].as_str().unwrap_or("").to_string();
                                    let d = n["dimension"].as_str().unwrap_or("General").to_string();
                                    if !name_to_id.contains_key(&c) {
                                        let new_id = brain.add_node(&c, &d);
                                        name_to_id.insert(c.clone(), new_id);
                                        brain.add_link(target_id, new_id, Relation::Implies);
                                        count += 1;
                                    }
                                }
                            }
                            
                            if let Some(links) = logic_json["new_links"].as_array() {
                                for l in links {
                                    let s_name = l["source"].as_str().unwrap_or("");
                                    let t_name = l["target"].as_str().unwrap_or("");
                                    let rel_str = l["relation"].as_str().unwrap_or("Implies");
                                    let rel = match rel_str {
                                        "Contradicts" => Relation::Contradicts,
                                        "TransformsInto" => Relation::TransformsInto,
                                        "Equivalent" => Relation::Equivalent,
                                        _ => Relation::Implies,
                                    };
                                    if let (Some(&s_id), Some(&t_id)) = (name_to_id.get(s_name), name_to_id.get(t_name)) {
                                        brain.add_link(s_id, t_id, rel);
                                    }
                                }
                            }
                            StorageManager::save(&brain, filename).unwrap();
                            println!("[SUCCESS] Expanded '{}'. Added {} deep concepts to brain.json.", concept_name, count);
                        } else {
                            println!("[FAILURE] Could not expand the node.");
                        }
                    } else {
                        println!("Node ID not found.");
                    }
                } else {
                    println!("Invalid ID format.");
                }
            },

            // === THE MICRO-LEARNING COMMAND ===
            "learn" => {
                let text = prompt("Enter text/concept for Engine to learn: ");
                println!("🧠 Dimaag soch raha hai... (Calling Gemini AI)");

                let api_key = "AIzaSyCtVCSVi5dKXcZJpYt3RtgpAH3WtO_tJUw";

                if let Some(logic_json) = llm_bridge::ask_gemini_to_extract_logic(&text, api_key) {
                    
                    let mut name_to_id: HashMap<String, u64> = HashMap::new();
                    for (id, node) in &brain.graph {
                        name_to_id.insert(node.concept.clone(), *id);
                    }

                    if let Some(nodes) = logic_json["new_nodes"].as_array() {
                        for n in nodes {
                            let concept = n["concept"].as_str().unwrap_or("").to_string();
                            let dim = n["dimension"].as_str().unwrap_or("General").to_string();
                            
                            if !name_to_id.contains_key(&concept) {
                                let new_id = brain.add_node(&concept, &dim);
                                name_to_id.insert(concept.clone(), new_id);
                                println!("🟢 Learned Concept: {} [ID: {}]", concept, new_id);
                            }
                        }
                    }

                    if let Some(links) = logic_json["new_links"].as_array() {
                        for l in links {
                            let source_name = l["source"].as_str().unwrap_or("");
                            let target_name = l["target"].as_str().unwrap_or("");
                            let rel_str = l["relation"].as_str().unwrap_or("Implies");

                            let rel = match rel_str {
                                "Contradicts" => Relation::Contradicts,
                                "TransformsInto" => Relation::TransformsInto,
                                "Equivalent" => Relation::Equivalent,
                                _ => Relation::Implies,
                            };

                            if let (Some(&s_id), Some(&t_id)) = (name_to_id.get(source_name), name_to_id.get(target_name)) {
                                brain.add_link(s_id, t_id, rel);
                                println!("🔗 Learned Logic: {} -> {}", source_name, target_name);
                            }
                        }
                    }
                    
                    StorageManager::save(&brain, filename).unwrap();
                    println!("[SUCCESS] Knowledge merged into brain.json.");

                } else {
                    println!("[FAILURE] Could not extract logical logic from input.");
                }
            },

            "add_node" => {
                let concept = prompt("Concept Name: ");
                let dim = prompt("Dimension (e.g., Classical, Quantum): ");
                let id = brain.add_node(&concept, &dim);
                println!("Node created with ID: {}", id);
            },

            "add_link" => {
                let s_str = prompt("Source ID: ");
                let t_str = prompt("Target ID: ");
                let r_str = prompt("Relation (1:Implies, 2:Contradicts, 3:Transforms, 4:Equivalent): ");
                
                let rel = match r_str.as_str() {
                    "2" => Relation::Contradicts,
                    "3" => Relation::TransformsInto,
                    "4" => Relation::Equivalent,
                    _ => Relation::Implies,
                };

                if let (Ok(s), Ok(t)) = (s_str.parse::<u64>(), t_str.parse::<u64>()) {
                    brain.add_link(s, t, rel);
                    println!("Link established.");
                } else {
                    println!("Error: IDs must be numbers.");
                }
            },

            "deduce" => {
                let s = prompt("Start Node ID: ").parse::<u64>().unwrap_or(0);
                let g = prompt("Goal Node ID: ").parse::<u64>().unwrap_or(0);
                
                if brain.verify_deduction(s, g) {
                    println!("[SUCCESS] Logical path exists from {} to {}.", s, g);
                } else {
                    println!("[FAILURE] No logical path found.");
                }
            },

            "check" => {
                let conflicts = brain.check_consistency();
                if conflicts.is_empty() { println!("System Status: STABLE."); }
                else { println!("ALERT: {} contradictions found.", conflicts.len()); }
            },

            "heal" => {
                let conflicts = brain.check_consistency();
                for (c1, c2) in conflicts { brain.resolve_contradiction(c1, c2); }
                StorageManager::save(&brain, filename).unwrap();
                println!("System healed and state saved.");
            },

            "exit" => {
                StorageManager::save(&brain, filename).unwrap();
                println!("System saved. Shutdown.");
                break;
            },
            _ => println!("Unknown command. Type 'help' for options."),
        }
    }
}

fn print_help() {
    println!("\nCommands:");
    println!("  stats      - Check Engine scale and link density (NEW)");
    println!("  links      - See exact logical connections/theories (NEW)");
    println!("  list       - Show all nodes");
    println!("  chat       - Talk to the Engine naturally");
    println!("  deep_learn - Map an entire subject at once");
    println!("  expand     - Deep-dive into a specific Node ID to expand syllabus");
    println!("  learn      - Let Engine read text and learn logic automatically");
    println!("  add_node   - Create new logic node");
    println!("  add_link   - Connect two nodes");
    println!("  deduce     - Check if Path exists (Reasoning)");
    println!("  check      - Stability check");
    println!("  heal       - Remove contradictions");
    println!("  exit       - Save and quit");
}

fn prompt(msg: &str) -> String {
    print!("{}", msg);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().to_string()
}