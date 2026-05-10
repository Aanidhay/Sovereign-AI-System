import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
import requests
import warnings
import os
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Custom CSS for neon chat bubbles (less glowy, more readable)
st.markdown("""
<style>
.user-message {
    background: linear-gradient(135deg, #1e90ff, #0066cc);
    border: 1px solid #0099ff;
    border-radius: 18px;
    padding: 12px 18px;
    margin: 8px 0;
    box-shadow: 0 0 8px rgba(0, 153, 255, 0.3),
                inset 0 0 10px rgba(255, 255, 255, 0.1);
    color: white;
    font-weight: 500;
    margin-left: auto;
    max-width: 70%;
    float: right;
    clear: both;
}

.assistant-message {
    background: linear-gradient(135deg, #00cc66, #009944);
    border: 1px solid #00ff88;
    border-radius: 18px;
    padding: 12px 18px;
    margin: 8px 0;
    box-shadow: 0 0 8px rgba(0, 255, 136, 0.3),
                inset 0 0 10px rgba(255, 255, 255, 0.1);
    color: white;
    font-weight: 500;
    margin-right: auto;
    max-width: 70%;
    float: left;
    clear: both;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px 0;
}

.clearfix::after {
    content: "";
    clear: both;
    display: table;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    try:
        caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        
        device = "cpu"
        caption_model = caption_model.to(device)
        vqa_model = vqa_model.to(device)
        caption_model.eval()
        vqa_model.eval()
        
        return caption_processor, caption_model, vqa_processor, vqa_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None

def get_comprehensive_image_details(image, caption_processor, caption_model, vqa_processor, vqa_model):
    """Fetch ALL details from image using BLIP"""
    try:
        device = "cpu"
        
        # Get multiple detailed descriptions with different parameters
        descriptions = []
        
        # Primary detailed description
        inputs = caption_processor(image, return_tensors="pt").to(device)
        out = caption_model.generate(**inputs, max_length=100, num_beams=5, do_sample=True, temperature=0.8)
        primary_desc = caption_processor.decode(out[0], skip_special_tokens=True)
        descriptions.append(primary_desc)
        
        # Additional perspectives
        for temp in [0.6, 1.0]:
            out = caption_model.generate(**inputs, max_length=80, num_beams=3, do_sample=True, temperature=temp)
            desc = caption_processor.decode(out[0], skip_special_tokens=True)
            descriptions.append(desc)
        
        # Get answers to common questions for more context
        common_questions = [
            "What colors are in this image?",
            "How many objects are there?",
            "What is the main subject?",
            "What is the setting or location?",
            "What is the mood or atmosphere?"
        ]
        
        vqa_answers = {}
        for question in common_questions:
            try:
                inputs = vqa_processor(image, question, return_tensors="pt").to(device)
                out = vqa_model.generate(**inputs, max_length=30, num_beams=2, do_sample=True, temperature=0.5)
                answer = vqa_processor.decode(out[0], skip_special_tokens=True)
                vqa_answers[question] = answer
            except:
                vqa_answers[question] = "Unable to determine"
        
        # Combine all details
        comprehensive_details = {
            "primary_description": primary_desc,
            "additional_perspectives": descriptions[1:],
            "vqa_context": vqa_answers,
            "full_analysis": f"Primary: {primary_desc}. Additional views: {'; '.join(descriptions[1:])}. Context: {vqa_answers}"
        }
        
        return comprehensive_details
    except Exception as e:
        return {"error": str(e), "primary_description": "Error analyzing image"}

def get_llama_intelligent_response(image_details, user_query):
    """Send comprehensive image details to Llama 3.2 for intelligent response"""
    try:
        # Check if Llama 3.2 is available
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code != 200:
                return f"Based on the image: {image_details.get('primary_description', 'Unable to analyze image')}"
        except:
            return f"Based on the image: {image_details.get('primary_description', 'Unable to analyze image')}"
        
        # Create comprehensive prompt for Llama 3.2
        prompt = f"""You are an intelligent AI assistant. Analyze the comprehensive image details and provide a helpful response to the user's query.

COMPREHENSIVE IMAGE ANALYSIS:
Primary Description: {image_details.get('primary_description', 'N/A')}
Additional Perspectives: {'; '.join(image_details.get('additional_perspectives', []))}
Colors: {image_details.get('vqa_context', {}).get('What colors are in this image?', 'N/A')}
Objects: {image_details.get('vqa_context', {}).get('How many objects are there?', 'N/A')}
Main Subject: {image_details.get('vqa_context', {}).get('What is the main subject?', 'N/A')}
Setting: {image_details.get('vqa_context', {}).get('What is the setting or location?', 'N/A')}
Mood: {image_details.get('vqa_context', {}).get('What is the mood or atmosphere?', 'N/A')}

USER QUERY: {user_query}

Instructions:
- Use ALL the image details to provide an intelligent, context-aware response
- If user asks to create/analyze/generate something, DO IT based on the comprehensive image information
- Be specific and helpful
- Respond directly without mentioning you're an AI

Response:"""
        
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 400
            }
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            return f"Based on the image: {image_details.get('primary_description', 'Unable to analyze image')}"
            
    except Exception as e:
        return f"Based on the image: {image_details.get('primary_description', 'Unable to analyze image')}"

def main():
    st.set_page_config(page_title="AI Image Chat", page_icon="💬", layout="centered")
    st.title("💬 AI Image Chat")
    
    # Session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'image_details' not in st.session_state:
        st.session_state.image_details = None
    
    # Load models
    if 'models' not in st.session_state:
        with st.spinner("Loading AI models..."):
            models = load_models()
            if None in models:
                st.error("Failed to load models")
                return
            st.session_state.models = models
    
    caption_processor, caption_model, vqa_processor, vqa_model = st.session_state.models
    
    # Sidebar
    with st.sidebar:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
        if st.button("📁 New Image"):
            st.session_state.current_image = None
            st.session_state.image_details = None
            st.session_state.chat_history = []
            st.rerun()
    
    # Image upload
    if st.session_state.current_image is None:
        uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png', 'webp'])
        if uploaded_file:
            image = Image.open(uploaded_file).convert('RGB')
            st.session_state.current_image = image
            # Analyze image immediately to get all details
            with st.spinner("🔍 Analyzing image details..."):
                image_details = get_comprehensive_image_details(
                    image, caption_processor, caption_model, 
                    vqa_processor, vqa_model
                )
                st.session_state.image_details = image_details
            st.image(image, caption="Uploaded image", use_column_width=True)
            st.rerun()
    else:
        st.image(st.session_state.current_image, caption="Current image", use_column_width=True)
    
    # Chat display with neon bubbles
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message clearfix">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message clearfix">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input
    if st.session_state.current_image:
        query = st.chat_input("Ask about the image...")
        if query:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            # Get AI response using comprehensive details
            with st.spinner("🧠 Thinking..."):
                response = get_llama_intelligent_response(
                    st.session_state.image_details, 
                    query
                )
            
            # Add AI response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
