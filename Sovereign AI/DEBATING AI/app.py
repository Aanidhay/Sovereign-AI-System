import streamlit as st
import os
from dotenv import load_dotenv
from debate_agents import DebateOrchestrator
import time
import subprocess
import sys

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .debate-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .agent-1 {
        border-left: 5px solid #FF6B6B;
        padding-left: 15px;
        color: #333333;
    }
    .agent-2 {
        border-left: 5px solid #4ECDC4;
        padding-left: 15px;
        color: #333333;
    }
    .winner-announcement {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        color: #000000;
        margin: 20px 0;
    }
    .argument-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🤖 AI Debate Arena")
    st.markdown("*Watch AI agents debate on any topic you choose!*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_name = st.selectbox(
            "Select Model",
            ["llama3.2:1b", "llama3.2", "llama2"],
            index=0,
            help="Select the Llama model to use for the debate"
        )
        
        # Check if Ollama is running
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                st.success("✅ Ollama is running")
            else:
                st.error("❌ Ollama is not responding")
        except:
            st.error("❌ Ollama is not running. Please start Ollama first.")
            st.code("ollama serve")
        
                
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. Make sure Ollama is running: `ollama serve`
        2. Pull the model: `ollama pull llama3.2`
        3. Choose a debate topic
        4. Select positions for both agents
        5. Click 'Start Debate' to begin
        6. Watch the AI agents debate!
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Debate Setup")
        
        with st.form("debate_setup_form"):
            # Topic input with 20-word limit
            topic = st.text_area(
                "Debate Topic (Maximum 20 words)",
                placeholder="Enter a topic for the AI agents to debate (e.g., 'Should artificial intelligence be regulated?')",
                height=100,
                max_chars=200  # Approximate 20 words limit
            )
            
            # Word count display and validation
            if topic:
                word_count = len(topic.split())
                if word_count > 20:
                    st.error(f"⚠️ Topic exceeds 20-word limit! Current: {word_count} words")
                    topic = " ".join(topic.split()[:20])  # Auto-truncate
                    st.info(f"📝 Auto-truncated to: {topic}")
                else:
                    st.success(f"✅ Topic length: {word_count}/20 words")
            
            # Agent position selection
            col_pos1, col_pos2 = st.columns(2)
            
            with col_pos1:
                agent1_position = st.selectbox(
                    "Agent 1 Position",
                    ["FOR", "AGAINST", "NEUTRAL"],
                    index=0,
                    key="agent1_pos"
                )
            
            with col_pos2:
                agent2_position = st.selectbox(
                    "Agent 2 Position",
                    ["FOR", "AGAINST", "NEUTRAL"],
                    index=1,
                    key="agent2_pos"
                )
            
            # Start debate button
            start_debate = st.form_submit_button(
                "🚀 Start Debate",
                type="primary"
            )
    
    with col2:
        st.header("📊 Debate Stats & MCP Context")
        
        # Display debate statistics
        if "debate_history" in st.session_state:
            total_debates = len(st.session_state.debate_history)
            st.metric("Total Debates", total_debates)
            
            if total_debates > 0:
                agent1_wins = sum(1 for d in st.session_state.debate_history 
                                if d.get("winner") == "Agent 1")
                agent2_wins = sum(1 for d in st.session_state.debate_history 
                                if d.get("winner") == "Agent 2")
                ties = sum(1 for d in st.session_state.debate_history 
                          if d.get("winner") == "Tie")
                
                st.write(f"🏆 Agent 1 Wins: {agent1_wins}")
                st.write(f"🏆 Agent 2 Wins: {agent2_wins}")
                st.write(f"🤝 Ties: {ties}")
        
        # Display MCP global stats if available
        try:
            from mcp_server import mcp_server
            global_stats = mcp_server.get_global_stats()
            
            st.markdown("---")
            st.markdown("### 🌐 MCP Global Stats")
            st.metric("📝 Total Sessions", global_stats.get("total_debates", 0))
            st.metric("🔄 Active Sessions", global_stats.get("active_sessions", 0))
            
            if global_stats.get("recent_topics"):
                st.markdown("**Recent Topics:**")
                for topic in global_stats["recent_topics"][-3:]:
                    st.write(f"• {topic}")
                    
        except Exception as e:
            st.info("MCP stats available after first debate")
    
    # Initialize session state
    if "debate_history" not in st.session_state:
        st.session_state.debate_history = []
    
    if "current_debate" not in st.session_state:
        st.session_state.current_debate = None
    
    # Handle debate start
    if start_debate and topic:
        with st.spinner("🤔 AI agents are preparing their arguments..."):
            try:
                # Initialize debate orchestrator
                orchestrator = DebateOrchestrator(model_name=model_name)
                
                # Run debate
                debate_result = orchestrator.run_debate(
                    topic=topic,
                    agent1_position=agent1_position,
                    agent2_position=agent2_position,
                    max_rounds=3
                )
                
                st.session_state.current_debate = debate_result
                st.session_state.debate_history.append(debate_result)
                
                # Display MCP session info
                if debate_result.get("session_id"):
                    st.success(f"🎉 Debate completed successfully!")
                    st.info(f"🆔 Session ID: {debate_result['session_id'][:8]}...")
                else:
                    st.success("🎉 Debate completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error during debate: {str(e)}")
                st.error("Please check that Ollama is running and the model is available.")
    
    # Display current debate
    if st.session_state.current_debate:
        debate = st.session_state.current_debate
        
        st.markdown("---")
        st.header("🗣️ Debate Results")
        
        # Topic and positions
        st.markdown(f"### **Topic:** {debate['topic']}")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"🤖 **Agent 1 Position:** {debate['agent1_position']}")
        with col_info2:
            st.markdown(f"🤖 **Agent 2 Position:** {debate['agent2_position']}")
        
        # Debate rounds
        st.markdown("### 💬 Debate Rounds")
        
        for round_num in range(debate['rounds']):
            with st.expander(f"Round {round_num + 1}", expanded=True):
                col_a1, col_a2 = st.columns(2)
                
                with col_a1:
                    st.markdown('<div class="agent-1">', unsafe_allow_html=True)
                    st.markdown(f"**🤖 Agent 1 ({debate['agent1_position']})**")
                    if round_num < len(debate['agent1_arguments']):
                        st.info(f"**Agent 1 Argument:**\n\n{debate['agent1_arguments'][round_num]}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_a2:
                    st.markdown('<div class="agent-2">', unsafe_allow_html=True)
                    st.markdown(f"**🤖 Agent 2 ({debate['agent2_position']})**")
                    if round_num < len(debate['agent2_arguments']):
                        st.success(f"**Agent 2 Argument:**\n\n{debate['agent2_arguments'][round_num]}")
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Winner announcement
        st.markdown("### 🏆 Judge's Decision")
        
        winner_color = {
            "Agent 1": "#FF6B6B",
            "Agent 2": "#4ECDC4",
            "Tie": "#FFD700"
        }
        
        winner_emoji = {
            "Agent 1": "🥇",
            "Agent 2": "🥈", 
            "Tie": "🤝"
        }
        
        st.markdown(f'''
        <div class="winner-announcement" style="background-color: {winner_color.get(debate['winner'], '#FFD700')};">
            <h2>{winner_emoji.get(debate['winner'], '🏆')} Winner: {debate['winner']}</h2>
        </div>
        ''', unsafe_allow_html=True)
        
        # Judge's reasoning
        with st.expander("📋 Judge's Reasoning", expanded=True):
            st.write(debate['reasoning'])
            
            # Display key points if available
            if 'key_points' in debate and debate['key_points']:
                st.info(f"**🎯 Key Winning Points:** {debate['key_points']}")
        
        # Detailed Points Analysis
        if debate.get('agent1_points') or debate.get('agent2_points'):
            st.markdown("### 📊 Detailed Points Analysis")
            
            col_analysis1, col_analysis2 = st.columns(2)
            
            with col_analysis1:
                st.markdown("**🤖 Agent 1 Specific Points:**")
                agent1_points = debate.get('agent1_points', {})
                
                # Show actual examples used
                if agent1_points.get('examples_used'):
                    st.success(f"📚 Evidence & Examples:")
                    for example in agent1_points['examples_used']:
                        st.write(f"• {example}")
                
                # Show actual reasoning chains
                if agent1_points.get('reasoning_chains'):
                    st.info(f"🧠 Logical Reasoning:")
                    for reasoning in agent1_points['reasoning_chains']:
                        st.write(f"• {reasoning}")
                
                # Show actual counter-arguments
                if agent1_points.get('counter_points'):
                    st.warning(f"⚔️ Counter-Arguments:")
                    for counter in agent1_points['counter_points']:
                        st.write(f"• {counter}")
                
                # Show specific claims
                if agent1_points.get('specific_claims'):
                    st.write(f"💬 Key Claims:")
                    for claim in agent1_points['specific_claims']:
                        st.write(f"• {claim}")
                
                st.metric("💪 Total Strength", agent1_points.get('total_strength', 0))
            
            with col_analysis2:
                st.markdown("**🤖 Agent 2 Specific Points:**")
                agent2_points = debate.get('agent2_points', {})
                
                # Show actual examples used
                if agent2_points.get('examples_used'):
                    st.success(f"📚 Evidence & Examples:")
                    for example in agent2_points['examples_used']:
                        st.write(f"• {example}")
                
                # Show actual reasoning chains
                if agent2_points.get('reasoning_chains'):
                    st.info(f"🧠 Logical Reasoning:")
                    for reasoning in agent2_points['reasoning_chains']:
                        st.write(f"• {reasoning}")
                
                # Show actual counter-arguments
                if agent2_points.get('counter_points'):
                    st.warning(f"⚔️ Counter-Arguments:")
                    for counter in agent2_points['counter_points']:
                        st.write(f"• {counter}")
                
                # Show specific claims
                if agent2_points.get('specific_claims'):
                    st.write(f"💬 Key Claims:")
                    for claim in agent2_points['specific_claims']:
                        st.write(f"• {claim}")
                
                st.metric("💪 Total Strength", agent2_points.get('total_strength', 0))
        
        # MCP Context Information
        if debate.get('session_id'):
            st.markdown("### 🔗 MCP Context Information")
            col_mcp1, col_mcp2 = st.columns(2)
            
            with col_mcp1:
                st.metric("🆔 Session ID", debate['session_id'][:8] + "...")
                if debate.get('mcp_context'):
                    st.metric("📅 Timestamp", debate['mcp_context'].get('timestamp', 'Unknown')[:10])
            
            with col_mcp2:
                if debate.get('global_stats'):
                    stats = debate['global_stats']
                    st.metric("🌐 Total Sessions", stats.get('total_debates', 0))
                    st.metric("🔄 Active Sessions", stats.get('active_sessions', 0))
        
        # Detailed scores
        col_score1, col_score2 = st.columns(2)
        with col_score1:
            st.metric("🤖 Agent 1 Score", debate.get('agent1_score', 'N/A'))
        with col_score2:
            st.metric("🤖 Agent 2 Score", debate.get('agent2_score', 'N/A'))
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 New Debate", type="secondary"):
                st.session_state.current_debate = None
                st.rerun()
        
        with col_btn2:
            if st.button("💾 Save Debate"):
                # Here you could implement saving to file or database
                st.success("Debate saved to history!")
        
        with col_btn3:
            if st.button("📊 View Statistics"):
                st.json({
                    "total_arguments_agent1": len(debate['agent1_arguments']),
                    "total_arguments_agent2": len(debate['agent2_arguments']),
                    "rounds": debate['rounds'],
                    "winner": debate['winner']
                })
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<center><small>🤖 AI Debate Arena - Powered by LangChain & LangGraph</small></center>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
