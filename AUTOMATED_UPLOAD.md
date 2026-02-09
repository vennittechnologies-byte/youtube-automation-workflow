# 🚀 Automated GitHub Upload Instructions

## One-Command Upload

Run this single command to automatically upload everything to your GitHub repository:

```bash
cd auto-youtube-pipeline
python3 upload_to_github.py
```

## What You'll Need

1. **GitHub Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Give it a name: "YouTube Workflow Upload"
   - Select scopes:
     - ✅ `repo` (all checkboxes)
     - ✅ `workflow`
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

## What the Script Does

The automated script will:
1. ✅ Create repository `vennittechnologies-byte/youtube-automation-workflow`
2. ✅ Respect `.gitignore` (won't upload sensitive files)
3. ✅ Upload all project files automatically
4. ✅ Maintain directory structure
5. ✅ Skip `.env`, credentials, and other sensitive files
6. ✅ Provide upload statistics

## Process

```
Step 1: Script asks for GitHub token
        → Paste your token

Step 2: Script confirms configuration
        → Press Enter to proceed

Step 3: Script creates repository

Step 4: Script uploads all files
        → Shows progress for each file

Step 5: Complete!
        → Shows repository URL
```

## Expected Output

```
🚀 Automated GitHub Upload
📦 YouTube Automation Workflow

🔑 GitHub Personal Access Token Required
Enter your GitHub Personal Access Token: [paste token]

📋 Configuration:
   Username: vennittechnologies-byte
   Repository: youtube-automation-workflow

Proceed with upload? (Y/n): y

🔨 Creating repository: vennittechnologies-byte/youtube-automation-workflow
✅ Repository created successfully!

📤 Uploading files...
📤 Uploading: README.md
📤 Uploading: main.py
📤 Uploading: requirements.txt
... (continues for all files)

✅ Upload Complete!

📊 Statistics:
   ✅ Uploaded: 45 files
   ❌ Failed: 0 files
   ⏭️  Skipped: 8 files

🔗 Repository URL:
   https://github.com/vennittechnologies-byte/youtube-automation-workflow
```

## After Upload

Visit your repository:
```
https://github.com/vennittechnologies-byte/youtube-automation-workflow
```

Configure repository settings:
1. Add description
2. Add topics: `youtube`, `automation`, `ai`, `python`
3. Enable Issues and Discussions

## Troubleshooting

**"requests module not found"**
```bash
pip install requests
```

**"Authentication failed"**
- Verify token is correct
- Check token has `repo` scope
- Generate new token if needed

**"Repository already exists"**
- Script will update existing repository
- No need to delete manually

## Security

The script automatically:
- ✅ Skips `.env` files
- ✅ Skips `client_secrets.json`
- ✅ Skips `token.pickle`
- ✅ Respects all `.gitignore` patterns
- ✅ Never uploads sensitive data

## That's It!

Just run:
```bash
python3 upload_to_github.py
```

And your code will be on GitHub in minutes! 🎉
