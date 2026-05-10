# 🚀 Llama 3.2 Setup Instructions

## Step 1: Install Ollama

**For Windows:**
1. Download Ollama from https://ollama.ai/
2. Run the installer
3. Open Command Prompt/PowerShell and verify installation:
```bash
ollama --version
```

## Step 2: Download Llama 3.2 Model

1. Start Ollama service:
```bash
ollama serve
```

2. In a NEW terminal, download Llama 3.2:
```bash
ollama pull llama3.2
```

## Step 3: Run the Chatbot

1. Make sure Ollama is running:
```bash
ollama serve
```

2. In your CHATBOT folder, run:
```bash
streamlit run app.py
```

## Alternative: Use Hugging Face API

If you prefer not to use Ollama, replace the `get_llama_response` function with:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def get_llama_response(prompt):
    try:
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=500)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return response[len(prompt):].strip()  # Remove the original prompt
    except Exception as e:
        return f"Error: {str(e)}"
```

## Troubleshooting

**Error: "Cannot connect to Ollama"**
- Make sure Ollama is running with `ollama serve`
- Check that port 11434 is not blocked
- Try restarting Ollama

**Slow responses**
- Llama 3.2 runs locally, responses depend on your computer's hardware
- Consider using a smaller model: `ollama pull llama3.2:8b`

**Model not found**
- Run: `ollama pull llama3.2`
- Or try: `ollama pull llama3.2:8b` for smaller version
