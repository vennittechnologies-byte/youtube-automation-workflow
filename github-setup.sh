#!/bin/bash

# GitHub Integration Script
# Automated setup for checking code into GitHub

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 GitHub Integration - YouTube Automation Workflow          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo

# Function to print colored messages
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
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Collect information
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Step 1: GitHub Configuration${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name [youtube-automation-workflow]: " REPO_NAME
REPO_NAME=${REPO_NAME:-youtube-automation-workflow}

read -p "Enter your Git name (for commits) [YouTube Automation]: " GIT_NAME
GIT_NAME=${GIT_NAME:-YouTube Automation}

read -p "Enter your Git email: " GIT_EMAIL

echo
print_info "Configuration:"
echo "  GitHub Username: $GITHUB_USERNAME"
echo "  Repository Name: $REPO_NAME"
echo "  Git Name: $GIT_NAME"
echo "  Git Email: $GIT_EMAIL"
echo

read -p "Is this correct? (y/N): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Setup cancelled. Please run again."
    exit 1
fi

# Step 2: Check prerequisites
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔍 Step 2: Checking Prerequisites${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Check Git
if command -v git &> /dev/null; then
    print_success "Git is installed: $(git --version)"
else
    print_error "Git is not installed!"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
fi

# Check GitHub CLI (optional)
if command -v gh &> /dev/null; then
    print_success "GitHub CLI is installed"
    GH_CLI_AVAILABLE=true
else
    print_warning "GitHub CLI not installed (optional)"
    echo "  You can install it for easier setup: https://cli.github.com/"
    GH_CLI_AVAILABLE=false
fi

# Step 3: Security check
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔒 Step 3: Security Verification${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

print_info "Checking for sensitive files..."

# Check .gitignore exists
if [ -f .gitignore ]; then
    print_success ".gitignore found"
else
    print_error ".gitignore not found!"
    exit 1
fi

# Check for sensitive files
SENSITIVE_FILES=(".env" "config/client_secrets.json" "config/token.pickle")
FOUND_SENSITIVE=false

for file in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_warning "Found sensitive file: $file"
        FOUND_SENSITIVE=true
    fi
done

if [ "$FOUND_SENSITIVE" = true ]; then
    print_info "These files should be in .gitignore and will NOT be committed"
fi

# Search for potential API keys in code
print_info "Scanning for potential secrets in code..."
if grep -r "sk-" scripts/ 2>/dev/null | grep -v ".pyc" | grep -v "__pycache__"; then
    print_error "Found potential API keys in code!"
    echo "Please remove these before continuing."
    exit 1
else
    print_success "No obvious secrets found in code"
fi

# Step 4: Initialize Git repository
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📦 Step 4: Initializing Git Repository${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Check if already a git repo
if [ -d .git ]; then
    print_warning "Git repository already initialized"
    read -p "Reinitialize? (y/N): " REINIT
    if [[ $REINIT =~ ^[Yy]$ ]]; then
        rm -rf .git
        git init
        print_success "Repository reinitialized"
    fi
else
    git init
    print_success "Git repository initialized"
fi

# Configure git
git config user.name "$GIT_NAME"
git config user.email "$GIT_EMAIL"
print_success "Git user configured"

# Set default branch to main
git branch -M main 2>/dev/null || git checkout -b main
print_success "Default branch set to 'main'"

# Step 5: Prepare commit
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📝 Step 5: Preparing Initial Commit${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Update README with actual username
print_info "Updating README with your username..."
if [ -f README.md ]; then
    sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
    rm -f README.md.bak
    print_success "README updated"
fi

# Stage files
print_info "Staging files..."
git add .

# Show what will be committed
echo
print_info "Files to be committed:"
git status --short | head -20
TOTAL_FILES=$(git status --short | wc -l)
if [ $TOTAL_FILES -gt 20 ]; then
    echo "... and $(($TOTAL_FILES - 20)) more files"
fi

echo
read -p "Proceed with commit? (Y/n): " PROCEED
if [[ $PROCEED =~ ^[Nn]$ ]]; then
    echo "Commit cancelled. Files are staged. You can commit manually."
    exit 0
fi

# Create initial commit
git commit -m "Initial commit: Complete YouTube automation workflow

Features:
- AI script generation (Ollama/Groq)
- Text-to-speech voiceover (Edge-TTS)
- Automatic stock footage download (Pexels)
- Thumbnail generation (Pillow)
- Video composition (MoviePy + FFmpeg)
- YouTube upload automation
- GitHub Actions scheduling
- 100% free tools ($0/month)

Complete documentation included:
- Setup guides (QUICKSTART.md, SETUP_SUMMARY.md)
- Technical docs (ARCHITECTURE.md)
- Troubleshooting (TROUBLESHOOTING.md)
- Contribution guidelines (CONTRIBUTING.md)
- MIT License"

print_success "Initial commit created"

# Step 6: Create GitHub repository
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🌐 Step 6: Creating GitHub Repository${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

if [ "$GH_CLI_AVAILABLE" = true ]; then
    echo "Choose repository creation method:"
    echo "  1) Use GitHub CLI (automatic)"
    echo "  2) Manual (you create repo on GitHub)"
    read -p "Enter choice (1-2): " CREATE_METHOD
else
    CREATE_METHOD=2
fi

if [ "$CREATE_METHOD" = "1" ] && [ "$GH_CLI_AVAILABLE" = true ]; then
    print_info "Checking GitHub CLI authentication..."
    
    if gh auth status &>/dev/null; then
        print_success "Already authenticated with GitHub"
    else
        print_info "Please authenticate with GitHub..."
        gh auth login
    fi
    
    echo
    read -p "Make repository public? (Y/n): " MAKE_PUBLIC
    if [[ $MAKE_PUBLIC =~ ^[Nn]$ ]]; then
        VISIBILITY="--private"
    else
        VISIBILITY="--public"
    fi
    
    print_info "Creating GitHub repository..."
    gh repo create "$REPO_NAME" $VISIBILITY \
        --description "End-to-End YouTube Video Upload Workflow - Automated video creation with AI, TTS, and stock footage" \
        --source=. \
        --remote=origin \
        --push
    
    print_success "Repository created and code pushed!"
    
else
    # Manual method
    print_warning "Please create the repository manually:"
    echo
    echo "  1. Go to: https://github.com/new"
    echo "  2. Repository name: $REPO_NAME"
    echo "  3. Description: End-to-End YouTube Video Upload Workflow"
    echo "  4. Choose Public or Private"
    echo "  5. DO NOT initialize with README, .gitignore, or license"
    echo "  6. Click 'Create repository'"
    echo
    read -p "Press Enter when you've created the repository..."
    
    # Add remote and push
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    
    print_info "Adding remote repository..."
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
    print_success "Remote added: $REPO_URL"
    
    echo
    print_info "Pushing to GitHub..."
    echo "  (You may be prompted for credentials)"
    
    if git push -u origin main; then
        print_success "Code pushed successfully!"
    else
        print_error "Push failed!"
        echo
        echo "Troubleshooting:"
        echo "  1. Check your GitHub credentials"
        echo "  2. Verify the repository was created"
        echo "  3. Try pushing manually:"
        echo "     git push -u origin main"
        exit 1
    fi
fi

# Step 7: Post-upload instructions
echo
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}✅ Step 7: Setup Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

print_success "Your code is now on GitHub!"
echo

REPO_FULL_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo -e "${GREEN}🔗 Repository URL:${NC} $REPO_FULL_URL"
echo

echo -e "${YELLOW}📋 Next Steps:${NC}"
echo
echo "1. Configure Repository:"
echo "   • Go to: $REPO_FULL_URL"
echo "   • Click ⚙️  next to 'About'"
echo "   • Add description and topics"
echo
echo "2. Setup GitHub Actions (Optional):"
echo "   • Go to: $REPO_FULL_URL/settings/secrets/actions"
echo "   • Add these secrets:"
echo "     - PEXELS_API_KEY"
echo "     - GROQ_API_KEY (if using Groq)"
echo "     - YOUTUBE_CLIENT_SECRETS"
echo "     - YOUTUBE_TOKEN_PICKLE"
echo
echo "3. Share Your Work:"
echo "   • Star your own repo: $REPO_FULL_URL"
echo "   • Share on social media"
echo "   • Submit to awesome lists"
echo
echo "4. Create First Release:"
echo "   git tag -a v1.0.0 -m 'Initial release'"
echo "   git push origin v1.0.0"
echo

echo -e "${BLUE}📚 Documentation:${NC}"
echo "   • README.md - Overview and setup"
echo "   • QUICKSTART.md - 10-minute guide"
echo "   • TROUBLESHOOTING.md - Problem solving"
echo "   • GITHUB_SETUP.md - Detailed GitHub info"
echo

print_success "Setup complete! Happy automating! 🚀"
