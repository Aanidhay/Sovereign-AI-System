import streamlit as st
import base64
import time
from PIL import Image
import io
import torch
from diffusers import StableDiffusionPipeline
import warnings
warnings.filterwarnings("ignore")

# Set page config
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🖼️",
    layout="centered"
)

@st.cache_resource
def load_pipeline():
    # Check for GPU
    if torch.cuda.is_available():
        # Initialize the diffusion pipeline for GPU
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", 
            torch_dtype=torch.float16
        )
        pipe = pipe.to("cuda")
        return pipe
    else:
        # Return None to indicate we should use the Cloud API instead of crashing the CPU
        return None

# Custom CSS for the image generator page
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    .main-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
    }
    
    h1, h2, h3, h4, h5, h6, .stMarkdown p {
        color: #f0f2f6 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: rgba(20, 20, 30, 0.9) !important;
        color: #fff !important;
        border: 2px solid rgba(255, 214, 10, 0.5) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #ffd60a !important;
        box-shadow: 0 0 20px rgba(255, 214, 10, 0.6) !important;
    }
    
    .stButton > button {
        background: radial-gradient(circle at 25% 25%, #fff7a8, #ffd60a 60%) !important;
        color: #0b0b0b !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px #ffd60a, 0 0 30px #ffea70 !important;
        width: 100% !important;
        margin: 20px 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px #ffd60a, 0 0 40px #ffea70 !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .loading-container {
        text-align: center;
        padding: 40px;
        background: rgba(30, 30, 40, 0.8);
        border-radius: 20px;
        border: 2px solid rgba(255, 214, 10, 0.3);
        margin: 20px 0;
    }
    
    .generated-image {
        text-align: center;
        padding: 20px;
        background: rgba(30, 30, 40, 0.8);
        border-radius: 20px;
        border: 2px solid rgba(255, 214, 10, 0.3);
        margin: 20px 0;
    }
    
    .back-button {
        background: rgba(30, 30, 40, 0.8) !important;
        color: #f0f2f6 !important;
        border: 2px solid rgba(0, 200, 255, 0.5) !important;
    }
    
    .back-button:hover {
        border-color: #00c8ff !important;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.title("🖼️ AI Image Generator")
st.markdown("### Describe what you want to create:")

# Back to main menu button
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Back to Menu", key="back_button"):
        st.markdown("""
        <script>
        window.close();
        window.open('app.py', '_self');
        </script>
        """, unsafe_allow_html=True)

# Text input for image prompt
prompt = st.text_area(
    "Enter your image description:",
    value=st.session_state.prompt,
    placeholder="Example: A majestic lion sitting on a rock at sunset, photorealistic, highly detailed...",
    height=120,
    key="image_prompt"
)

# Generation parameters
col1, col2 = st.columns(2)
with col1:
    width = st.slider("Image Width", 256, 1024, 512)
with col2:
    height = st.slider("Image Height", 256, 1024, 512)

num_inference_steps = st.slider("Quality Steps", 10, 50, 20)
guidance_scale = st.slider("Creativity Scale", 1.0, 20.0, 7.5)

# Generate button
generate_button = st.button("🎨 Generate Image", type="primary")

if generate_button and prompt.strip():
    st.session_state.generating = True
    st.session_state.prompt = prompt
    st.rerun()

# Show loading state
if st.session_state.generating and not st.session_state.generated_image:
    st.markdown("""
    <div class="loading-container">
        <h2>🎨 CREATING</h2>
        <p>Your image is being generated...</p>
        <div style="width: 100%; background-color: rgba(255, 214, 10, 0.2); border-radius: 10px; overflow: hidden;">
            <div style="width: 0%; height: 30px; background: linear-gradient(90deg, #ffd60a, #ffea70); border-radius: 10px; animation: loading 2s ease-in-out infinite;">
            </div>
        </div>
        <style>
        @keyframes loading {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate image generation (replace with actual LLM call)
    time.sleep(2)
    
    try:
        pipe = load_pipeline()
        
        if pipe is not None:
            # Generate the image locally using NVIDIA GPU
            with torch.no_grad():
                result = pipe(
                    prompt=st.session_state.prompt,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                )
            st.session_state.generated_image = result.images[0]
        else:
            # No GPU available. Use free Cloud AI API to prevent CPU memory crash
            import requests
            import urllib.parse
            
            encoded_prompt = urllib.parse.quote(st.session_state.prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            response = requests.get(url)
            if response.status_code == 200:
                st.session_state.generated_image = Image.open(io.BytesIO(response.content))
            else:
                raise Exception("Cloud API failed to generate image.")
                
        st.session_state.generating = False
        st.rerun()
        
    except Exception as e:
        st.session_state.generating = False
        st.error(f"Error generating image: {str(e)}")
        st.rerun()

# Display generated image
if st.session_state.generated_image:
    st.markdown("""
    <div class="generated-image">
        <h3>✨ Your Generated Image</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the image
    st.image(st.session_state.generated_image, use_container_width=True)
    
    # Download button
    img_buffer = io.BytesIO()
    st.session_state.generated_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Image",
            data=img_buffer,
            file_name="generated_image.png",
            mime="image/png"
        )
    
    # Generate new image button
    if st.button("🔄 Generate New Image"):
        st.session_state.generated_image = None
        st.session_state.generating = False
        st.rerun()

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
