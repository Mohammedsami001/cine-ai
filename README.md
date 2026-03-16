# 🎬 CINE AI

> The First Fully Autonomous AI Production Studio — Built for the Google Gemini Live Agent Challenge

## 🎯 Problem

Filmmakers and creative writers have no unified AI tool that thinks like both a
Director AND a Screenplay Writer — one that can write, visualize, and animate
ideas in a single seamless workflow.

## 💡 Solution

Cine AI is a multimodal agentic AI assistant that uses an intelligent
routing ageent to automatically decide whether to write a screenplay, generate
concept art, or produce a cinematic video — all from one natural language prompt.

## 🏗️ Architecture

```
[User Prompt + Optional Image]
         ↓
  [Streamlit UI]
         ↓
[Intent Router Agent — Gemini 2.5 Flash on Vertex AI]
    ↓           ↓              ↓
 [WRITE]     [IMAGE]        [VIDEO]
    ↓           ↓              ↓
[Writer-   [Art Director  [Director
 Director   Agent →        Agent →
 Agent]     Gemini Image]  Veo 3.1]
    ↓           ↓              ↓
[Script]  [Concept Art]  [Video File]
         ↑________________________|
            [Vertex AI — GCP]
```

## 🛠️ Tech Stack

| Layer                 | Technology                                      |
| --------------------- | ----------------------------------------------- |
| LLM Routing + Writing | Gemini 2.5 Flash via Vertex AI                  |
| Image Generation      | Gemini Image Model (gemini-3-pro-image-preview) |
| Video Generation      | Veo 3.1 (veo-3.1-generate-preview)              |
| Cloud Backend         | Google Vertex AI (aiplatform.googleapis.com)    |
| SDK                   | Google GenAI SDK (google-genai)                 |
| Frontend              | Streamlit                                       |

## ☁️ Google Cloud Services Used

- **Vertex AI** — All Gemini model calls routed through Vertex AI backend
- **Project:** tribal-quest-490419-s4

## 🚀 Setup & Run Locally

### Prerequisites

- Python 3.11+
- Google Cloud CLI → [Install here](https://cloud.google.com/sdk/docs/install)
- A Google Cloud project with Vertex AI API enabled

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/Mohammedsami001/cine-ai.git
cd cine-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
cp .env.example .env
# Edit .env and add your keys

# 4. Authenticate with Google Cloud
gcloud auth application-default login
gcloud config set project tribal-quest-490419-s4

# 5. Run the app
streamlit run app.py
```

## 🎬 Features

- **Agentic Routing** — Automatically detects if you want to write, visualize, or animate
- **Screenplay Mode** — Industry-format scripts with Director's Notes
- **Concept Art Mode** — Art Director agent translates context into visual briefs → generates images
- **Video Mode** — Hollywood Director agent structures prompts → Veo 3.1 renders cinematic video
- **Multimodal Input** — Upload reference images for art direction
- **Conversation Memory** — Context carries across all three modes

## 📁 GCP Proof

See `/assets/gcp_proof/` for screenshots of live Vertex AI API calls.

---

## 🧪 Reproducible Testing for Judges

To verify the autonomous routing and multimodal capabilities of CINE AI, please follow this exact sequence of prompts in the chat interface. Do not click any toggles; the Agent will route these automatically.

**Test Case 1: The Screenplay (Triggers WRITE Mode)**

1. Type: `Write an intense opening scene for a sci-fi thriller set in a neon-lit cyberpunk diner. Include director's notes.`
2. **Expected Result:** The Agent will output `AGENT DECISION: WRITE DEPT` and generate a properly formatted screenplay with bolded `[DIRECTOR'S NOTE]` tags.

**Test Case 2: The Concept Art (Triggers IMAGE Mode with Context Memory)**

1. Type: `Generate concept art for the opening wide shot of that diner scene.`
2. **Expected Result:** The Agent will recognize the intent, output `AGENT DECISION: IMAGE DEPT`, extract the visual details from the previous chat history, display the visual brief, and render the concept art image.

**Test Case 3: The Animation (Triggers VIDEO Mode with Context Memory)**

1. Type: `Animate the scene with a slow pan across the diner counter.`
2. **Expected Result:** The Agent will output `AGENT DECISION: VIDEO DEPT`, structure a strict Veo prompt using the visual context of the diner, submit the job to the Render Farm, and display the final `.mp4` cinematic sequence.

---

## 👥 Team

- [Saish Kharat] 
- [Mohammedsami Sanadi]
- [Sankalp Mhatre]
- [Arjun Thakur]
