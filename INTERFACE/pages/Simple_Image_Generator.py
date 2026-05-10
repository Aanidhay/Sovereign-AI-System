import streamlit as st
import time
import io
import torch
from diffusers import StableDiffusionPipeline
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🖼️",
    layout="centered"
)

# Custom CSS
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
    </style>
""", unsafe_allow_html=True)

# Session state
for key, default in {
    "generating": False,
    "generated_image": None,
    "prompt": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🖼️ AI Image Generator")
st.markdown("### Describe what you want to create:")

# Back button
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Back to Menu", key="back_button"):
        st.switch_page("app.py")

# Prompt input
prompt = st.text_area(
    "Enter your image description:",
    value=st.session_state.prompt,
    placeholder="Example: A majestic lion sitting on a rock at sunset, photorealistic, highly detailed...",
    height=120,
    key="image_prompt",
)

# Parameters
c1, c2 = st.columns(2)
with c1:
    width = st.slider("Image Width", 256, 1024, 512)
with c2:
    height = st.slider("Image Height", 256, 1024, 512)

num_inference_steps = st.slider("Quality Steps", 10, 50, 20)
guidance_scale = st.slider("Creativity Scale", 1.0, 20.0, 7.5)

# Generate button
if st.button("🎨 Generate Image", type="primary") and prompt.strip():
    st.session_state.generating = True
    st.session_state.prompt = prompt
    st.rerun()

# Loading state
if st.session_state.generating and st.session_state.generated_image is None:
    st.markdown("""
    <div class="loading-container">
        <h2>🎨 CREATING</h2>
        <p>Your image is being generated...</p>
        <div style="width: 100%; background-color: rgba(255, 214, 10, 0.2); border-radius: 10px; overflow: hidden;">
            <div style="width: 0%; height: 30px; background: linear-gradient(90deg, #ffd60a, #ffea70); border-radius: 10px; animation: loading 2s ease-in-out infinite;"></div>
        </div>
        <style>
        @keyframes loading { 0% { width: 0%; } 50% { width: 70%; } 100% { width: 100%; } }
        </style>
    </div>
    """, unsafe_allow_html=True)

    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32,
            safety_checker=None,
        ).to("cpu")

        with torch.no_grad():
            result = pipe(
                prompt=st.session_state.prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            )

        st.session_state.generated_image = result.images[0]
        st.session_state.generating = False
        st.rerun()
    except Exception as e:
        st.session_state.generating = False
        st.error(f"Error generating image: {e}")
        st.rerun()

# Show result
if st.session_state.generated_image:
    st.markdown("""
    <div class="generated-image">
        <h3>✨ Your Generated Image</h3>
    </div>
    """, unsafe_allow_html=True)
    st.image(st.session_state.generated_image, use_column_width=True)

    img_buf = io.BytesIO()
    st.session_state.generated_image.save(img_buf, format="PNG")
    img_buf.seek(0)

    st.download_button(
        label="📥 Download Image",
        data=img_buf,
        file_name="generated_image.png",
        mime="image/png",
    )

    if st.button("🔄 Generate New Image"):
        st.session_state.generated_image = None
        st.session_state.generating = False
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
