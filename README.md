<<<<<<< HEAD
# 🚀 Pro Local AI Chatbot (Ollama + Streamlit)

A professional, modern, and privacy-focused AI chat interface that runs entirely on your local machine. No data leaks, no subscription fees, just pure AI power.

## ✨ Features

-   **Professional UI:** Sleek night-mode interface with gradient backgrounds and smooth animations.
-   **Real-time Streaming:** AI responses appear word-by-word with a typing effect for a better user experience.
-   **Complete History Control:**
    -   **Timestamps:** Every message is logged with its exact time.
    -   **Persistence:** Chat history is maintained using `st.session_state`.
    -   **Download:** Export your entire conversation as a `.txt` file.
    -   **Reset:** Clear chat history with a single click.
-   **Smart Inputs:** Prevents empty submissions and supports "Enter" to send.
-   **Utility Tools:** 
    -   "Copy" feature to quickly grab AI responses.
    -   Status dashboard showing active model (`llama3`).
    -   Automatic loading spinners during processing.
-   **Error Resilient:** Built-in checks for Ollama service availability and API stability.

---

## 🛠️ Installation & Setup

### 1. Install Ollama
Download and install the appropriate version for your OS from **[ollama.com](https://ollama.com)**.

### 2. Pull the AI Model
Open your terminal and pull the `llama3` model:
```bash
ollama pull llama3
```

### 3. Install Python Dependencies
Ensure you have Python installed, then run:
```bash
pip install streamlit requests
```

### 4. Launch the App
Clone this project or navigate to the directory and run:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

- `app.py`: The core application file (frontend + backend connection).
- `README.md`: This documentation file.

---

## ⚙️ How it Works
1. **Frontend:** Built with Streamlit, using custom CSS for the premium aesthetic.
2. **Backend:** Connects to the Ollama REST API at `http://localhost:11434`.
3. **Response:** Uses the `/api/generate` endpoint with `stream: true` to feed text chunks to the UI in real-time.

---

## 🔒 Privacy & Security
This app is **100% private**. 
- It does **not** send data to OpenAI, Google, or any other cloud provider.
- Everything runs on your local CPU/GPU via Ollama.
- Chat history is stored only in your browser's current session memory.
=======
# streamlit-llm-interface
Interactive Streamlit interface for a locally installed LLM using Ollama, allowing users to ask questions and receive AI-generated responses.
>>>>>>> 95c35bceef9b4e6b874685abd25d588f69df87b6
