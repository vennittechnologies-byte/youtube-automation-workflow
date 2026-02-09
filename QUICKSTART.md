# 🚀 Quick Start Guide

Get your automated YouTube pipeline running in **under 10 minutes**!

## ⚡ Super Fast Setup

### 1. Install Dependencies (2 minutes)

```bash
# Install system dependencies
sudo apt install ffmpeg  # Ubuntu/Debian
# OR
brew install ffmpeg      # macOS

# Install Python packages
pip install -r requirements.txt
```

### 2. Get API Keys (3 minutes)

#### Pexels (Required - 1 minute)
1. Go to https://www.pexels.com/api/
2. Click "Get Started"
3. Copy your API key
4. Save for step 3

#### Groq (Optional but Recommended - 2 minutes)
1. Go to https://console.groq.com
2. Sign up with Google/GitHub
3. Create API key
4. Save for step 3

### 3. Configure Environment (1 minute)

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys:
nano .env
```

Add these lines:
```bash
PEXELS_API_KEY=your_pexels_key_here
GROQ_API_KEY=your_groq_key_here
USE_OLLAMA=false
```

### 4. Run Your First Video! (4 minutes)

```bash
# Create video (without uploading to YouTube)
python main.py --no-upload
```

Your video will be saved in `output/videos/`!

---

## 📺 YouTube Upload Setup (Optional)

### Get YouTube Credentials (5 minutes)

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Click "New Project" → Name it → Create

2. **Enable YouTube API**
   - Go to "APIs & Services" → "Library"
   - Search "YouTube Data API v3"
   - Click "Enable"

3. **Create OAuth Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - If prompted, configure consent screen:
     - User Type: External
     - App name: Your app name
     - Add your email
     - Add test users (your email)
   - Application type: **Desktop app**
   - Download JSON file

4. **Save Credentials**
   ```bash
   # Save the downloaded file as:
   config/client_secrets.json
   ```

5. **Authenticate**
   ```bash
   # Run upload script (browser will open for auth)
   python scripts/upload.py
   ```
   - Log in to your YouTube account
   - Click "Allow"
   - Done! Token saved for future use

---

## 🎯 Common Commands

```bash
# Full pipeline with YouTube upload
python main.py

# Create video without uploading
python main.py --no-upload

# Custom topic
python main.py --topic "Space Exploration"

# Run individual steps
python scripts/script_generator.py
python scripts/voiceover.py
python scripts/visuals.py
python scripts/compose.py
python scripts/upload.py
```

---

## 🔧 Quick Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### "PEXELS_API_KEY not found"
1. Check `.env` file exists
2. Verify key is on the line: `PEXELS_API_KEY=your_key`
3. No quotes around the key

### "Failed to generate voiceover"
```bash
# Edge-TTS might need updating
pip install --upgrade edge-tts
```

---

## 📊 What Gets Created

After running `python main.py --no-upload`:

```
output/
├── script.json              # Generated script
├── audio/
│   └── voiceover.mp3       # Generated voiceover
├── clips/
│   ├── clip_0_0.mp4        # Downloaded stock footage
│   └── clip_0_1.mp4
├── thumbnails/
│   └── thumbnail.jpg       # Generated thumbnail
└── videos/
    └── final_video.mp4     # YOUR FINAL VIDEO! 🎉
```

---

## 🎥 Video Specifications

- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS
- **Format**: MP4 (H.264 + AAC)
- **Duration**: ~60 seconds (based on script)
- **File Size**: ~20-50 MB

---

## ⏭️ Next Steps

1. ✅ Test with `--no-upload` first
2. ✅ Review generated video
3. ✅ Setup YouTube OAuth
4. ✅ Run full pipeline with upload
5. ✅ Configure GitHub Actions for automation

---

## 💡 Pro Tips

**Better Quality Videos:**
- Add more visual queries in `config/topics.json`
- Use higher quality voice (try different `TTS_VOICE` values)
- Increase video bitrate in `compose.py`

**Faster Processing:**
- Use local Ollama instead of Groq
- Reduce video resolution in `.env`
- Use fewer video clips

**More Engagement:**
- Write better hooks in script prompts
- Use trending topics
- Add relevant tags

---

## 📚 Full Documentation

For complete setup instructions, see [README.md](README.md)

---

**Total Time to First Video: ~10 minutes** ⚡

Questions? Check the [Troubleshooting](README.md#troubleshooting) section!
