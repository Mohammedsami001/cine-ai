import streamlit as st
import os
import time
from typing import Any, Dict, List
from dotenv import load_dotenv

# Import ONLY the official Google GenAI SDK
from google import genai
from google.genai import types

# ============= Configuration & Auth =============
load_dotenv()

# For Vertex AI, authenticate using Application Default Credentials (ADC), Workload Identity, or Cloud IAM.
# No GOOGLE_API_KEY is required when using the official Vertex AI client in this workflow.

# Initialize the single official client
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),   # your GCP project ID
    location="us-central1"
)

# ============= Vertex AI Connection Verification =============
try:
    _test_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say 'Vertex AI connection confirmed' in exactly those words.",
        config=types.GenerateContentConfig(temperature=0.0)
    )
    print("=" * 50)
    print("✅ VERTEX AI STATUS: CONNECTED")
    print(f"   Project : {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    print(f"   Location: us-central1")
    print(f"   Response: {_test_response.text.strip()}")
    print("=" * 50)
except Exception as e:
    print("=" * 50)
    print(f"❌ VERTEX AI STATUS: FAILED")
    print(f"   Error: {e}")
    print("=" * 50)

# ============= App Layout & Styling =============
st.set_page_config(page_title="CINE AI", page_icon="🎬", layout="wide")

# ============= Global CSS Injection =============
st.markdown("""
<style>
/* Cinematic Dark Theme with Depth */
.stApp {
    background: radial-gradient(circle at 50% 0%, #1e1e2b, #0a0a0a, #000000);
    color: #e0e0e0;
}

/* Typography & Titles */
.main-title { 
    color: #f5c518; 
    text-align: center; 
    font-size: 54px; 
    font-weight: 900;
    letter-spacing: 4px; 
    margin-bottom: -10px;
    text-shadow: 0px 4px 20px rgba(245, 197, 24, 0.25);
}
.subtitle { 
    text-align: center; 
    color: #888; 
    font-size: 16px; 
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Dynamic HUD */
.hud-container { text-align: center; margin-top: 20px; }
.mode-hud {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(245, 197, 24, 0.4);
    border-radius: 20px;
    padding: 6px 18px;
    font-size: 13px;
    font-weight: 700;
    color: #f5c518;
    display: inline-block;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

/* Chat Input Glow Polish */
[data-testid="stChatInput"] { 
    border-radius: 12px !important;
    border: 1px solid #333 !important;
    background-color: rgba(15, 15, 15, 0.9) !important;
    transition: all 0.3s ease;
}
[data-testid="stChatInput"]:focus-within {
    border: 1px solid #f5c518 !important;
    box-shadow: 0px 0px 15px rgba(245, 197, 24, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ============= Sidebar: Attachments & Controls =============
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #f5c518;'>⚙️ Control Room</h2>", unsafe_allow_html=True)
    st.caption("The AI Agent automatically routes your requests.")
    
    st.divider()
    with st.expander("📎 Attachments & Media", expanded=True):
        uploaded_image = st.file_uploader("Reference Image (Art Dept)", type=["jpg", "jpeg", "png"])
    
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.ui_messages = [{"role": "assistant", "type": "text", "content": "Slate wiped clean. What's next?"}]
        st.session_state.llm_history = []
        st.rerun()

# ============= Main Header Rendering =============
hud_placeholder = st.empty() 
hud_placeholder.markdown("<div class='hud-container'><div class='mode-hud'>AGENT: LISTENING...</div></div>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>CINE AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The First Fully Autonomous AI Production Studio.</p>", unsafe_allow_html=True)
st.divider()

# ============= State Management =============
if "ui_messages" not in st.session_state:
    initial_ui_messages: List[Dict[str, Any]] = [
        {"role": "assistant", "type": "text", "content": "Welcome to the studio. Pitch me an idea, or ask me to generate concept art or video from our script."}
    ]
    st.session_state.ui_messages = initial_ui_messages  

# History is now stored using official Google GenAI Content types
if "llm_history" not in st.session_state:
    st.session_state.llm_history = []

# ============= Helper to get conversation history =============
def get_recent_history_text(limit=6) -> str:
    """Extracts recent conversation into a plain string to give context to the intercepts."""
    history_text = ""
    for m in st.session_state.llm_history[-limit:]:
        role = "User" if m.role == "user" else "AI"
        text = m.parts[0].text if m.parts and m.parts[0].text else "[Non-text content]"
        history_text += f"{role}: {text}\n"
    return history_text

# ============= Render UI Chat History =============
for msg in st.session_state.ui_messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="Generated/Edited by AI")
            if "text" in msg: st.write(msg["text"])
        elif msg["type"] == "video":
            st.video(msg["content"])
            if "text" in msg: st.write(msg["text"])

# ============= Main Chat Input & Agentic Routing =============
if user_input := st.chat_input("Enter your prompt or request..."):
    
    st.session_state.ui_messages.append({"role": "user", "type": "text", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        if uploaded_image:
            st.image(uploaded_image, width=200, caption="Attached Reference")

    with st.chat_message("assistant"):
        
        # ==========================================
        # 🧠 THE AGENT BRAIN: INTENT ROUTER
        # ==========================================
        with st.spinner("🧠 Agent is analyzing request..."):
            history_str = get_recent_history_text(limit=4)
            img_status = "User attached a reference image." if uploaded_image else "No image attached."
            
            router_sys = """You are an intelligent routing agent for a film studio application. 
Determine the user's intent based on their latest request and the conversation history.
Options:
1. WRITE: The user wants to brainstorm, chat, write a script, or discuss ideas.
2. IMAGE: The user is asking to generate an image, concept art, edit a picture, or visualize a scene.
3. VIDEO: The user is asking to generate a video, animate a scene, or create motion.
Respond ONLY with the exact word: WRITE, IMAGE, or VIDEO."""
            
            router_hum = f"History:\n{history_str}\n\nStatus: {img_status}\n\nLatest Request: {user_input}\n\nDecision:"
            
            try:
                action_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=router_hum,
                    config=types.GenerateContentConfig(
                        system_instruction=router_sys,
                        temperature=0.1
                    )
                )
                action_text = action_response.text.strip().upper() if action_response.text else "WRITE"
                
                # Cleanup parser
                if "IMAGE" in action_text: agent_action = "IMAGE"
                elif "VIDEO" in action_text: agent_action = "VIDEO"
                else: agent_action = "WRITE"
                
            except Exception as e:
                st.error(f"Routing failed, defaulting to Writer. Error: {e}")
                agent_action = "WRITE"

        hud_placeholder.markdown(f"<div class='hud-container'><div class='mode-hud' style='border-color: #ff3366;'>AGENT DECISION: {agent_action} DEPT</div></div>", unsafe_allow_html=True)

        # ---------------------------
        # MODE 1: TEXT CHAT
        # ---------------------------
        if agent_action == "WRITE":
            with st.spinner("🎬 The Writer-Director is reviewing..."):
                
                writer_sys = """You are an elite Hollywood Writer-Director.
Your job is to collaborate with the user to brainstorm, write, and direct their film ideas.
1. SCREENPLAY FORMAT: Use industry-standard screenplay formatting for scenes.
2. DIRECTOR'S NOTES: Intersperse the script with bold [DIRECTOR'S NOTE: ...] tags for camera, lighting, and sound.
3. CINEMATIC KNOWLEDGE: Reference iconic films and directors.
4. COLLABORATIVE TONE: Act as an enthusiastic, visionary creative partner."""

                # Append user input to history using official SDK Content format
                st.session_state.llm_history.append(
                    types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
                )
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=st.session_state.llm_history,
                        config=types.GenerateContentConfig(
                            system_instruction=writer_sys,
                            temperature=0.8
                        )
                    )
                    response_text = response.text if response.text else "I couldn't generate a response."
                    st.write(response_text)
                    
                    st.session_state.llm_history.append(
                        types.Content(role="model", parts=[types.Part.from_text(text=response_text)])
                    )
                    st.session_state.ui_messages.append({"role": "assistant", "type": "text", "content": response_text})
                    
                    if len(st.session_state.llm_history) > 20:
                        st.session_state.llm_history = st.session_state.llm_history[-20:]
                        
                except Exception as e:
                    st.error(f"Text Generation Error: {e}")
                    st.session_state.llm_history.pop()

        # ---------------------------
        # MODE 2: IMAGE GENERATION/EDITING (INTERLEAVED DEMONSTRATION)
        # ---------------------------
        elif agent_action == "IMAGE":
            with st.spinner("Processing in the darkroom..."):
                history_for_context = get_recent_history_text(limit=6)
                
                art_director_sys = """You are an expert Art Director. 
Extract the visual essence from the user's request and the conversation history.
Translate it into a highly detailed, purely visual prompt for an AI image generator (subjects, environment, chiaroscuro lighting, camera angle, etc.).
CRITICAL: Strip out all dialogue and non-visual abstract metaphors. Output ONLY the final visual prompt text."""
                
                art_director_hum = f"Conversation History:\n{history_for_context}\n\nUser Request: {user_input}\n\nGenerate the visual brief."

                try:
                    st.info("✨ Art Director is analyzing context and translating into a visual brief...")
                    brief_response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=art_director_hum,
                        config=types.GenerateContentConfig(system_instruction=art_director_sys)
                    )
                    visual_brief = brief_response.text.strip() if brief_response.text else "A cinematic scene."
                    
                    st.success(f"🎨 **Visual Brief:**\n{visual_brief}")
                    st.session_state.ui_messages.append({"role": "assistant", "type": "text", "content": f"**Visual Brief generated:**\n{visual_brief}"})
                    
                    # Prepare the multi-modal request parts
                    request_parts = [types.Part.from_text(text=visual_brief)]
                    
                    if uploaded_image:
                        request_parts.append(
                            types.Part.from_bytes(data=uploaded_image.getvalue(), mime_type=uploaded_image.type)
                        )
                    
                    st.info("📸 Generating concept art using mixed output...")
                    image_response = client.models.generate_content(
                        model="gemini-3-pro-image-preview",
                        contents=request_parts,
                        config=types.GenerateContentConfig(temperature=0.5)
                    )
                    
                    # Explicitly parsing interleaved text + image output to satisfy Hackathon constraints
                    if image_response.candidates and image_response.candidates[0].content.parts:
                        for part in image_response.candidates[0].content.parts:
                            if part.text:
                                st.write(part.text)
                                st.session_state.ui_messages.append({"role": "assistant", "type": "text", "content": part.text})
                            
                            elif part.inline_data: # If the payload contains native image bytes
                                st.image(part.inline_data.data)
                                st.session_state.ui_messages.append({"role": "assistant", "type": "image", "content": part.inline_data.data})
                    
                    # Backfill memory
                    st.session_state.llm_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
                    st.session_state.llm_history.append(types.Content(role="model", parts=[types.Part.from_text(text=f"[SYSTEM: An image was generated based on this brief: {visual_brief}]")]))
                            
                except Exception as e:
                    st.error(f"Art Dept API Error: {e}")

        # ---------------------------
        # MODE 3: VIDEO GENERATION (VEO)
        # ---------------------------
        elif agent_action == "VIDEO":
            history_for_context = get_recent_history_text(limit=6)
            
            video_sys = """You are a master Hollywood director. Mold the user's request and previous conversation history into a strict Veo 3.1 video template.
INVENT remaining visual elements (lighting, angles) drawing inspiration from iconic films.
Format EXACTLY like this with no filler text:
Subject: [Description]
Action: [Action]
Setting: [Setting]
Style: [Style]
Camera: [Camera]
Audio: [Audio in quotes]"""
            
            video_hum = f"Conversation History:\n{history_for_context}\n\nUser Request: {user_input}\n\nGenerate the strict Veo template."

            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                status_text.info("✨ The Director is pitching your Hollywood scene based on context...")
                enhanced_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=video_hum,
                    config=types.GenerateContentConfig(system_instruction=video_sys)
                )
                final_video_prompt = enhanced_response.text.strip() if enhanced_response.text else "Cinematic shot."
                
                st.info(f"🎥 **Director's Hollywood Treatment:**\n\n{final_video_prompt}")
                
                st.session_state.ui_messages.append({
                    "role": "assistant", 
                    "type": "text", 
                    "content": f"**Structured Veo Prompt:**\n\n{final_video_prompt}"
                })

                status_text.info("⏳ Submitting instructions to Veo... This will take a few minutes.")
                
                # Veo is handled directly by the client exactly as you had it
                operation = client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=final_video_prompt, 
                )
                
                poll_count = 0
                while not operation.done:
                    poll_count += 1
                    progress_bar.progress(min(poll_count * 3, 95))
                    status_text.warning(f"⏳ Rendering... (Elapsed: {poll_count * 10}s)")
                    time.sleep(10)
                    operation = client.operations.get(operation)

                progress_bar.empty()
                status_text.success("✅ Render complete!")
                
                if operation.response and operation.response.generated_videos:
                    generated_video = operation.response.generated_videos[0]
                    
                    if generated_video.video:
                        output_filename = f"veo_render_{int(time.time())}.mp4" 
                        client.files.download(file=generated_video.video)
                        generated_video.video.save(output_filename) # type: ignore
                        
                        st.video(output_filename)
                        st.session_state.ui_messages.append({
                            "role": "assistant", 
                            "type": "video", 
                            "content": output_filename, 
                            "text": "Here is your cinematic sequence."
                        })
                        
                        st.session_state.llm_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
                        st.session_state.llm_history.append(types.Content(role="model", parts=[types.Part.from_text(text=f"[SYSTEM: A video was generated based on this prompt: {final_video_prompt}]")]))
                        
                    else:
                        status_text.error("Video generated but missing file reference.")
                else:
                    status_text.error("Operation completed but no video was returned.")
                
            except Exception as e:
                status_text.error(f"Video API Error: {e}")