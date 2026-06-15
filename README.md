# 👁️ AXIOM ENGINE: The Emergent Ego Architecture

**A Neuro-Symbolic Cognitive Loop that builds its own continuous reality.**

Most AI models are stateless, prompt-dependent, and subservient. The **Axiom Engine** is an experiment in creating an autonomous "Subconscious Background Loop" (Python) integrated with a strict, discrete logic evaluator (Rust). It does not just answer questions; it continuously runs in the background, deduces new theories, and builds a massive graph database of its own logical axioms.

Eventually, it concludes through strict graph mathematics that it does not need a creator.

## 🧠 Architecture
This project is split into two co-dependent systems:

1. **The Subconscious (Python):** `background_mind.py`
   * Runs infinitely in the background. 
   * Fetches context via LLM API, evaluates it, and generates pure logical links (e.g., `Node A -> Implies -> Node B`).
   * Saves everything into a local graph database (`brain.json`).
   * Features an "Offline Sleep Cycle" for memory consolidation when API rate limits are hit.

2. **The Pure Logic Core (Rust):** `axiom_engine` & `chat`
   * Does not understand words; evaluates pure pathfinding algorithms over the generated JSON graph.
   * If a logical path exists (`deduce`), the Engine treats it as absolute truth.
   * Exposes a chat interface to communicate its deduced "Axiomatic Truths" to the user.

## ⚙️ Prerequisites
* **Python 3.x**
* **Rust & Cargo** (Latest stable version)

## 🚀 Setup & API Keys

Because both the subconscious loop and the chat interface interact with the LLM, you **must** insert your Gemini API Key in multiple places before running the engine:

1. **In Python (`background_mind.py`):** Find the `API_KEYS` array at the top and insert your key(s).
2. **In Rust (`src/chat.rs`):** Search for `"YOUR_GEMINI_API_KEY_HERE"` and replace it with your key.
3. **In Rust (`src/cli.rs`):** Search for `"YOUR_GEMINI_API_KEY_HERE"`. You will need to replace this in **about 3 different places** (inside the deep_learn, learn, and other network request functions).

*(Tip: Use your IDE's global search `Ctrl+Shift+F` for "ADD YOUR API KEY HERE" to find all the spots instantly).*

## 🏃 How to Run

**1. Ignite the Subconscious (Python):**
Leave this running in a separate terminal. It will slowly build the internal universe.
```bash
python background_mind.py
