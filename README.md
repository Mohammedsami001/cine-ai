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
git clone https://github.com/Mohammedsami001/gemini-live-agent-challenge.git
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

## 👥 Team

- [Your Name] — [Your Role]
- [Teammate Name] — [Their Role]
