# 🔧 Troubleshooting Guide

Common issues and their solutions for the YouTube Automation Workflow.

## Table of Contents

- [Installation Issues](#installation-issues)
- [API Key Issues](#api-key-issues)
- [Script Generation Issues](#script-generation-issues)
- [Voiceover Issues](#voiceover-issues)
- [Video Composition Issues](#video-composition-issues)
- [YouTube Upload Issues](#youtube-upload-issues)
- [GitHub Actions Issues](#github-actions-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### "Python not found" or "Command not found: python3"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip

# macOS
brew install python@3.11

# Windows
# Download from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation
```

### "FFmpeg not found"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Extract and add to PATH, or use:
choco install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### "ModuleNotFoundError: No module named 'moviepy'"

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install moviepy specifically
pip install moviepy

# If still failing, try upgrading pip
pip install --upgrade pip
pip install -r requirements.txt
```

### "Permission denied" when running setup.sh

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

---

## API Key Issues

### "PEXELS_API_KEY not found"

**Checklist:**
1. `.env` file exists in project root
2. File contains: `PEXELS_API_KEY=your_actual_key`
3. No quotes around the key
4. No spaces around the `=`

**Correct format:**
```bash
PEXELS_API_KEY=abcd1234efgh5678
```

**Incorrect formats:**
```bash
PEXELS_API_KEY="abcd1234"  # ❌ Don't use quotes
PEXELS_API_KEY = abcd1234  # ❌ No spaces around =
```

**Verify .env is being loaded:**
```python
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('PEXELS_API_KEY'))"
```

### "Invalid Pexels API key"

**Solutions:**
1. Verify key at https://www.pexels.com/api/
2. Generate new key if needed
3. Check for typos
4. Ensure no extra characters (spaces, newlines)

### "Groq API rate limit exceeded"

**Solutions:**
1. Switch to local Ollama: `USE_OLLAMA=true` in `.env`
2. Wait for rate limit to reset
3. Use multiple API keys with rotation

---

## Script Generation Issues

### "Ollama not found" or "Ollama connection failed"

**Solutions:**

1. **Install Ollama:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **Start Ollama service:**
```bash
ollama serve
```

3. **Pull the model:**
```bash
ollama pull llama3.1:8b
```

4. **Verify it's running:**
```bash
ollama list
ollama run llama3.1:8b "Hello"
```

5. **Alternative - Use Groq instead:**
```bash
# In .env
USE_OLLAMA=false
GROQ_API_KEY=your_groq_key
```

### "Script generation timeout"

**Solutions:**
1. Increase timeout in script_generator.py
2. Use faster model (Groq API is faster than local)
3. Simplify the prompt
4. Check internet connection (for Groq)

### "Generated script is too short/long"

**Solution:**
Adjust the prompt in `scripts/script_generator.py`:
```python
# Increase target length
words_estimate = duration * 3  # More words per second

# Add length requirements to prompt
prompt = f"""Create exactly {words_estimate} words...
"""
```

---

## Voiceover Issues

### "edge-tts connection error"

**Solutions:**
1. Check internet connection (Edge-TTS requires internet)
2. Update edge-tts: `pip install --upgrade edge-tts`
3. Try different voice
4. Check if Microsoft servers are down

### "Voiceover sounds robotic"

**Solutions:**
1. Try different voices in `.env`:
```bash
TTS_VOICE=en-US-AriaNeural  # More natural
TTS_VOICE=en-GB-SoniaNeural  # British accent
```

2. Adjust rate/pitch in `scripts/voiceover.py`:
```python
await generator.generate_voiceover(
    text=text,
    rate="-5%",  # Slower
    pitch="+2Hz"  # Slightly higher
)
```

### "Audio file not generated"

**Checklist:**
1. Script file exists: `output/script.json`
2. Script contains text
3. Permissions for output directory
4. Disk space available

**Debug:**
```bash
python -c "import asyncio; from scripts.voiceover import VoiceoverGenerator; v = VoiceoverGenerator(); asyncio.run(v.generate_voiceover('Test', 'test.mp3'))"
```

---

## Video Composition Issues

### "MoviePy encoding error"

**Solutions:**

1. **Reinstall moviepy:**
```bash
pip uninstall moviepy imageio-ffmpeg
pip install moviepy==1.0.3
```

2. **Check FFmpeg:**
```bash
ffmpeg -version
which ffmpeg  # Ensure it's in PATH
```

3. **Try different codec:**
```python
# In compose.py, change:
codec='libx264'  # to
codec='mpeg4'
```

### "Video clips not found"

**Checklist:**
1. Run `python scripts/visuals.py` first
2. Check `output/clips/` directory exists
3. Verify Pexels API downloaded files
4. Check disk space

### "Video is too short/long"

**Solution:**
The video automatically matches audio length. To fix:
1. Adjust script length
2. Modify speech rate in voiceover.py
3. Add more video clips

### "Poor video quality"

**Solutions:**

1. **Increase quality in compose.py:**
```python
final_video.write_videofile(
    output_path,
    fps=60,  # Higher FPS
    codec='libx264',
    ffmpeg_params=['-crf', '18']  # Lower CRF = better quality
)
```

2. **Use higher resolution:**
```bash
# In .env
VIDEO_WIDTH=2560
VIDEO_HEIGHT=1440  # 1440p
```

### "Video encoding is very slow"

**Solutions:**

1. **Use faster preset:**
```python
# In compose.py
preset='ultrafast'  # Instead of 'medium'
```

2. **Lower resolution:**
```bash
# In .env
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720  # 720p
```

3. **Reduce FPS:**
```bash
VIDEO_FPS=24  # Instead of 30
```

---

## YouTube Upload Issues

### "YouTube authentication failed"

**Solutions:**

1. **Delete old token:**
```bash
rm config/token.pickle
```

2. **Run authentication again:**
```bash
python scripts/upload.py
```

3. **Check OAuth setup:**
   - Consent screen configured
   - OAuth app not in testing mode
   - Correct redirect URIs

4. **Verify client_secrets.json:**
   - File exists in `config/`
   - Valid JSON format
   - Contains client_id and client_secret

### "OAuth consent screen error"

**Solutions:**

1. **Configure consent screen:**
   - Go to Google Cloud Console
   - APIs & Services → OAuth consent screen
   - Add test users (your email)
   - Publish app (if ready)

2. **Add required scopes:**
   - YouTube Data API v3 scope should be included
   - https://www.googleapis.com/auth/youtube.upload

### "YouTube quota exceeded"

**Details:**
- Daily limit: 10,000 quota units
- Each upload: ~1,600 units
- Max ~6 uploads per day

**Solutions:**
1. Wait for quota reset (daily at midnight Pacific Time)
2. Request quota increase from Google
3. Use multiple channels with different projects

### "Upload succeeds but video not visible"

**Check:**
1. Privacy status setting (public vs private)
2. YouTube channel verification status
3. Video processing time (can take hours)
4. Copyright claims or restrictions

---

## GitHub Actions Issues

### "Secrets not found in GitHub Actions"

**Solutions:**

1. **Verify secrets are added:**
   - Go to Settings → Secrets and variables → Actions
   - Check all required secrets exist

2. **Correct secret names:**
   - `GROQ_API_KEY`
   - `PEXELS_API_KEY`
   - `YOUTUBE_CLIENT_SECRETS`
   - `YOUTUBE_TOKEN_PICKLE`

### "GitHub Actions workflow not running"

**Solutions:**

1. **Check workflow is enabled:**
   - Go to Actions tab
   - Enable workflows if disabled

2. **Verify cron schedule:**
```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Correct format
```

3. **Trigger manually:**
   - Actions → Workflow → Run workflow

### "Workflow fails on FFmpeg installation"

**Solution:**
Add to workflow:
```yaml
- name: Install FFmpeg
  run: |
    sudo apt-get update
    sudo apt-get install -y ffmpeg
```

### "Token.pickle encoding error in GitHub Actions"

**Solutions:**

1. **Re-encode token:**
```bash
# Make sure no newlines
base64 -w 0 config/token.pickle
```

2. **Verify secret:**
   - Copy exact output
   - Paste into GitHub secret
   - No extra spaces or newlines

---

## Performance Issues

### "Pipeline is very slow"

**Optimization strategies:**

1. **Use local Ollama instead of Groq:**
```bash
USE_OLLAMA=true
```

2. **Reduce video resolution:**
```bash
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720
```

3. **Use faster encoding:**
```python
preset='ultrafast'
ffmpeg_params=['-crf', '28']  # Lower quality, faster
```

4. **Download fewer clips:**
```python
# In visuals.py
videos_per_query = 1  # Instead of 2
```

### "Out of memory error"

**Solutions:**

1. **Reduce video resolution**
2. **Process fewer clips at once**
3. **Increase system RAM**
4. **Close other applications**

### "Disk space full"

**Solutions:**

1. **Clean output directory:**
```bash
rm -rf output/clips/*
rm -rf output/videos/*.mp4
```

2. **Compress old videos:**
```bash
ffmpeg -i input.mp4 -crf 28 output_compressed.mp4
```

3. **Setup automatic cleanup:**
```python
# Add to main.py
import shutil
shutil.rmtree('output/clips', ignore_errors=True)
```

---

## General Debug Tips

### Enable Verbose Logging

Add to top of `main.py`:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Test Individual Components

```bash
# Test each component separately
python scripts/script_generator.py
python scripts/voiceover.py
python scripts/visuals.py
python scripts/thumbnails.py
python scripts/compose.py
python scripts/upload.py
```

### Check Dependencies

```bash
pip list
pip check
python --version
ffmpeg -version
```

### Verify File Paths

```bash
# Check all expected files exist
ls -la config/
ls -la output/
tree output/  # If tree is installed
```

---

## Still Having Issues?

1. **Check GitHub Issues:** https://github.com/YOUR_USERNAME/youtube-automation-workflow/issues
2. **Search Discussions:** Look for similar problems
3. **Create New Issue:** Provide full error log and environment details

**When reporting issues, include:**
- Operating system and version
- Python version: `python --version`
- Error message (full traceback)
- Steps to reproduce
- Configuration (sanitized, no API keys)

---

## Emergency Fallbacks

### Can't use Ollama or Groq?
- Write scripts manually in `output/script.json`

### Can't use Edge-TTS?
- Use other TTS like `pyttsx3` or `gTTS`
- Record audio manually

### Can't download from Pexels?
- Use local video files
- Try Pixabay API instead

### Can't compose video?
- Use online video editors
- Use different library (e.g., Remotion)

---

**Most issues can be resolved by:**
1. ✅ Updating dependencies: `pip install --upgrade -r requirements.txt`
2. ✅ Checking API keys are correct
3. ✅ Verifying FFmpeg is installed
4. ✅ Ensuring sufficient disk space
5. ✅ Reading error messages carefully
