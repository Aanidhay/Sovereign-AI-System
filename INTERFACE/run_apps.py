import subprocess
import time
import threading
import webbrowser

def run_main_app():
    """Run the main Streamlit app on port 8501"""
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501"])

def run_image_generator():
    """Run the image generator app on port 8502"""
    subprocess.run(["streamlit", "run", "image_generator.py", "--server.port", "8502"])

if __name__ == "__main__":
    print("🚀 Starting AI Services Dashboard...")
    print("📱 Main App: http://localhost:8501")
    print("🖼️ Image Generator: http://localhost:8502")
    print("\n⚠️  Make sure both apps are running for the new tab functionality to work!")
    
    # Start both apps in separate threads
    main_thread = threading.Thread(target=run_main_app)
    image_thread = threading.Thread(target=run_image_generator)
    
    main_thread.start()
    time.sleep(2)  # Give main app time to start
    image_thread.start()
    
    # Open main app in browser after a short delay
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    
    # Wait for both threads to complete
    main_thread.join()
    image_thread.join()
