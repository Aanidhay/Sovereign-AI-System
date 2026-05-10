import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
import warnings
import requests
import json
warnings.filterwarnings("ignore")

@st.cache_resource
def load_models():
    """Load optimized BLIP models for faster loading"""
    try:
        # Use smaller, faster models for quick loading
        caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        
        # Force models to CPU to save GPU VRAM for Ollama
        device = "cpu"
        caption_model = caption_model.to(device)
        vqa_model = vqa_model.to(device)
        
        # Set to evaluation mode for faster inference
        caption_model.eval()
        vqa_model.eval()
        
        return caption_processor, caption_model, vqa_processor, vqa_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None

def get_detailed_description(image, caption_processor, caption_model):
    """Get comprehensive image analysis"""
    try:
        device = "cpu"
        
        # Get detailed caption with more parameters
        inputs = caption_processor(image, return_tensors="pt").to(device)
        out = caption_model.generate(**inputs, max_length=80, num_beams=5, do_sample=True, temperature=0.8)
        detailed_caption = caption_processor.decode(out[0], skip_special_tokens=True)
        
        # Get multiple perspectives by generating with different seeds
        descriptions = []
        for temp in [0.6, 0.8, 1.0]:
            out = caption_model.generate(**inputs, max_length=60, num_beams=3, do_sample=True, temperature=temp)
            desc = caption_processor.decode(out[0], skip_special_tokens=True)
            descriptions.append(desc)
        
        # Combine all descriptions for comprehensive analysis
        combined_analysis = f"Primary description: {detailed_caption}. Additional perspectives: {'; '.join(descriptions[1:])}"
        
        return detailed_caption, combined_analysis
    except Exception as e:
        return f"Error generating description: {str(e)}", ""

def get_llama_response(image_description, user_query, vqa_answer=None):
    """Send image analysis to Llama 3.2 for intelligent response"""
    try:
        # Check if Ollama is running and Llama 3.2 is available
        try:
            response = requests.get("http://localhost:11434/api/tags")
            models = response.json().get('models', [])
            llama_available = any('llama3.2' in model.get('name', '').lower() for model in models)
        except:
            llama_available = False
        
        if not llama_available:
            return """🤖 **Llama 3.2 Integration Setup Required:**

To enable truly intelligent responses, please:

1. **Install Ollama:** 
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Download Llama 3.2:**
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama:**
   ```bash
   ollama serve
   ```

Once set up, BLIP will analyze images and send the data to Llama 3.2 for sophisticated, context-aware responses.

**Current Image Analysis:** {image_description}
**Your Question:** {user_query}
**VQA Result:** {vqa_answer if vqa_answer else "N/A"}"""
        
        # Create the prompt for Llama 3.2
        prompt = f"""You are an intelligent AI assistant. Analyze the user's request and the image information to provide a helpful, relevant response.

IMAGE ANALYSIS: {image_description}
SPECIFIC DETAILS: {vqa_answer if vqa_answer else "No specific details"}
USER REQUEST: {user_query}

Instructions:
- Understand what the user actually wants from this image
- If they ask to create/analyze/generate something, DO IT based on the image content
- If they ask a question, ANSWER it using the image information
- Be practical and helpful - think about what would be most useful for the user
- Adapt your response to ANY type of image or question
- If the request doesn't make sense for this image, suggest alternatives

Respond directly and helpfully."""

        # Send to Llama 3.2 via Ollama
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 400
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'No response received')
        else:
            return f"❌ Error communicating with Llama 3.2: {response.status_code}"
            
    except Exception as e:
        return f"""❌ **Llama 3.2 Integration Error:**

Please ensure Ollama is running with Llama 3.2 installed.

**Setup Instructions:**
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull llama3.2`
3. Start: `ollama serve`

**Technical Error:** {str(e)}

**Fallback Analysis:** {image_description}"""

def analyze_image_with_ai(image, query, caption_processor, caption_model, vqa_processor, vqa_model):
    """Pipeline: BLIP analyzes image → sends to Llama 3.2 for intelligent response"""
    try:
        device = "cpu"
        
        # Step 1: Get detailed image analysis from BLIP
        basic_caption, _ = get_detailed_description(image, caption_processor, caption_model)
        
        # Step 2: Get specific VQA answer if it's a specific question
        vqa_answer = None
        query_lower = query.strip().lower()
        
        # Check if it's a specific question (not general description)
        if not any(word in query_lower for word in [
            "what do you see", "describe this image", "what is in this image", 
            "describe", "what", "tell me about", "explain", "analyze", "overview",
            "summary", "what's happening", "scene", "setting"
        ]):
            # Get specific VQA answer
            inputs = vqa_processor(image, query, return_tensors="pt").to(device)
            out = vqa_model.generate(**inputs, max_length=50, num_beams=3, do_sample=True, temperature=0.7)
            vqa_answer = vqa_processor.decode(out[0], skip_special_tokens=True)
        
        # Step 3: Send to Llama 3.2 for intelligent response
        return get_llama_response(basic_caption, query, vqa_answer)
            
    except Exception as e:
        return f"❌ **Pipeline Error:** {str(e)}"

def main():
    st.set_page_config(
        page_title="AI Image Chat",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    st.title("💬 AI Image Chat")
    st.markdown("Upload an image and have a continuous conversation about it!")
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'image_description' not in st.session_state:
        st.session_state.image_description = ""
    
    # Load models
    if 'models_loaded' not in st.session_state:
        with st.spinner("⚡ Loading optimized AI models... Under 1 minute!"):
            caption_processor, caption_model, vqa_processor, vqa_model = load_models()
            if None in (caption_processor, caption_model, vqa_processor, vqa_model):
                st.error("❌ Failed to load AI models. Please try again.")
                return
            st.session_state.caption_processor = caption_processor
            st.session_state.caption_model = caption_model
            st.session_state.vqa_processor = vqa_processor
            st.session_state.vqa_model = vqa_model
            st.session_state.models_loaded = True
    else:
        caption_processor = st.session_state.caption_processor
        caption_model = st.session_state.caption_model
        vqa_processor = st.session_state.vqa_processor
        vqa_model = st.session_state.vqa_model
    
    # Sidebar with example questions and controls
    with st.sidebar:
        st.header("🎯 Chat Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # New image button
        if st.button("📁 Upload New Image"):
            st.session_state.current_image = None
            st.session_state.image_description = ""
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.header("💬 Example Questions")
        st.markdown("**General Analysis:**")
        st.write("• What do you see in detail?")
        st.write("• Describe the entire scene")
        st.write("• What's happening here?")
        
        st.markdown("**Creative Tasks:**")
        st.write("• Create a schedule from this")
        st.write("• Write a story about this")
        st.write("• Make a plan based on this")
        
        st.markdown("**Specific Questions:**")
        st.write("• What colors are dominant?")
        st.write("• How many people are there?")
        st.write("• What are they doing?")
        st.write("• What's the weather like?")
        
        st.markdown("**Complex Analysis:**")
        st.write("• Analyze the composition")
        st.write("• What's the story behind this?")
        st.write("• Describe the mood and atmosphere")
    
    # File uploader (only show if no image is loaded)
    if st.session_state.current_image is None:
        uploaded_file = st.file_uploader(
            "📁 Choose an image to start chatting...",
            type=['jpg', 'jpeg', 'png', 'webp', 'gif'],
            help="Upload any image format for AI analysis"
        )
        
        if uploaded_file is not None:
            # Process and store image
            image = Image.open(uploaded_file).convert('RGB')
            st.session_state.current_image = image
            
            # Get initial description
            with st.spinner("🧠 Analyzing image..."):
                basic_desc, _ = get_detailed_description(image, caption_processor, caption_model)
                st.session_state.image_description = basic_desc
            
            st.rerun()
    
    else:
        # Display current image
        st.image(st.session_state.current_image, caption="📸 Current Image", use_container_width=True)
        
        # Show image description
        if st.session_state.image_description:
            st.info(f"📝 **Image Context:** {st.session_state.image_description}")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    st.markdown(f"**👤 You:** {message['content']}")
                else:
                    st.markdown(f"**🤖 AI:** {message['content']}")
                st.markdown("---")
        
        # Chat input
        st.subheader("💬 Ask about this image:")
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎯 General Analysis"):
                st.session_state.quick_query = "What do you see in this image? Describe everything in detail."
        
        with col2:
            if st.button("📅 Create Schedule"):
                st.session_state.quick_query = "Can you create a schedule or plan based on what you see in this image?"
        
        with col3:
            if st.button("✍️ Write Story"):
                st.session_state.quick_query = "Write a creative story or poem based on this image."
        
        with col4:
            if st.button("🎨 Colors & Style"):
                st.session_state.quick_query = "What colors are dominant? Describe the visual style and composition."
        
        # Use quick query if set
        if 'quick_query' in st.session_state:
            query = st.session_state.quick_query
            st.session_state.quick_query = None
        else:
            query = st.text_input(
                "Type your question:",
                placeholder="e.g., What do you see in detail? Create a schedule from this image.",
                key="chat_input"
            )
        
        # Send button
        if st.button("💬 Send", type="primary") or (query and 'send_pressed' in st.session_state):
            if query.strip():
                # Add user message to chat
                st.session_state.chat_history.append({"role": "user", "content": query})
                
                # Get AI response
                with st.spinner("🧠 AI is thinking..."):
                    response = analyze_image_with_ai(
                        st.session_state.current_image, query, caption_processor, caption_model, 
                        vqa_processor, vqa_model
                    )
                
                # Add AI response to chat
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Clear send flag and rerun
                if 'send_pressed' in st.session_state:
                    del st.session_state.send_pressed
                st.rerun()
            else:
                st.warning("⚠️ Please enter a question about the image.")
    
    # Instructions for new users
    if st.session_state.current_image is None:
        st.info("📁 Please upload an image to start chatting with the AI!")
        
        st.subheader("🚀 How to use:")
        st.markdown("""
        1. **Upload an image** - Click the button above to select any image
        2. **Start chatting** - Ask questions continuously without re-uploading
        3. **Get intelligent responses** - The AI remembers the image and context
        4. **Create schedules, stories, plans** - Ask the AI to generate content based on images
        
        **💡 Advanced Capabilities:**
        - 📅 **Schedule Creation**: "Create a schedule from this image"
        - ✍️ **Creative Writing**: "Write a story about this scene"
        - 🎨 **Visual Analysis**: Colors, composition, style, mood
        - 👥 **People Detection**: Counting, actions, emotions
        - 🌍 **Scene Understanding**: Location, weather, time
        - 📝 **Text Recognition**: Reading signs and labels
        - 🧠 **Continuous Chat**: Keep asking questions about the same image
        """)

if __name__ == "__main__":
    main()
