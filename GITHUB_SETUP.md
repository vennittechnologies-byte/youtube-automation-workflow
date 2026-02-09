# 📦 GitHub Setup Guide

Complete step-by-step instructions for checking your code into GitHub.

## Prerequisites

- Git installed on your system
- GitHub account created
- Code downloaded and working locally

---

## Step 1: Prepare Your Repository

### Clean Up Sensitive Files

Before pushing to GitHub, ensure sensitive files are ignored:

```bash
# Check .gitignore includes:
cat .gitignore
```

Should contain:
```
.env
config/client_secrets.json
config/token.pickle
*.json
output/
```

### Verify No Secrets in Code

```bash
# Search for any API keys accidentally in code
grep -r "PEXELS_API_KEY" scripts/ --exclude-dir=.git
grep -r "GROQ_API_KEY" scripts/ --exclude-dir=.git

# Should only appear in .env.example (as placeholders)
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Repository settings:
   - **Name:** `youtube-automation-workflow`
   - **Description:** `End-to-End YouTube Video Upload Workflow - Automated video creation and publishing with AI`
   - **Visibility:** Public or Private (your choice)
   - **Initialize:** Don't check any boxes (we already have files)
4. Click "Create repository"

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if needed
# Ubuntu: sudo apt install gh
# macOS: brew install gh

# Login
gh auth login

# Create repository
gh repo create youtube-automation-workflow --public --source=. --remote=origin
```

---

## Step 3: Initialize Git (If Not Already Done)

```bash
# Navigate to project directory
cd /path/to/auto-youtube-pipeline

# Initialize git repository
git init

# Check current status
git status
```

---

## Step 4: Configure Git

```bash
# Set your name and email (if not already set)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Step 5: Prepare the Commit

### Stage Files

```bash
# Add all files
git add .

# Or add selectively
git add scripts/
git add config/topics.json
git add main.py
git add requirements.txt
git add README.md
git add .github/
# ... etc

# Check what's staged
git status
```

### Verify Sensitive Files Are Excluded

```bash
# This should show .env, client_secrets.json, etc. as untracked
git status

# If sensitive files appear in "Changes to be committed":
git reset HEAD path/to/sensitive/file
```

### Create Initial Commit

```bash
git commit -m "Initial commit: Complete YouTube automation workflow

Features:
- AI script generation (Ollama/Groq)
- Text-to-speech voiceover
- Automatic stock footage download
- Thumbnail generation
- Video composition
- YouTube upload
- GitHub Actions automation"
```

---

## Step 6: Connect to GitHub

```bash
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation-workflow.git

# Verify remote
git remote -v
```

### If Using SSH (Recommended)

```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Use SSH remote
git remote set-url origin git@github.com:YOUR_USERNAME/youtube-automation-workflow.git
```

---

## Step 7: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**First push output should look like:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 8 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (45/45), 156.23 KiB | 8.23 MiB/s, done.
Total 45 (delta 12), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Step 8: Verify Upload

### Check GitHub Repository

1. Go to https://github.com/YOUR_USERNAME/youtube-automation-workflow
2. Verify all files are present
3. Check README.md renders correctly
4. Ensure no sensitive files (.env, credentials) are visible

### File Structure Should Look Like:

```
youtube-automation-workflow/
├── .github/
│   └── workflows/
│       └── auto-video.yml
├── scripts/
│   ├── script_generator.py
│   ├── voiceover.py
│   ├── visuals.py
│   ├── thumbnails.py
│   ├── compose.py
│   └── upload.py
├── config/
│   └── topics.json
├── main.py
├── requirements.txt
├── setup.sh
├── .env.example
├── .gitignore
├── README.md
├── QUICKSTART.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── TROUBLESHOOTING.md
├── LICENSE
└── SETUP_SUMMARY.md
```

---

## Step 9: Setup GitHub Actions (Optional)

### Add Repository Secrets

1. Go to repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

Add these secrets:

#### PEXELS_API_KEY
- Name: `PEXELS_API_KEY`
- Value: Your Pexels API key

#### GROQ_API_KEY (if using Groq)
- Name: `GROQ_API_KEY`
- Value: Your Groq API key

#### YOUTUBE_CLIENT_SECRETS
- Name: `YOUTUBE_CLIENT_SECRETS`
- Value: Entire content of `config/client_secrets.json`
```bash
cat config/client_secrets.json
# Copy the output
```

#### YOUTUBE_TOKEN_PICKLE
- Name: `YOUTUBE_TOKEN_PICKLE`
- Value: Base64 encoded token.pickle
```bash
base64 -w 0 config/token.pickle
# Copy the output
```

### Enable GitHub Actions

1. Go to **Actions** tab
2. Enable workflows if prompted
3. Workflows should now be visible

### Test Workflow

1. Go to **Actions** tab
2. Select "Automated YouTube Video Pipeline"
3. Click **Run workflow**
4. Select branch: `main`
5. (Optional) Enter custom topic
6. Click **Run workflow**

Monitor the workflow execution in real-time.

---

## Step 10: Update README with Your Info

### Edit README.md

Replace placeholders:

```bash
# Clone your actual repository
git clone https://github.com/YOUR_USERNAME/youtube-automation-workflow.git

# Update URLs in README.md
sed -i 's/YOUR_USERNAME/YourActualUsername/g' README.md

# Commit changes
git add README.md
git commit -m "Update README with repository URLs"
git push
```

### Add Repository Badges

At the top of README.md, update:
```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/youtube-automation-workflow?style=social)](https://github.com/YOUR_USERNAME/youtube-automation-workflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
```

---

## Step 11: Add Topics and Description

### Set Repository Topics

1. Go to repository main page
2. Click ⚙️ (gear icon) next to "About"
3. Add topics:
   - `youtube`
   - `automation`
   - `video-creation`
   - `ai`
   - `python`
   - `ffmpeg`
   - `text-to-speech`
   - `workflow`
   - `github-actions`
4. Add description:
   > End-to-End YouTube Video Upload Workflow - Automated video creation and publishing with AI, TTS, and stock footage. 100% free tools.
5. Add website (if you have one)
6. Click "Save changes"

---

## Step 12: Create Releases (Optional)

### Create First Release

```bash
# Tag the current commit
git tag -a v1.0.0 -m "Initial release: Complete YouTube automation workflow"

# Push tags
git push origin v1.0.0
```

### Create Release on GitHub

1. Go to repository → **Releases**
2. Click **Create a new release**
3. Select tag: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
```markdown
## 🚀 Initial Release

Complete YouTube video automation workflow with:

### Features
- ✅ AI script generation (Ollama/Groq)
- ✅ Text-to-speech voiceover (20+ voices)
- ✅ Automatic stock footage download
- ✅ Thumbnail generation
- ✅ Video composition with FFmpeg
- ✅ YouTube upload automation
- ✅ GitHub Actions scheduling
- ✅ 100% free tools

### What's Included
- Complete pipeline scripts
- GitHub Actions workflow
- Comprehensive documentation
- Setup wizard

### Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
cd youtube-automation-workflow
./setup.sh
```

See [README.md](README.md) for full documentation.
```

6. Click **Publish release**

---

## Step 13: Future Updates

### Making Changes

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ...

# Commit changes
git add .
git commit -m "Add new feature: description"

# Push branch
git push origin feature/new-feature

# Create Pull Request on GitHub
```

### Regular Updates

```bash
# Pull latest changes
git pull origin main

# Make changes
# ...

# Commit and push
git add .
git commit -m "Update: description"
git push origin main
```

---

## Common Git Commands

```bash
# Check status
git status

# View changes
git diff

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo changes to file
git checkout -- filename

# Create new branch
git checkout -b branch-name

# Switch branch
git checkout branch-name

# Merge branch
git merge branch-name

# Delete branch
git branch -d branch-name

# Pull latest changes
git pull origin main

# Push changes
git push origin main
```

---

## Security Checklist

Before making repository public:

- [ ] No API keys in code
- [ ] No passwords in code  
- [ ] .env in .gitignore
- [ ] client_secrets.json in .gitignore
- [ ] token.pickle in .gitignore
- [ ] output/ directory in .gitignore
- [ ] README.md has placeholders (YOUR_USERNAME)
- [ ] No personal information in commits
- [ ] LICENSE file included
- [ ] CONTRIBUTING.md included

---

## Repository Settings

### Recommended Settings

1. **General**
   - ✅ Allow merge commits
   - ✅ Allow squash merging
   - ✅ Allow rebase merging
   - ✅ Automatically delete head branches

2. **Branches**
   - Add branch protection for `main`:
     - ✅ Require pull request reviews
     - ✅ Require status checks to pass

3. **Actions**
   - ✅ Allow all actions and reusable workflows
   - Set workflow permissions

---

## Troubleshooting Git Issues

### "fatal: remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
```

### "Permission denied (publickey)"

```bash
# Add SSH key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to GitHub Settings → SSH Keys
```

### "The requested URL returned error: 403"

```bash
# Use personal access token or SSH
git remote set-url origin git@github.com:YOUR_USERNAME/youtube-automation-workflow.git
```

### "fatal: refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

---

## Next Steps

1. ✅ Share repository link with others
2. ✅ Add to your GitHub profile
3. ✅ Write blog post about the project
4. ✅ Submit to awesome lists
5. ✅ Monitor issues and discussions

---

## Congratulations! 🎉

Your code is now on GitHub and ready to share with the world!

**Repository URL:** https://github.com/YOUR_USERNAME/youtube-automation-workflow

Share it:
- Twitter/X
- LinkedIn  
- Reddit (r/Python, r/selfhosted)
- Dev.to
- Hacker News (Show HN)
