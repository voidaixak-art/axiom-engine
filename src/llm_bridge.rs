use std::process::Command;
use serde_json::Value;

pub fn ask_gemini_to_extract_logic(text: &str, api_key: &str) -> Option<Value> {
    // Rust is executing the Python script as a background process!
    let output = Command::new("python")
        .arg("gemini_eyes.py")
        .arg(text)
        .arg(api_key)
        .output()
        .expect("Failed to execute python script. Make sure Python is installed.");

    if output.status.success() {
        // Read the JSON printed by Python
        let json_str = String::from_utf8_lossy(&output.stdout);
        serde_json::from_str(&json_str).ok()
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        println!("Python Bridge Error: {}", err);
        None
    }
}

pub fn chat_with_engine(text: &str, api_key: &str) -> String {
    let output = Command::new("python")
        .arg("gemini_mouth.py")
        .arg(text)
        .arg(api_key)
        .output()
        .expect("Failed to execute gemini_mouth.py");

    if output.status.success() {
        // Ab hum terminal pe print nahi kar rahe, UI ko string wapas bhej rahe hain
        String::from_utf8_lossy(&output.stdout).trim().to_string()
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        format!("Error communicating with Voice Module: {}", err)
    }
}

pub fn ask_gemini_deep_learn(topic: &str, api_key: &str) -> Option<Value> {
    let output = Command::new("python")
        .arg("gemini_scholar.py")
        .arg(topic)
        .arg(api_key)
        .output()
        .expect("Failed to execute gemini_scholar.py");

    if output.status.success() {
        let json_str = String::from_utf8_lossy(&output.stdout);
        serde_json::from_str(&json_str).ok()
    } else {
        let err = String::from_utf8_lossy(&output.stderr);
        println!("Scholar Module Error: {}", err);
        None
    }
}