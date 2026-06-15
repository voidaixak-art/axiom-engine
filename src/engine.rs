// src/engine.rs

use std::collections::{HashMap, HashSet};
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum Relation {
    Implies,
    Contradicts,
    TransformsInto,
    Equivalent,
    Evolved_Vector_Link, // Mutator ka naya relation support
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CausalLink {
    pub target_id: u64,
    pub relation: Relation,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub confidence: Option<f64>, // Mutation ka score save karne ke liye
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Node {
    pub id: u64,
    pub concept: String,
    pub dimension: String,
    pub links: Vec<CausalLink>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub vector: Option<Vec<f64>>, // 50-Dimensional math array
}

#[derive(Serialize, Deserialize)] 
pub struct AxiomEngine {
    pub graph: HashMap<u64, Node>,
    pub counter: u64,
}

impl AxiomEngine {
    pub fn new() -> Self {
        AxiomEngine { graph: HashMap::new(), counter: 0 }
    }

    pub fn add_node(&mut self, concept: &str, dimension: &str) -> u64 {
        self.counter += 1;
        let node = Node {
            id: self.counter,
            concept: concept.to_string(),
            dimension: dimension.to_string(),
            links: Vec::new(),
            vector: None, // By default naya node bina vector ke banega
        };
        self.graph.insert(self.counter, node);
        self.counter
    }

    pub fn add_link(&mut self, source_id: u64, target_id: u64, relation: Relation) {
        if let Some(source_node) = self.graph.get_mut(&source_id) {
            source_node.links.push(CausalLink { 
                target_id, 
                relation,
                confidence: None,
            });
        }
    }

    // --- RECURSIVE DEEP REASONING ---
    pub fn verify_deduction(&self, start_id: u64, goal_id: u64) -> bool {
        let mut visited = HashSet::new();
        self.recursive_dfs(start_id, goal_id, &mut visited)
    }

    fn recursive_dfs(&self, current: u64, goal: u64, visited: &mut HashSet<u64>) -> bool {
        if current == goal { return true; }
        visited.insert(current);

        if let Some(node) = self.graph.get(&current) {
            for link in &node.links {
                if !visited.contains(&link.target_id) {
                    // Engine ab 'Evolved_Vector_Link' ke raste bhi chal kar sochega
                    if matches!(link.relation, Relation::Implies | Relation::Equivalent | Relation::TransformsInto | Relation::Evolved_Vector_Link) {
                        if self.recursive_dfs(link.target_id, goal, visited) {
                            return true;
                        }
                    }
                }
            }
        }
        false
    }

    // --- SELF-HEALING: CONFLICT RESOLUTION ---
    pub fn resolve_contradiction(&mut self, id1: u64, id2: u64) {
        if let Some(node) = self.graph.get_mut(&id1) {
            node.links.retain(|l| !(l.target_id == id2 && l.relation == Relation::Contradicts));
        }
        println!("[SYSTEM] Contradiction between {} and {} healed.", id1, id2);
    }

    pub fn check_consistency(&self) -> Vec<(u64, u64)> {
        let mut conflicts = Vec::new();
        for (id, node) in &self.graph {
            for link in &node.links {
                if link.relation == Relation::Contradicts {
                    conflicts.push((*id, link.target_id));
                }
            }
        }
        conflicts
    }

    // --- CONTEXT RETRIEVAL (RAG ENGINE) ---
    pub fn retrieve_context(&self, query: &str) -> String {
        // Query ko words me todo (sirf bade words, 'is', 'the' ko ignore karo)
        let query_words: Vec<&str> = query.split_whitespace().filter(|w| w.len() > 3).collect();
        
        let mut scored_nodes: Vec<(&Node, usize)> = self.graph.values().map(|n| {
            let mut score = 0;
            let concept_lower = n.concept.to_lowercase();
            let dimension_lower = n.dimension.to_lowercase();
            
            for word in &query_words {
                let word_lower = word.to_lowercase();
                if concept_lower.contains(&word_lower) || dimension_lower.contains(&word_lower) {
                    score += 1;
                }
            }
            (n, score)
        }).collect();

        // Jiska score sabse zyada, use upar rakho
        scored_nodes.sort_by(|a, b| b.1.cmp(&a.1));

        let mut context = String::from("Axiom Engine Core Logic (STRICT CONTEXT):\n");
        let mut added = 0;
        
        // Sirf top 5 sabse relevant nodes uthao
        for (node, score) in scored_nodes {
            if score > 0 && added < 5 { 
                context.push_str(&format!("- [Node {}]: {}\n", node.id, node.concept));
                added += 1;
            }
        }
        
        if added == 0 {
            return "No specific axioms mapped. Use pure determinism and logical reasoning.".to_string();
        }
        
        context
    }
}