// src/storage.rs
use crate::engine::AxiomEngine;
use std::fs::File;
use std::io::{Write, Read};

pub struct StorageManager;

impl StorageManager {
    pub fn save(engine: &AxiomEngine, path: &str) -> Result<(), std::io::Error> {
        let json = serde_json::to_string_pretty(engine)?;
        let mut file = File::create(path)?;
        file.write_all(json.as_bytes())?;
        println!("[MEMORY] Brain state saved to {}", path);
        Ok(())
    }

    pub fn load(path: &str) -> AxiomEngine {
        let mut file = File::open(path).expect("[ERROR] Brain file not found!");
        let mut data = String::new();
        file.read_to_string(&mut data).expect("[ERROR] Failed to read brain file!");
        serde_json::from_str(&data).expect("[ERROR] Brain data corrupted!")
    }
}