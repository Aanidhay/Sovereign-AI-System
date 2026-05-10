import streamlit as st
import time
import requests
import json

st.set_page_config(
    page_title="Llama 3.2 Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Llama 3.2 Chatbot")

st.markdown("""
<style>
.user-message {
    background: linear-gradient(135deg, #0066ff 0%, #00ccff 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 20px;
    margin: 10px 0;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0 4px 15px rgba(0, 102, 255, 0.6);
    animation: glow 2s ease-in-out infinite alternate;
}

.bot-message {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 20px;
    margin: 10px 0;
    max-width: 80%;
    box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.6);
    }
    to {
        box-shadow: 0 4px 25px rgba(0, 102, 255, 0.9);
    }
}

.loading-message {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 20px;
    margin: 10px 0;
    max-width: 80%;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0% {
        opacity: 0.7;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.02);
    }
    100% {
        opacity: 0.7;
        transform: scale(1);
    }
}

.chat-container {
    height: 70vh;
    overflow-y: auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    border-radius: 15px;
    margin-bottom: 20px;
}

.stTextInput > div > div > input {
    background: white;
    border: 2px solid #667eea;
    border-radius: 25px;
    padding: 12px 20px;
    font-size: 16px;
}

.stTextInput > div > div > input:focus {
    border-color: #764ba2;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_llama_response(prompt):
    try:
        # Using Ollama API for Llama 3.2 (make sure Ollama is running locally)
        # You need to install Ollama first: https://ollama.ai/
        # Then run: ollama pull llama3.2
        
        response = requests.post(
            'http://127.0.0.1:11434/api/generate',
            json={
                'model': 'llama3.2:1b',
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Ollama Error (Status {response.status_code}): {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Please make sure Ollama is installed and running with 'ollama serve'. Install from https://ollama.ai/"
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown('<div class="chat-container" style="height: 70vh; overflow-y: auto; padding: 20px; background: #0e1117; border-radius: 15px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

# Display all messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🤖 Bot: {message["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message immediately
    st.markdown(f'<div class="user-message">👤 You: {user_input}</div>', unsafe_allow_html=True)
    
    # Show loading message
    loading_placeholder = st.empty()
    loading_placeholder.markdown('<div class="loading-message">🤖 ANSWERING TO THE QUERY...</div>', unsafe_allow_html=True)
    
    # Get response
    response = get_llama_response(user_input)
    
    # Remove loading message and show response
    loading_placeholder.empty()
    st.markdown(f'<div class="bot-message">🤖 Bot: {response}</div>', unsafe_allow_html=True)
    
    # Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the interface
    st.rerun()

