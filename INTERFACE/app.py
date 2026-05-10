import streamlit as st
import base64
import webbrowser
from streamlit.components.v1 import html

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set page config with dark theme
st.set_page_config(
    page_title="AI Services Dashboard",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS with direct style injection
st.markdown("""
    <style>
    /* Hide Streamlit sidebar and header controls */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="collapsedControl"], header [data-testid="baseButton-header"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem;
    }
    /* Force dark theme */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Button styling with neon bubble effect */
    .stButton>button {
        width: 100% !important;
height: 80px !important;
        border: none !important;
        border-radius: 50px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 20px 0 !important;
        cursor: pointer !important;
        transition: all 0.4s ease !important;
        position: relative !important;
        overflow: visible !important;
        z-index: 1 !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
        transform-style: preserve-3d;
        perspective: 1000px;
        box-shadow: 0 0 15px currentColor, 
                   0 0 30px currentColor, 
                   0 0 45px currentColor !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: inherit;
        border-radius: 50px;
        z-index: -1;
        opacity: 0.7;
        filter: blur(15px);
        transition: all 0.4s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 0 20px currentColor, 
                   0 0 40px currentColor, 
                   0 0 60px currentColor !important;
    }
    
    .stButton>button:active {
        transform: translateY(2px) scale(0.98) !important;
        box-shadow: 0 0 10px currentColor !important;
    }
    
    /* Individual button styles */
    #img_gen {
        background: radial-gradient(circle at 25% 25%, #fff7a8, #ffd60a 60%) !important;
        box-shadow: 0 0 18px #ffd60a, 0 0 38px #ffea70, 0 0 60px rgba(255,214,10,0.65) !important;
        color: #0b0b0b !important;
    }
    
    #img_analysis {
        background: radial-gradient(circle at 25% 25%, #c8ffcf, #00ff88 60%) !important;
        box-shadow: 0 0 18px #00ff88, 0 0 38px #7dffb5, 0 0 60px rgba(0,255,136,0.6) !important;
        color: #0b0b0b !important;
    }
    
    #tourism {
        background: radial-gradient(circle at 25% 25%, #c4e6ff, #2196f3 60%) !important;
        box-shadow: 0 0 18px #2196f3, 0 0 38px #74c8ff, 0 0 60px rgba(33,150,243,0.6) !important;
        color: #0b0b0b !important;
    }
    
    #debate {
        background: radial-gradient(circle at 25% 25%, #ffc7cf, #ff1744 60%) !important;
        box-shadow: 0 0 18px #ff1744, 0 0 38px #ff6f8d, 0 0 60px rgba(255,23,68,0.6) !important;
        color: #fff !important;
    }
    
    #chatbot {
        background: radial-gradient(circle at 25% 25%, #ffd1ff, #ff4de1 60%) !important;
        box-shadow: 0 0 18px #ff4de1, 0 0 38px #ff8cf0, 0 0 60px rgba(255,77,225,0.65) !important;
        color: #fff !important;
    }
    
    /* Hover effects */
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        filter: brightness(1.1) !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px) scale(0.99) !important;
    }
    
    /* Container styling */
    .main-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6, .stMarkdown p {
        color: #f0f2f6 !important;
    }
    
    /* Parameter bubbles */
    .stSlider, .stSelectbox, .stTextInput, .stNumberInput {
        margin: 15px 0 !important;
    }
    
    .stSlider .stSlider, .stSelectbox .stSelectbox, 
    .stTextInput .stTextInput, .stNumberInput .stNumberInput {
        background: rgba(30, 30, 40, 0.8) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 0 10px rgba(0, 150, 255, 0.5) !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
    }
    
    .stSlider .stSlider:hover, .stSelectbox .stSelectbox:hover,
    .stTextInput .stTextInput:hover, .stNumberInput .stNumberInput:hover {
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.8) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSlider .stSlider:focus-within, .stSelectbox .stSelectbox:focus-within,
    .stTextInput .stTextInput:focus-within, .stNumberInput .stNumberInput:focus-within {
        box-shadow: 0 0 20px rgba(0, 200, 255, 1) !important;
        border: 1px solid rgba(0, 200, 255, 0.8) !important;
    }
    
    /* Slider specific styles */
    .stSlider .stSlider .stSlider-thumb {
        background: #00c8ff !important;
        border: 2px solid #fff !important;
        box-shadow: 0 0 10px #00c8ff, 0 0 20px #00c8ff !important;
    }
    
    /* Selectbox dropdown */
    .stSelectbox select {
        background-color: rgba(20, 20, 30, 0.9) !important;
        color: #fff !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(20, 20, 30, 0.9) !important;
        color: #fff !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #00c8ff !important;
        box-shadow: 0 0 10px rgba(0, 200, 255, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title and description
st.title("🤖 AI Services Dashboard")
st.markdown("### Choose a service to get started:")


# Add JavaScript to handle button clicks
st.markdown("""
<script>
function handleButtonClick(buttonId) {
    // Update the session state using Streamlit's setComponentValue
    const data = {buttonId: buttonId};
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        data: data
    }, '*');
    
    // Show which button was clicked
    const buttons = document.querySelectorAll('.neon-button');
    buttons.forEach(btn => {
        btn.style.transform = 'translateY(0) scale(1)';
        btn.style.boxShadow = '0 0 15px ' + btn.getAttribute('data-glow').split(',')[0];
    });
    
    const clickedBtn = document.getElementById(buttonId);
    if (clickedBtn) {
        clickedBtn.style.transform = 'translateY(2px) scale(0.98)';
        clickedBtn.style.boxShadow = '0 0 25px ' + clickedBtn.getAttribute('data-glow').split(',')[0];
    }
}
</script>
""", unsafe_allow_html=True)

# Button styles and data
button_data = [
    {
        'id': 'img_gen',
        'text': '🖼️ Image Generation',
        'help': 'Generate images using AI',
        'gradient': 'radial-gradient(circle at 25% 25%, #fff7a8, #ffd60a 60%)',
        'glow': '0 0 18px #ffd60a, 0 0 38px #ffea70, 0 0 60px rgba(255,214,10,0.65)',
        'color': '#0b0b0b'
    },
    {
        'id': 'img_analysis',
        'text': '🔍 Image Analysis',
        'help': 'Analyze images using AI',
        'gradient': 'radial-gradient(circle at 25% 25%, #c8ffcf, #00ff88 60%)',
        'glow': '0 0 18px #00ff88, 0 0 38px #7dffb5, 0 0 60px rgba(0,255,136,0.6)',
        'color': '#0b0b0b'
    },
    {
        'id': 'tourism',
        'text': '🌍 Tourism Guide',
        'help': 'Get travel recommendations',
        'gradient': 'radial-gradient(circle at 25% 25%, #c4e6ff, #2196f3 60%)',
        'glow': '0 0 18px #2196f3, 0 0 38px #74c8ff, 0 0 60px rgba(33,150,243,0.6)',
        'color': '#0b0b0b'
    },
    {
        'id': 'debate',
        'text': '💬 Debating AI',
        'help': 'Engage in a debate with AI',
        'gradient': 'radial-gradient(circle at 25% 25%, #ffc7cf, #ff1744 60%)',
        'glow': '0 0 18px #ff1744, 0 0 38px #ff6f8d, 0 0 60px rgba(255,23,68,0.6)',
        'color': '#ffffff'
    },
    {
        'id': 'chatbot',
        'text': '🤖 Chatbot (Optional)',
        'help': 'Chat with our AI assistant',
        'gradient': 'radial-gradient(circle at 25% 25%, #ffd1ff, #ff4de1 60%)',
        'glow': '0 0 18px #ff4de1, 0 0 38px #ff8cf0, 0 0 60px rgba(255,77,225,0.65)',
        'color': '#ffffff'
    }
]

# Create buttons
for btn in button_data:
    if btn['id'] == 'img_gen':
        # For image generation button with bubble effect
        button_html = f"""
        <div style="margin: 25px 0;">
            <a href="http://localhost:8504" target="_blank" style="text-decoration: none;">
                <button 
                    id="{btn['id']}"
                    class="neon-button"
                    onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                    onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                    data-glow="{btn['glow']}"
                    style="
                        width: 100%;
                        height: 80px;
                        border: none;
                        border-radius: 50px;
                        font-size: 20px;
                        font-weight: 800;
                        margin: 20px 0;
                        cursor: pointer;
                        background: {btn['gradient']} !important;
                        color: {btn['color']} !important;
                        box-shadow: {btn['glow']} !important;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        z-index: 1;
                        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                    "
                >
                    {btn['text']}
                </button>
            </a>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)
    elif btn['id'] == 'img_analysis':
        # For image analysis button with link to IMAGE ANALYSIS app
        button_html = f"""
        <div style="margin: 25px 0;">
            <a href="http://localhost:5000" target="_blank" style="text-decoration: none;">
                <button 
                    id="{btn['id']}"
                    class="neon-button"
                    onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                    onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                    data-glow="{btn['glow']}"
                    style="
                        width: 100%;
                        height: 80px;
                        border: none;
                        border-radius: 50px;
                        font-size: 20px;
                        font-weight: 800;
                        margin: 20px 0;
                        cursor: pointer;
                        background: {btn['gradient']} !important;
                        color: {btn['color']} !important;
                        box-shadow: {btn['glow']} !important;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        z-index: 1;
                        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                    "
                >
                    {btn['text']}
                </button>
            </a>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)
    elif btn['id'] == 'debate':
        # For debating AI button with link to DEBATING AI app
        button_html = f"""
        <div style="margin: 25px 0;">
            <a href="http://localhost:8503" target="_blank" style="text-decoration: none;">
                <button 
                    id="{btn['id']}"
                    class="neon-button"
                    onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                    onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                    data-glow="{btn['glow']}"
                    style="
                        width: 100%;
                        height: 80px;
                        border: none;
                        border-radius: 50px;
                        font-size: 20px;
                        font-weight: 800;
                        margin: 20px 0;
                        cursor: pointer;
                        background: {btn['gradient']} !important;
                        color: {btn['color']} !important;
                        box-shadow: {btn['glow']} !important;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        z-index: 1;
                        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                    "
                >
                    {btn['text']}
                </button>
            </a>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)
    elif btn['id'] == 'tourism':
        # For tourism guide button with link to TOUR GUIDE app
        button_html = f"""
        <div style="margin: 25px 0;">
            <a href="http://localhost:8505" target="_blank" style="text-decoration: none;">
                <button 
                    id="{btn['id']}"
                    class="neon-button"
                    onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                    onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                    data-glow="{btn['glow']}"
                    style="
                        width: 100%;
                        height: 80px;
                        border: none;
                        border-radius: 50px;
                        font-size: 20px;
                        font-weight: 800;
                        margin: 20px 0;
                        cursor: pointer;
                        background: {btn['gradient']} !important;
                        color: {btn['color']} !important;
                        box-shadow: {btn['glow']} !important;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        z-index: 1;
                        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                    "
                >
                    {btn['text']}
                </button>
            </a>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)
    elif btn['id'] == 'chatbot':
        # For chatbot button with link to CHATBOT app
        button_html = f"""
        <div style="margin: 25px 0;">
            <a href="http://localhost:8502" target="_blank" style="text-decoration: none;">
                <button 
                    id="{btn['id']}"
                    class="neon-button"
                    onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                    onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                    data-glow="{btn['glow']}"
                    style="
                        width: 100%;
                        height: 80px;
                        border: none;
                        border-radius: 50px;
                        font-size: 20px;
                        font-weight: 800;
                        margin: 20px 0;
                        cursor: pointer;
                        background: {btn['gradient']} !important;
                        color: {btn['color']} !important;
                        box-shadow: {btn['glow']} !important;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        z-index: 1;
                        text-shadow: 0 0 8px rgba(255,255,255,0.8) !important;
                    "
                >
                    {btn['text']}
                </button>
            </a>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)
    else:
        # For other buttons, keep the original behavior
        button_html = f"""
        <div style="margin: 25px 0;">
            <button 
                id="{btn['id']}"
                class="neon-button"
                onclick="handleButtonClick('{btn['id']}')"
                onmouseover="this.style.boxShadow='0 0 25px {btn['glow'].split(',')[0]}'"
                onmouseout="this.style.boxShadow='0 0 15px {btn['glow'].split(',')[0]}'"
                data-glow="{btn['glow']}"
                style="
                    width: 100%;
                    height: 80px;
                    border: none;
                    border-radius: 50px;
                    font-size: 20px;
                    font-weight: 800;
                    cursor: pointer;
                    background: {btn['gradient']};
                    color: {btn['color']};
                    box-shadow: {btn['glow']};
                    transition: all 0.3s ease;
                    outline: none;
                "
            >
                {btn['text']}
            </button>
        </div>"""
        st.markdown(button_html, unsafe_allow_html=True)

# Handle button clicks
if 'selected' not in st.session_state:
    st.session_state['selected'] = None


# Display the selected option
if st.session_state['selected']:
    st.success(f"You selected: {st.session_state['selected']}")
    
    # Add a button to go back
    if st.button("← Back to menu"):
        st.session_state['selected'] = None
        st.experimental_rerun()
        
    # Add content based on selection
    if st.session_state['selected'] == 'Image Generation':
        st.markdown("### Image Generation Parameters")
        st.slider("Creativity", 0, 100, 50)
        st.text_input("Image description")
        
    elif st.session_state['selected'] == 'Image Analysis':
        st.markdown("### Image Analysis")
        st.file_uploader("Upload an image")
        
    elif st.session_state['selected'] == 'Tourism Guide':
        st.markdown("### Tourism Guide")
        st.text_input("Destination")
        st.date_input("Travel dates")
        
    elif st.session_state['selected'] == 'Debating AI':
        st.markdown("### Debating AI")
        st.text_area("Your argument")
        
    elif st.session_state['selected'] == 'Chatbot':
        st.markdown("### Chat with our AI")
        st.text_input("Type your message")
        
    # Add a button to go back
    st.button("← Back to menu", on_click=lambda: setattr(st.session_state, 'selected', None))

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Display selected option
if 'selected' in st.session_state and st.session_state['selected']:
    st.success(f"You selected: {st.session_state['selected']}")
