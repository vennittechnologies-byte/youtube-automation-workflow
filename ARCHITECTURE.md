# 📁 Project Structure Overview

Complete file-by-file explanation of the automated YouTube pipeline.

## Directory Structure

```
auto-youtube-pipeline/
├── .github/
│   └── workflows/
│       └── auto-video.yml          # GitHub Actions automation
├── config/
│   ├── topics.json                 # Content topics and rotation
│   ├── client_secrets.json         # YouTube OAuth (gitignored)
│   └── token.pickle               # YouTube refresh token (gitignored)
├── scripts/
│   ├── script_generator.py        # LLM script generation
│   ├── voiceover.py               # Text-to-speech conversion
│   ├── visuals.py                 # Stock footage downloader
│   ├── thumbnails.py              # Thumbnail generator
│   ├── compose.py                 # Video composition
│   └── upload.py                  # YouTube uploader
├── output/                        # All generated content (gitignored)
│   ├── videos/                    # Final rendered videos
│   ├── audio/                     # Generated voiceovers
│   ├── clips/                     # Downloaded stock footage
│   └── thumbnails/                # Generated thumbnails
├── main.py                        # Pipeline orchestrator
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── setup.sh                      # Automated setup script
├── README.md                     # Full documentation
└── QUICKSTART.md                 # Quick start guide
```

---

## Core Files Explained

### 📝 Configuration Files

#### `.env` (Your Settings)
Contains all your API keys and configuration:
```bash
PEXELS_API_KEY=...           # Stock footage API
GROQ_API_KEY=...             # LLM API (optional)
USE_OLLAMA=true              # Use local LLM
TTS_VOICE=en-US-JennyNeural  # Voice selection
VIDEO_WIDTH=1920             # Video resolution
YOUTUBE_PRIVACY_STATUS=public # Upload privacy
```

#### `config/topics.json` (Content Calendar)
Defines your video topics and rotates through them:
```json
{
  "topics": [
    {
      "title": "AI Revolution",
      "keywords": ["AI", "technology"],
      "visual_queries": ["robots", "technology"]
    }
  ],
  "last_used_index": 0
}
```

#### `requirements.txt` (Dependencies)
Lists all Python packages needed:
- `moviepy` - Video editing
- `edge-tts` - Text-to-speech
- `google-api-python-client` - YouTube API
- `Pillow` - Image/thumbnail creation
- And more...

---

### 🤖 Pipeline Scripts

#### `scripts/script_generator.py`
**Purpose**: Generate video scripts using AI

**What it does**:
1. Takes a topic as input
2. Calls Ollama (local) or Groq (cloud) LLM
3. Generates a 60-second YouTube script with:
   - Catchy hook (5 seconds)
   - Main content (45 seconds)
   - Call-to-action (10 seconds)
4. Outputs: `output/script.json`

**Key Functions**:
- `generate_script(topic)` - Main generation function
- `_generate_with_ollama()` - Local LLM
- `_generate_with_groq()` - Cloud API

#### `scripts/voiceover.py`
**Purpose**: Convert script text to natural speech

**What it does**:
1. Reads `output/script.json`
2. Uses Microsoft Edge-TTS (free, unlimited)
3. Generates MP3 audio file
4. Outputs: `output/audio/voiceover.mp3`

**Voice Options**:
- `en-US-JennyNeural` - Friendly female (default)
- `en-US-GuyNeural` - Professional male
- `en-GB-SoniaNeural` - British female
- Many more...

#### `scripts/visuals.py`
**Purpose**: Download stock video footage

**What it does**:
1. Reads visual queries from `config/topics.json`
2. Searches Pexels API for matching videos
3. Downloads 2-3 clips per query
4. Outputs: `output/clips/clip_*.mp4`

**Features**:
- Free API (200 requests/hour)
- Automatic quality selection
- Rate limiting to be nice to API

#### `scripts/thumbnails.py`
**Purpose**: Create eye-catching YouTube thumbnails

**What it does**:
1. Reads video title from script
2. Creates 1280x720 image
3. Adds gradient background
4. Overlays title text with nice formatting
5. Outputs: `output/thumbnails/thumbnail.jpg`

**Customization**:
- Background colors
- Text colors
- Font sizes
- Accent bars

#### `scripts/compose.py`
**Purpose**: Combine everything into final video

**What it does**:
1. Loads all video clips
2. Loads audio voiceover
3. Resizes clips to 1920x1080
4. Adds fade transitions
5. Matches video length to audio
6. Exports final MP4
7. Outputs: `output/videos/final_video.mp4`

**Processing**:
- H.264 codec (universal compatibility)
- AAC audio codec
- 30 FPS frame rate
- CRF 23 quality (balanced)

#### `scripts/upload.py`
**Purpose**: Upload video to YouTube

**What it does**:
1. Authenticates with YouTube API
2. Reads video and metadata
3. Uploads video with:
   - Title
   - Description
   - Tags
   - Thumbnail
   - Privacy settings
4. Returns video URL

**Authentication**:
- OAuth 2.0 flow
- Token saved to `config/token.pickle`
- Refresh token for automation

---

### 🎯 Main Orchestrator

#### `main.py`
**Purpose**: Run the complete pipeline

**What it does**:
1. Runs all 6 stages in order:
   - Script generation
   - Voiceover creation
   - Visual download
   - Thumbnail creation
   - Video composition
   - YouTube upload
2. Handles errors gracefully
3. Saves results to `output/pipeline_results.json`

**Usage**:
```bash
python main.py                    # Full pipeline
python main.py --no-upload        # Skip YouTube
python main.py --topic "AI"       # Custom topic
```

---

### ⚙️ Automation

#### `.github/workflows/auto-video.yml`
**Purpose**: GitHub Actions automation

**What it does**:
1. Runs on schedule (e.g., every Monday)
2. Sets up Ubuntu environment
3. Installs dependencies
4. Runs pipeline
5. Uploads video to YouTube
6. Saves artifacts

**Triggers**:
- Scheduled cron jobs
- Manual workflow dispatch
- Custom topics via input

**Required Secrets**:
- `GROQ_API_KEY`
- `PEXELS_API_KEY`
- `YOUTUBE_CLIENT_SECRETS`
- `YOUTUBE_TOKEN_PICKLE`

---

### 🛠️ Setup & Documentation

#### `setup.sh`
**Purpose**: Interactive setup wizard

**What it does**:
1. Checks system requirements
2. Installs dependencies
3. Creates `.env` file
4. Helps setup Ollama/Groq
5. Guides YouTube OAuth setup
6. Runs basic tests

**Usage**:
```bash
chmod +x setup.sh
./setup.sh
```

#### `README.md`
Complete documentation with:
- Full setup instructions
- API key setup guides
- Configuration options
- Troubleshooting
- GitHub Actions setup

#### `QUICKSTART.md`
Minimal 10-minute setup guide for impatient users!

---

## 📊 Data Flow

```
1. Topic Selection
   ↓
   config/topics.json → main.py

2. Script Generation
   ↓
   Ollama/Groq → output/script.json

3. Voiceover
   ↓
   Edge-TTS → output/audio/voiceover.mp3

4. Visuals
   ↓
   Pexels API → output/clips/*.mp4

5. Thumbnail
   ↓
   Pillow → output/thumbnails/thumbnail.jpg

6. Video Composition
   ↓
   MoviePy + FFmpeg → output/videos/final_video.mp4

7. YouTube Upload
   ↓
   YouTube API → Video URL
```

---

## 🔄 Pipeline Stages

### Stage 1: Script Generation
- **Input**: Topic string
- **Process**: LLM generation
- **Output**: `script.json` (title, script, tags)
- **Duration**: 10-30 seconds

### Stage 2: Voiceover
- **Input**: `script.json`
- **Process**: Edge-TTS synthesis
- **Output**: `voiceover.mp3`
- **Duration**: 5-15 seconds

### Stage 3: Visuals
- **Input**: Visual queries
- **Process**: Pexels API search + download
- **Output**: Multiple `clip_*.mp4` files
- **Duration**: 30-60 seconds

### Stage 4: Thumbnail
- **Input**: Video title
- **Process**: Image composition
- **Output**: `thumbnail.jpg`
- **Duration**: 1-2 seconds

### Stage 5: Composition
- **Input**: Clips + audio
- **Process**: Video editing + encoding
- **Output**: `final_video.mp4`
- **Duration**: 1-3 minutes

### Stage 6: Upload
- **Input**: Final video + metadata
- **Process**: YouTube API upload
- **Output**: Video URL
- **Duration**: 1-5 minutes

**Total Pipeline Time**: 3-8 minutes (depending on video length)

---

## 🎛️ Customization Points

### Easy to Customize:
- Video topics (`config/topics.json`)
- TTS voice (`.env`)
- Video resolution (`.env`)
- Upload schedule (`.github/workflows/auto-video.yml`)

### Moderate Customization:
- Script format (`scripts/script_generator.py`)
- Thumbnail design (`scripts/thumbnails.py`)
- Video transitions (`scripts/compose.py`)

### Advanced Customization:
- Add subtitles (Whisper integration)
- Multiple voices (dialogue)
- Custom video effects
- AI-generated images (Stable Diffusion)

---

## 💾 Storage Requirements

### Per Video:
- Script: ~1 KB
- Audio: ~1 MB
- Video clips: ~50-100 MB
- Thumbnail: ~200 KB
- Final video: ~20-50 MB

**Total per video**: ~70-150 MB

### With 100 Videos:
- ~7-15 GB storage
- Easily managed with periodic cleanup

---

## 🔐 Security Considerations

### Sensitive Files (gitignored):
- `.env` - API keys
- `config/client_secrets.json` - OAuth client
- `config/token.pickle` - Refresh token
- `output/*` - Generated content

### GitHub Secrets:
All sensitive data stored as encrypted secrets:
- API keys
- OAuth credentials
- Refresh tokens

### Best Practices:
1. Never commit `.env` or credentials
2. Use environment-specific secrets
3. Rotate API keys periodically
4. Review OAuth permissions

---

## 🚀 Performance Optimization

### Speed Improvements:
1. Use local Ollama (faster than API calls)
2. Pre-download stock footage library
3. Reduce video resolution
4. Use faster encoding presets

### Quality Improvements:
1. Use higher CRF values
2. Increase video bitrate
3. Use better TTS voices
4. Manual script editing

### Resource Usage:
- CPU: High during video encoding
- RAM: 2-4 GB during composition
- Disk: ~100 MB per video
- Network: ~100 MB download per video

---

## 📈 Scaling Considerations

### Single Machine:
- 10-20 videos/day comfortably
- Limited by API rate limits

### Multiple Machines:
- Use different Pexels API keys
- Separate YouTube channels
- Parallel processing

### Cloud Deployment:
- GitHub Actions: 2,000 min/month free
- Oracle Cloud: Free VM tier
- AWS Lambda: Serverless options

---

This structure is designed to be:
- ✅ Modular (each component independent)
- ✅ Testable (run stages individually)
- ✅ Maintainable (clear separation of concerns)
- ✅ Extensible (easy to add features)
- ✅ Production-ready (error handling, logging)
