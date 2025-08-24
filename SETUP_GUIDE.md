# Complete Setup Guide

# Run command for the chatbot-:       streamlit run app_frontend.py

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 2GB free space
- **GPU** (Optional): NVIDIA GPU with CUDA support for acceleration

### Required Accounts
1. **OpenAI Account**: For GPT API access
2. **LangSmith Account**: For observability (optional but recommended)
3. **Alpha Vantage Account**: For stock price API (free tier available)

## Installation Steps

### 1. Clone or Download Project
\`\`\`bash
# If using git
git clone <your-repo-url>
cd chatbot-project

# Or download and extract ZIP file
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv chatbot_env

# Activate virtual environment
# On Windows:
chatbot_env\Scripts\activate
# On macOS/Linux:
source chatbot_env/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
# Install required packages
pip install langgraph langchain langchain-openai python-dotenv
pip install streamlit langgraph-checkpoint-sqlite langsmith
pip install langchain-community duckduckgo-search ddgs
pip install torch requests uuid

# For GPU support (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
\`\`\`

### 4. Environment Configuration
Create a `.env` file in the project root directory:

\`\`\`env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: LangSmith for observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=ls__your-langsmith-api-key-here
LANGCHAIN_PROJECT=my-chatbot-project

# Optional: Custom model settings
MODEL_TEMPERATURE=0.7
MAX_TOKENS=2000
\`\`\`

### 5. API Key Setup

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new API key
5. Copy key to `.env` file

#### LangSmith API Key (Optional)
1. Visit [LangSmith](https://smith.langchain.com/)
2. Sign up for account
3. Create new project
4. Get API key from settings
5. Copy key to `.env` file

## Running the Application

### 1. Start the Chatbot
\`\`\`bash
# Make sure virtual environment is activated
# Navigate to project directory
streamlit run app_frontend.py
\`\`\`

### 2. Access the Interface
- Open browser to `http://localhost:8501`
- The chatbot interface should load automatically

### 3. First Time Setup
1. Click "New Chat" to start first conversation
2. Test basic functionality with simple question
3. Test tools with "search for latest news" or "what's AAPL stock price?"


### 2. Test Core Features
- **Basic Chat**: Ask "Hello, how are you?"
- **Web Search**: Ask "Search for latest AI news"
- **Stock Prices**: Ask "What's Apple's stock price?"
- **Memory**: Start new conversation, verify history saves

### 3. Check Database Creation
Verify `chatbot.db` file is created in project directory.

## Troubleshooting

### Common Issues

#### "Module not found" errors
\`\`\`bash
# Ensure virtual environment is activated
# Reinstall packages
pip install -r requirements.txt
\`\`\`

#### "OpenAI API key not found"
- Check `.env` file exists in project root
- Verify API key format starts with `sk-`
- Ensure no extra spaces in `.env` file

#### "Database locked" error
\`\`\`bash
# Stop all running instances
# Delete chatbot.db file
# Restart application
\`\`\`

#### GPU not detected
\`\`\`bash
# Check CUDA installation
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
\`\`\`

### Performance Issues

#### Slow responses
- Check internet connection for API calls
- Verify GPU utilization with `nvidia-smi`
- Consider reducing model temperature

#### Memory issues
- Close other applications
- Reduce conversation history length
- Consider using smaller model variants

## Advanced Configuration

### Custom Model Settings
Add to `.env`:
\`\`\`env
MODEL_NAME=gpt-4
MODEL_TEMPERATURE=0.5
MAX_TOKENS=1500
TIMEOUT_SECONDS=30
\`\`\`


### Using Streamlit Cloud # For Deployment 
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Add environment variables in Streamlit Cloud dashboard
4. Deploy automatically




