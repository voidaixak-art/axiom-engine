// src/reasoner.rs - Logic Engine

use crate::engine::{AxiomEngine, Relation};

impl AxiomEngine {
    // 1. DEDUCTION: Kya 'start' node se 'goal' node tak koi logical path hai?
    pub fn verify_deduction(&self, start_id: u64, goal_id: u64) -> bool {
        let mut visited = std::collections::HashSet::new();
        let mut stack = vec![start_id];

        while let Some(current_id) = stack.pop() {
            if current_id == goal_id { return true; }
            
            if visited.insert(current_id) {
                if let Some(node) = self.graph.get(&current_id) {
                    for link in &node.links {
                        // Agar relation 'Implies' ya 'Equivalent' hai, toh aage badho
                        if matches!(link.relation, Relation::Implies | Relation::Equivalent) {
                            stack.push(link.target_id);
                        }
                    }
                }
            }
        }
        false
    }

    // 2. CONTRADICTION CHECK: Kya graph mein koi 'Contradicts' link exists karta hai?
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
}