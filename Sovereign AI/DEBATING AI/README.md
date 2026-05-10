# 🤖 AI Debate Arena

An interactive Streamlit application where AI agents debate on user-selected topics using LangChain, LangGraph, and Ollama with Llama 3.2 models.

## Features

- **Interactive Interface**: Clean and modern Streamlit UI
- **AI Agents**: Two AI agents that can debate FOR, AGAINST, or NEUTRAL positions
- **LangGraph Integration**: Uses LangGraph for structured debate workflow
- **Llama 3.2 Models**: Powered by Ollama with Llama 3.2, Llama 3.2, or Llama 2
- **Judge Agent**: An impartial AI judge evaluates debates and declares winners
- **Debate History**: Tracks debate statistics and history
- **Configurable Rounds**: Adjustable number of debate rounds
- **No API Keys**: Uses local Ollama installation

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [https://ollama.com](https://ollama.com)

### 2. Pull Llama Model

```bash
# Start Ollama server
ollama serve

# Pull Llama 3.2 (recommended)
ollama pull llama3.2

# Alternatively, pull other models
ollama pull llama3.2
ollama pull llama2
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## How to Use

1. **Start Ollama**: Make sure Ollama is running (`ollama serve`)
2. **Open App**: Launch the Streamlit application
3. **Select Model**: Choose Llama 3.2, Llama 3.2, or Llama 2
4. **Choose Topic**: Enter any debate topic in the text area
5. **Select Positions**: Choose FOR, AGAINST, or NEUTRAL for each agent
6. **Configure Rounds**: Set the number of debate rounds (1-5)
7. **Start Debate**: Click the "Start Debate" button
8. **Watch the Debate**: See AI agents argue in real-time
9. **View Results**: Check the judge's decision and reasoning

## Architecture

### Components

- **`app.py`**: Main Streamlit application
- **`debate_agents.py`**: Core debate logic with AI agents
- **`DebateAgent`**: Individual AI agent class
- **`JudgeAgent`**: AI judge for evaluating debates
- **`DebateOrchestrator`**: Manages the debate workflow using LangGraph

### Debate Flow

1. User inputs topic and selects agent positions
2. LangGraph workflow orchestrates the debate
3. Agents take turns making arguments using Llama models
4. Judge evaluates all arguments
5. Winner is declared with detailed reasoning

## Dependencies

- `streamlit`: Web application framework
- `langchain`: AI/LLM framework
- `langchain-community`: Community extensions
- `langchain-ollama`: Ollama integration
- `langgraph`: Graph-based workflow orchestration
- `ollama`: Ollama API client
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for Ollama status

## Troubleshooting

### Common Issues

1. **Ollama Not Running**: Start Ollama with `ollama serve`
2. **Model Not Found**: Pull the model with `ollama pull llama3.2`
3. **Import Errors**: Ensure all dependencies are installed
4. **Connection Issues**: Check that Ollama is running on localhost:11434

### Debug Mode

To enable debug logging, add this to `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Model Performance

- **Llama 3.2**: Best performance, latest model
- **Llama 3.2**: Good performance, widely tested
- **Llama 2**: Faster but less capable

## Customization

### Adding New Models

Update the model selection in `app.py`:

```python
model_name = st.selectbox(
    "Select Model",
    ["llama3.2", "llama3.2", "llama2", "your-custom-model"],
    index=0
)
```

### Adjusting Judge Criteria

Modify the evaluation criteria in `JudgeAgent.evaluate_debate()` to change how debates are judged.

### Changing Debate Structure

Update the `DebateOrchestrator` class to modify the debate flow and logic.

## License

This project is open source and available under the MIT License.
