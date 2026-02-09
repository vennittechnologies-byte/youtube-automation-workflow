# 🚀 Your GitHub Integration Commands

Follow these exact commands to push your code to GitHub.

## Prerequisites

Before running these commands, you need:
1. ✅ GitHub account created
2. ✅ Git installed on your machine
3. ✅ Project downloaded to your local machine

---

## Method 1: Automated Script (Recommended)

```bash
# Navigate to the project directory
cd /path/to/auto-youtube-pipeline

# Run the automated setup script
chmod +x github-setup.sh
./github-setup.sh
```

The script will:
- ✅ Check for security issues
- ✅ Initialize Git repository
- ✅ Create initial commit
- ✅ Guide you through GitHub setup
- ✅ Push code to GitHub
- ✅ Provide next steps

---

## Method 2: Manual Commands

### Step 1: Navigate to Project
```bash
cd /path/to/auto-youtube-pipeline
```

### Step 2: Configure Git User
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize Repository
```bash
# Initialize Git
git init

# Set default branch to main
git branch -M main

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: YouTube automation workflow

Complete end-to-end automated video creation pipeline with:
- AI script generation
- Text-to-speech voiceover
- Stock footage download
- Video composition
- YouTube upload
- GitHub Actions automation"
```

### Step 4: Create GitHub Repository

**Option A: Using GitHub CLI (if installed)**
```bash
# Login to GitHub
gh auth login

# Create and push repository
gh repo create youtube-automation-workflow --public --source=. --remote=origin --push
```

**Option B: Using Web Interface (Manual)**

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `youtube-automation-workflow`
   - **Description**: `End-to-End YouTube Video Upload Workflow - Automated video creation with AI`
   - **Visibility**: Public (or Private)
   - **DO NOT** check "Initialize this repository with..."
3. Click "Create repository"

### Step 5: Push to GitHub (if using Option B)

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation-workflow.git

# Verify remote
git remote -v

# Push code
git push -u origin main
```

If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password)
  - Create token at: https://github.com/settings/tokens
  - Select: `repo` scope
  - Copy token and use as password

---

## Method 3: SSH (Most Secure)

### Setup SSH Key (First Time Only)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Paste the public key
4. Click "Add SSH key"

### Push Using SSH

```bash
# Initialize and commit (same as above)
git init
git branch -M main
git add .
git commit -m "Initial commit: YouTube automation workflow"

# Add remote with SSH (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/youtube-automation-workflow.git

# Push
git push -u origin main
```

---

## Verification Checklist

After pushing, verify:

- [ ] Visit https://github.com/YOUR_USERNAME/youtube-automation-workflow
- [ ] All files are visible
- [ ] README.md displays correctly
- [ ] No `.env` file visible
- [ ] No `client_secrets.json` visible
- [ ] No `token.pickle` visible

---

## Post-Upload Configuration

### 1. Update Repository Settings

Go to: https://github.com/YOUR_USERNAME/youtube-automation-workflow

**About Section** (click ⚙️):
- Description: `End-to-End YouTube Video Upload Workflow - Automated video creation with AI, TTS, and stock footage`
- Topics: `youtube`, `automation`, `ai`, `python`, `video-creation`, `ffmpeg`, `github-actions`
- Website: (your URL if any)

### 2. Enable Features

Go to: Settings → General
- ✅ Issues
- ✅ Discussions (optional)

### 3. Setup GitHub Actions Secrets (Optional)

Go to: Settings → Secrets and variables → Actions

Add these secrets:

**PEXELS_API_KEY**
```
Your Pexels API key from https://www.pexels.com/api/
```

**GROQ_API_KEY** (if using Groq)
```
Your Groq API key from https://console.groq.com
```

**YOUTUBE_CLIENT_SECRETS**
```
# Copy entire contents of config/client_secrets.json
cat config/client_secrets.json
```

**YOUTUBE_TOKEN_PICKLE**
```
# Base64 encode the token file
base64 -w 0 config/token.pickle
# Or on macOS:
base64 -i config/token.pickle
```

---

## Create First Release

```bash
# Tag the release
git tag -a v1.0.0 -m "Initial release: Complete YouTube automation workflow"

# Push tag
git push origin v1.0.0
```

Then on GitHub:
1. Go to: https://github.com/YOUR_USERNAME/youtube-automation-workflow/releases
2. Click "Create a new release"
3. Select tag: v1.0.0
4. Title: `v1.0.0 - Initial Release`
5. Add release notes
6. Click "Publish release"

---

## Troubleshooting

### "Authentication failed"
```bash
# Use Personal Access Token
# Create at: https://github.com/settings/tokens
# Use token as password when prompted
```

### "Permission denied (publickey)"
```bash
# Add SSH key to GitHub
cat ~/.ssh/id_ed25519.pub
# Add at: https://github.com/settings/keys
```

### "Remote already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
```

### "Nothing to commit"
```bash
git status
git add .
git commit -m "Initial commit"
```

---

## Quick Commands Reference

```bash
# Check status
git status

# View changes
git diff

# Commit history
git log --oneline

# Check remote
git remote -v

# Pull latest
git pull origin main

# Push changes
git push origin main
```

---

## Success! 🎉

Your code is now on GitHub!

**Repository URL**: https://github.com/YOUR_USERNAME/youtube-automation-workflow

### Share Your Work
- ⭐ Star your repository
- 🐦 Tweet about it
- 💼 Add to LinkedIn
- 📝 Write a blog post
- 🗣️ Share on Reddit (r/Python, r/selfhosted)

---

## Need Help?

- See: **GITHUB_SETUP.md** for detailed instructions
- See: **TROUBLESHOOTING.md** for common issues
- Check: **GITHUB_CHECKLIST.md** for verification

---

**Congratulations on sharing your project with the world! 🚀**
