// src/main.rs
mod engine;
mod storage;
mod cli;
mod llm_bridge;

use storage::StorageManager;

fn main() {
    let filename = "brain.json";
    
    let brain = if std::path::Path::new(filename).exists() {
        StorageManager::load(filename)
    } else {
        engine::AxiomEngine::new()
    };

    cli::run_interface(brain, filename);
}