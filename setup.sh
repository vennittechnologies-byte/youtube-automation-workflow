#!/bin/bash

# Automated YouTube Video Pipeline - Setup Script
# This script helps you set up the project for the first time

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚀 Automated YouTube Video Pipeline - Setup                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check system requirements
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Step 1: Checking system requirements"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found!"
    echo "  Please install Python 3.11 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check FFmpeg
if command_exists ffmpeg; then
    print_success "FFmpeg found"
else
    print_warning "FFmpeg not found"
    echo
    echo "  FFmpeg is required for video processing. Install it with:"
    echo
    echo "  Ubuntu/Debian:  sudo apt install ffmpeg"
    echo "  macOS:          brew install ffmpeg"
    echo "  Windows:        Download from https://ffmpeg.org/download.html"
    echo
    read -p "Continue without FFmpeg? (y/N): " continue_without_ffmpeg
    if [[ ! $continue_without_ffmpeg =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Git
if command_exists git; then
    print_success "Git found"
else
    print_warning "Git not found (optional)"
fi

echo

# Step 2: Install Python dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Step 2: Installing Python dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

read -p "Install Python dependencies? (Y/n): " install_deps
if [[ ! $install_deps =~ ^[Nn]$ ]]; then
    print_info "Installing dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_warning "Skipped dependency installation"
fi

echo

# Step 3: Setup environment variables
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  Step 3: Configure environment variables"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

if [ -f .env ]; then
    print_warning ".env file already exists"
    read -p "Overwrite existing .env file? (y/N): " overwrite_env
    if [[ ! $overwrite_env =~ ^[Yy]$ ]]; then
        print_info "Keeping existing .env file"
    else
        cp .env.example .env
        print_success "Created new .env file from template"
    fi
else
    cp .env.example .env
    print_success "Created .env file from template"
fi

echo
print_info "Please edit .env and add your API keys:"
echo
echo "  Required:"
echo "    - PEXELS_API_KEY     (get from https://www.pexels.com/api/)"
echo
echo "  Optional (choose one for script generation):"
echo "    - GROQ_API_KEY       (get from https://console.groq.com)"
echo "    - Or install Ollama  (see Step 4)"
echo
read -p "Open .env in editor now? (Y/n): " edit_env
if [[ ! $edit_env =~ ^[Nn]$ ]]; then
    ${EDITOR:-nano} .env
fi

echo

# Step 4: Setup LLM (Ollama or Groq)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 Step 4: Setup LLM for script generation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

echo "Choose your LLM backend:"
echo "  1) Ollama (local, private, requires ~4GB disk) - RECOMMENDED"
echo "  2) Groq (cloud API, requires API key)"
echo "  3) Skip for now"
echo
read -p "Enter choice (1-3): " llm_choice

case $llm_choice in
    1)
        if command_exists ollama; then
            print_success "Ollama already installed"
        else
            print_info "Installing Ollama..."
            curl -fsSL https://ollama.com/install.sh | sh
            print_success "Ollama installed"
        fi
        
        print_info "Pulling Llama 3.1 model (this may take a few minutes)..."
        ollama pull llama3.1:8b
        print_success "Llama 3.1 model ready"
        
        # Update .env
        sed -i.bak 's/USE_OLLAMA=.*/USE_OLLAMA=true/' .env
        print_success "Configured to use Ollama"
        ;;
    2)
        print_info "Using Groq API"
        echo
        echo "  Get your Groq API key from: https://console.groq.com"
        echo "  Add it to .env: GROQ_API_KEY=your_key_here"
        echo
        
        # Update .env
        sed -i.bak 's/USE_OLLAMA=.*/USE_OLLAMA=false/' .env
        print_success "Configured to use Groq"
        ;;
    *)
        print_warning "Skipped LLM setup - you'll need to configure this later"
        ;;
esac

echo

# Step 5: Setup YouTube OAuth
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📺 Step 5: Setup YouTube OAuth credentials"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

print_info "YouTube API setup instructions:"
echo
echo "  1. Go to: https://console.cloud.google.com"
echo "  2. Create a new project"
echo "  3. Enable 'YouTube Data API v3'"
echo "  4. Create OAuth 2.0 credentials (Desktop app)"
echo "  5. Download the JSON file"
echo "  6. Save it as: config/client_secrets.json"
echo

read -p "Have you already completed YouTube OAuth setup? (y/N): " youtube_done
if [[ $youtube_done =~ ^[Yy]$ ]]; then
    if [ -f config/client_secrets.json ]; then
        print_success "Found config/client_secrets.json"
    else
        print_warning "config/client_secrets.json not found"
        echo "  Please add your OAuth credentials to config/client_secrets.json"
    fi
else
    print_info "Setup YouTube OAuth before uploading videos"
    echo "  You can still test the pipeline with --no-upload flag"
fi

echo

# Step 6: Create output directories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Step 6: Creating output directories"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

mkdir -p output/{videos,audio,clips,thumbnails}
mkdir -p config
print_success "Created output directories"

echo

# Step 7: Test installation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Step 7: Testing installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

read -p "Run basic tests? (Y/n): " run_tests
if [[ ! $run_tests =~ ^[Nn]$ ]]; then
    print_info "Testing Python imports..."
    
    python3 -c "import moviepy; print('✅ MoviePy OK')" 2>/dev/null || print_error "MoviePy import failed"
    python3 -c "from PIL import Image; print('✅ Pillow OK')" 2>/dev/null || print_error "Pillow import failed"
    python3 -c "import edge_tts; print('✅ Edge-TTS OK')" 2>/dev/null || print_error "Edge-TTS import failed"
    python3 -c "import requests; print('✅ Requests OK')" 2>/dev/null || print_error "Requests import failed"
    
    print_success "Basic tests complete"
fi

echo

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

echo "📋 Next Steps:"
echo
echo "  1. Edit .env and add your API keys (especially PEXELS_API_KEY)"
echo "  2. (Optional) Setup YouTube OAuth credentials"
echo "  3. Test the pipeline:"
echo
echo "     python main.py --no-upload"
echo
echo "  4. For automated scheduling, setup GitHub Actions:"
echo "     See README.md for GitHub secrets configuration"
echo

echo "📚 Documentation: README.md"
echo "❓ Need help? Check the troubleshooting section in README.md"
echo

print_success "You're all set! Happy automating! 🚀"
