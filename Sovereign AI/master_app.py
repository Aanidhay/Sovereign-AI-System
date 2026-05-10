# import subprocess
# import time
# import sys
# import os

# def run_streamlit(app_path, port, cwd, headless=True):
#     print(f"Starting Streamlit app: {app_path} on port {port}")
#     cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", str(port)]
#     if headless:
#         cmd.extend(["--server.headless", "true"])
#     return subprocess.Popen(
#         cmd,
#         cwd=cwd
#     )



# def main():
#     print("Starting AI Services Master Orchestrator")
#     print("Please wait while all services are initialized. This may take a moment...\n")
    
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     processes = []
    
#     try:
#         # 1. Image Analysis (Streamlit) - Port 5000
#         p_img_analysis = run_streamlit(
#             "app.py", 5000,
#             cwd=os.path.join(base_dir, "IMAGE ANALYSIS"),
#             headless=True
#         )
#         processes.append(p_img_analysis)
#         time.sleep(2)
        
#         # 2. Chatbot (Streamlit) - Port 8502
#         p_chatbot = run_streamlit(
#             "rag_app.py", 8502,
#             cwd=os.path.join(base_dir, "CHATBOT"),
#             headless=True
#         )
#         processes.append(p_chatbot)
        
#         # 3. Debating AI (Streamlit) - Port 8503
#         p_debate = run_streamlit(
#             "app.py", 8503,
#             cwd=os.path.join(base_dir, "DEBATING AI"),
#             headless=True
#         )
#         processes.append(p_debate)
        
#         # 4. Image Generation (Streamlit) - Port 8504
#         p_img_gen = run_streamlit(
#             "image_generator.py", 8504,
#             cwd=os.path.join(base_dir, "INTERFACE"),
#             headless=True
#         )
#         processes.append(p_img_gen)
        
#         # 5. Tour Guide Recommender (Streamlit) - Port 8505
#         p_tour = run_streamlit(
#             "tour_app.py", 8505,
#             cwd=os.path.join(base_dir, "TOUR GUIDE RECOMMENDER"),
#             headless=True
#         )
#         processes.append(p_tour)
        
#         # 6. Main Dashboard (Streamlit) - Port 8501
#         p_main = run_streamlit(
#             "app.py", 8501,
#             cwd=os.path.join(base_dir, "INTERFACE"),
#             headless=False
#         )
#         processes.append(p_main)
        
#         print("\nAll services started successfully!")
#         print("Access the Main Dashboard at: http://localhost:8501")
#         print("Press Ctrl+C to stop all services.\n")
        
#         # Keep the main process alive
#         for p in processes:
#             p.wait()
            
#     except KeyboardInterrupt:
#         print("\nShutting down all services gracefully...")
#         for p in processes:
#             p.terminate()
#             try:
#                 p.wait(timeout=3)
#             except subprocess.TimeoutExpired:
#                 p.kill()
#         print("Shutdown complete.")

# if __name__ == "__main__":
#     main()


import subprocess
import time
import sys
import os

def run_streamlit(app_path, port, cwd, base_path=""):
    print(f"🚀 Starting {app_path} on port {port} at path /{base_path}")
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path, 
        "--server.port", str(port),
        "--server.address", "0.0.0.0"
    ]
    if base_path:
        cmd.extend(["--server.baseUrlPath", base_path])
        
    return subprocess.Popen(cmd, cwd=cwd)

def main():
    print("🌟 Starting AI Services Master Orchestrator 🌟")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processes = []
    
    try:
        # 1. Image Analysis - Port 5000
        processes.append(run_streamlit("app.py", 5000, os.path.join(base_dir, "IMAGE ANALYSIS"), "analysis"))
        time.sleep(2)
        # 2. Chatbot - Port 8502
        processes.append(run_streamlit("rag_app.py", 8502, os.path.join(base_dir, "CHATBOT"), "chatbot"))
        # 3. Debating AI - Port 8503
        processes.append(run_streamlit("app.py", 8503, os.path.join(base_dir, "DEBATING AI"), "debate"))
        # 4. Image Generation - Port 8504
        processes.append(run_streamlit("image_generator.py", 8504, os.path.join(base_dir, "INTERFACE"), "image-gen"))
        # 5. Tour Guide Recommender - Port 8505
        processes.append(run_streamlit("tour_app.py", 8505, os.path.join(base_dir, "TOUR GUIDE RECOMMENDER"), "tour"))
        # 6. Main Dashboard - Port 8501
        processes.append(run_streamlit("app.py", 8501, os.path.join(base_dir, "INTERFACE"), ""))
        
        for p in processes:
            p.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services gracefully...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()