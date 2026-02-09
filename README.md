# 🎬 End-to-End YouTube Video Upload Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A fully automated, **100% free** end-to-end pipeline for creating and publishing YouTube videos using AI and open-source tools.

## ✨ Features

- 🤖 **AI Script Generation** - Powered by Ollama (local) or Groq (cloud API)
- 🎙️ **Natural Text-to-Speech** - Microsoft Edge-TTS with 20+ voices
- 📹 **Automatic Stock Footage** - Downloads from Pexels API
- 🎨 **Thumbnail Generation** - Professional thumbnails with Pillow
- 🎬 **Video Composition** - FFmpeg + MoviePy editing
- 📤 **YouTube Upload** - Automated publishing with OAuth
- ⏰ **Scheduling** - GitHub Actions automation
- 💰 **Zero Cost** - All tools and APIs are completely free

## 🎥 Demo

```bash
# Run the full pipeline
python main.py

# Output: A complete YouTube video in 3-8 minutes!
```

**What gets created:**
- ✅ AI-generated 60-second script
- ✅ Professional voiceover
- ✅ HD stock footage (1080p)
- ✅ Custom thumbnail
- ✅ Edited and published video

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- FFmpeg
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
cd youtube-automation-workflow

# Run the automated setup
chmod +x setup.sh
./setup.sh
```

Or install manually:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS

# Copy environment template
cp .env.example .env

# Add your API keys to .env
nano .env
```

### Configuration

Get your free API keys:

1. **Pexels API** (Required): https://www.pexels.com/api/
2. **Groq API** (Optional): https://console.groq.com
3. **YouTube OAuth** (For uploads): See [YouTube Setup Guide](#youtube-setup)

Add to `.env`:
```bash
PEXELS_API_KEY=your_pexels_api_key
GROQ_API_KEY=your_groq_api_key  # If not using Ollama
```

### Usage

```bash
# Generate video without uploading
python main.py --no-upload

# Full pipeline with YouTube upload
python main.py

# Specify custom topic
python main.py --topic "Climate Change Solutions"

# Run individual components
python scripts/script_generator.py
python scripts/voiceover.py
python scripts/visuals.py
python scripts/compose.py
python scripts/upload.py
```

## 📁 Project Structure

```
youtube-automation-workflow/
├── scripts/
│   ├── script_generator.py    # AI script generation
│   ├── voiceover.py           # Text-to-speech
│   ├── visuals.py             # Stock footage fetcher
│   ├── thumbnails.py          # Thumbnail generator
│   ├── compose.py             # Video composition
│   └── upload.py              # YouTube uploader
├── config/
│   └── topics.json            # Content topics
├── .github/workflows/
│   └── auto-video.yml         # GitHub Actions
├── main.py                    # Pipeline orchestrator
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Configuration

### Topics Configuration

Edit `config/topics.json` to customize your video topics:

```json
{
  "topics": [
    {
      "title": "AI Revolution in 2025",
      "keywords": ["AI", "technology", "future"],
      "description": "Exploring the latest AI breakthroughs",
      "visual_queries": ["artificial intelligence", "robots", "technology"]
    }
  ]
}
```

### Environment Variables

Available settings in `.env`:

```bash
# API Keys
PEXELS_API_KEY=your_key
GROQ_API_KEY=your_key

# LLM Settings
USE_OLLAMA=true              # Use local Ollama
OLLAMA_MODEL=llama3.1:8b
GROQ_MODEL=llama-3.1-8b-instant

# TTS Voice
TTS_VOICE=en-US-JennyNeural  # See voice options below

# Video Settings
VIDEO_WIDTH=1920
VIDEO_HEIGHT=1080
VIDEO_FPS=30

# YouTube
YOUTUBE_PRIVACY_STATUS=public  # public, private, unlisted
```

### Available TTS Voices

- `en-US-JennyNeural` - Friendly female (default)
- `en-US-GuyNeural` - Professional male
- `en-GB-SoniaNeural` - British female
- `en-AU-NatashaNeural` - Australian female
- And many more...

## 📺 YouTube Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable "YouTube Data API v3"

### Step 2: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Application type: **Desktop app**
4. Download JSON file

### Step 3: Save Credentials

```bash
# Save the downloaded file as:
config/client_secrets.json
```

### Step 4: First-time Authentication

```bash
# Run the upload script
python scripts/upload.py

# A browser will open for authentication
# Grant permissions
# Token saved to config/token.pickle for future use
```

## 🤖 GitHub Actions Automation

### Setup

1. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
git push -u origin main
```

2. **Add Repository Secrets**

Go to Settings → Secrets and variables → Actions, add:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `GROQ_API_KEY` | Groq API key | [console.groq.com](https://console.groq.com) |
| `PEXELS_API_KEY` | Pexels API key | [pexels.com/api](https://www.pexels.com/api/) |
| `YOUTUBE_CLIENT_SECRETS` | OAuth credentials | Copy content of `client_secrets.json` |
| `YOUTUBE_TOKEN_PICKLE` | Refresh token | `base64 config/token.pickle` |

3. **Configure Schedule**

Edit `.github/workflows/auto-video.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

### Manual Trigger

1. Go to Actions tab
2. Select "Automated YouTube Video Pipeline"
3. Click "Run workflow"

## 💰 Cost Breakdown

| Component | Tool | Cost |
|-----------|------|------|
| Script Generation | Ollama/Groq | $0 |
| Text-to-Speech | Edge-TTS | $0 |
| Stock Footage | Pexels API | $0 |
| Video Editing | FFmpeg/MoviePy | $0 |
| Thumbnails | Pillow | $0 |
| YouTube Upload | YouTube Data API | $0 |
| Automation | GitHub Actions | $0 |
| **Total** | | **$0/month** |

**Free Tier Limits:**
- Pexels: 200 requests/hour
- YouTube: 10,000 quota units/day (~100 uploads)
- GitHub Actions: 2,000 minutes/month
- Groq: Very generous limits

## 📊 Pipeline Performance

- **Average Pipeline Time**: 3-8 minutes per video
- **Video Quality**: 1080p HD, 30 FPS
- **Audio Quality**: High-fidelity TTS
- **File Size**: ~20-50 MB per video

## 🛠️ Advanced Usage

### Custom Script Templates

Edit `scripts/script_generator.py` to customize the script format:

```python
prompt = f"""Create a {duration}-second YouTube script about: {topic}

Your custom instructions here...
"""
```

### Video Transitions

Modify `scripts/compose.py` to add custom transitions:

```python
clip = clip.fx(fadein, transition_duration)
clip = clip.fx(fadeout, transition_duration)
```

### Thumbnail Customization

Edit `scripts/thumbnails.py` to change colors, fonts, and layout:

```python
background_color = (20, 25, 35)
text_color = (255, 255, 255)
accent_color = (249, 115, 22)
```

## 🔍 Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"FFmpeg not found"**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

**"PEXELS_API_KEY not found"**
- Ensure `.env` file exists in project root
- Verify API key is correct
- No quotes around the key value

**"YouTube authentication failed"**
- Delete `config/token.pickle`
- Run `python scripts/upload.py` again
- Complete OAuth flow in browser

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - 10-minute setup
- [Architecture Overview](ARCHITECTURE.md) - Technical details
- [Setup Summary](SETUP_SUMMARY.md) - Complete overview
- [API Documentation](docs/API.md) - Component APIs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Groq](https://groq.com/) - Fast LLM API
- [Pexels](https://www.pexels.com/) - Free stock footage
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Edge-TTS](https://github.com/rany2/edge-tts) - Text-to-speech
- [YouTube Data API](https://developers.google.com/youtube/v3) - Video uploads

## ⭐ Support

If you find this project helpful, please consider giving it a star on GitHub!

## 📧 Contact

- GitHub Issues: [Create an issue](https://github.com/YOUR_USERNAME/youtube-automation-workflow/issues)
- Discussions: [Join the discussion](https://github.com/YOUR_USERNAME/youtube-automation-workflow/discussions)

---

**Made with ❤️ using 100% free and open-source tools**

[![Star on GitHub](https://img.shields.io/github/stars/YOUR_USERNAME/youtube-automation-workflow?style=social)](https://github.com/YOUR_USERNAME/youtube-automation-workflow)
