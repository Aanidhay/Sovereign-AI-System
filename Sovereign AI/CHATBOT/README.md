# 🤖 Llama 3.2 Chatbot

A beautiful Streamlit-based chatbot application with Llama 3.2 integration.

## Features

- ✨ **Glowing UI**: Blue bubbles for user messages, green bubbles for bot responses
- 🔄 **Loading Indicator**: Shows "ANSWERING TO THE QUERY" while processing
- 📱 **Responsive Design**: Works on all screen sizes
- 💬 **Chat Interface**: Text input field positioned at the bottom
- 🎨 **Modern Styling**: Gradient backgrounds and smooth animations

## Installation

1. Navigate to the CHATBOT folder:
```bash
cd CHATBOT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the chatbot with:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. Type your message in the text field at the bottom
2. Press Enter to send your message
3. Your message appears in a glowing blue bubble
4. Wait for "ANSWERING TO THE QUERY" while the bot processes
5. The bot's response appears in a glowing green bubble

## Customization

### Adding Real Llama 3.2 Integration

To connect to a real Llama 3.2 model, replace the `get_llama_response()` function in `app.py` with your preferred API:

**Option 1: Hugging Face API**
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
```

**Option 2: Ollama Local**
```python
import requests

def get_llama_response(prompt):
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama3.2',
        'prompt': prompt,
        'stream': False
    })
    return response.json()['response']
```

**Option 3: OpenAI-Compatible API**
```python
import openai

openai.api_base = "your-llama3.2-api-endpoint"
def get_llama_response(prompt):
    response = openai.ChatCompletion.create(
        model="llama-3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## File Structure

```
CHATBOT/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- `streamlit`: Web framework for the chat interface
- `requests`: For API calls (when using real Llama 3.2)

## Notes

- The current implementation uses mock responses for demonstration
- To use real Llama 3.2, you'll need API keys or local model deployment
- The UI is fully responsive and includes smooth animations
