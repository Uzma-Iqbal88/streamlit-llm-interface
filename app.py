import streamlit as st
import requests
import json
import time
from datetime import datetime

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# --- Page Setup ---
st.set_page_config(
    page_title="Pro Local AI Chat",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Modern & Professional) ---
def apply_custom_css():
    st.markdown("""
        <style>
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        
        /* Chat Bubble Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .chat-bubble {
            animation: fadeIn 0.3s ease-out forwards;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Header Styling */
        .main-header {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .timestamp {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 5px;
            display: block;
        }

        /* Button Styling */
        div.stButton > button {
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# CORE LOGIC FUNCTIONS
# ==========================================

def get_installed_models():
    """Fetches the list of currently pulled models from Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        return []
    except:
        return []

def get_ai_response(prompt, model, messages_history):
    """
    Calls Ollama API with streaming enabled for a "typing" effect.
    """
    payload = {
        "model": model, # Use the selected model
        "prompt": prompt,
        "stream": True # Enable streaming for a better UI experience
    }
    
    full_response = ""
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=90)
        response.raise_for_status()
        
        # Create a placeholder for the streaming text
        message_placeholder = st.empty()
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                full_response += chunk.get("response", "")
                # Update the placeholder with the current accumulated response
                message_placeholder.markdown(full_response + "▌")
        
        # Final update without the cursor
        message_placeholder.markdown(full_response)
        return full_response

    except requests.exceptions.ConnectionError:
        st.error("❌ **Ollama is not running.** Please start Ollama (`ollama serve`) and try again.")
        return None
    except Exception as e:
        st.error(f"⚠️ **API Error:** {str(e)}")
        return None

def download_history():
    """Formats chat history for download."""
    history_text = "--- Chat History ---\n\n"
    for msg in st.session_state.messages:
        role = "USER" if msg["role"] == "user" else "AI"
        history_text += f"[{msg['time']}] {role}:\n{msg['content']}\n\n"
    return history_text

# ==========================================
# UI RENDERING
# ==========================================

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='color: #38bdf8;'>⚙️ Dashboard</h2>", unsafe_allow_html=True)
        
        # Dynamically fetch models
        available_models = get_installed_models()
        
        if available_models:
            # Set default model index
            default_index = 0
            if "llama2:latest" in available_models:
                default_index = available_models.index("llama2:latest")
            
            # Model selection
            st.session_state.selected_model = st.selectbox(
                "Select Model:",
                available_models,
                index=default_index
            )
            st.success(f"Model `{st.session_state.selected_model}` is ready!")
        else:
            st.error("No models found in Ollama. Pull one first (e.g., `ollama pull llama2`).")
            st.session_state.selected_model = "llama3" # Fallback
            
        st.write("---")
        
        st.markdown("**About this App:**")
        st.info("A professional-grade local AI chat interface powered by Ollama. Your data never leaves this machine.")
        
        if st.button("🗑️ Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        if st.session_state.messages:
            st.download_button(
                label="📥 Download Chat Log",
                data=download_history(),
                file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        st.markdown("---")
        st.markdown("<small>Built with ❤️ using Streamlit & Ollama</small>", unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama3" # Default fallback
    
    # Render Sidebar
    render_sidebar()
    
    # Header
    st.markdown("<div class='main-header'>⚡ Local AI Pro</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Ultra-fast, private, and secure AI workspace.</p>", unsafe_allow_html=True)
    st.divider()

    # Display Chat History
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='chat-bubble'>{message['content']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='timestamp'>{message['time']}</span>", unsafe_allow_html=True)
            
            # Add a copy button for AI messages
            if message["role"] == "assistant":
                if st.button(f"📋 Copy", key=f"copy_{i}"):
                    # In a real app we'd use JS, but here we can just show it in code block for easy grabbing
                    st.code(message["content"], language=None)

    # Welcome message for empty state
    if not st.session_state.messages:
        st.markdown(f"""
            <div style='text-align: center; padding: 50px;'>
                <h3>👋 Ready to chat with {st.session_state.selected_model}!</h3>
                <p>Try asking about code, writing, or just have a chat.</p>
            </div>
        """, unsafe_allow_html=True)

    # Chat Input (Auto-scrolled and Enter supported)
    if prompt := st.chat_input("Enter your command..."):
        
        # 1. Validation (Prevent empty input)
        if not prompt.strip():
            st.warning("Please enter some text before sending.")
        else:
            # 2. Add user message with timestamp
            current_time = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt, 
                "time": current_time
            })
            
            # Handle Rerender to show user message
            st.rerun()

    # If the last message was from user, trigger AI response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        user_msg = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant"):
            with st.spinner("⚡ Processing Request..."):
                ai_reply = get_ai_response(user_msg, st.session_state.selected_model, st.session_state.messages)
                
                if ai_reply:
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_reply, 
                        "time": datetime.now().strftime("%I:%M %p")
                    })
                    st.rerun()

if __name__ == "__main__":
    main()
