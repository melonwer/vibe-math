# 📱 iOS Shortcuts Integration - Complete Guide

This document provides a comprehensive overview of the iOS Shortcuts integration for Vibe Math.

## 🚀 Quick Start

### 1. Install iOS Shortcut
- **Full Version**: [Vibe Math](https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131)
- **Lite Version**: [Vibe Math Lite](https://www.icloud.com/shortcuts/9f4a5b3c6e5f7g8h9i0j1k2l3m4n5o6p)

### 2. Get API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key (starts with `AIza...`)

### 3. First Use
1. Run the shortcut
2. Enter your API key when prompted
3. Allow camera and photo permissions
4. Start solving math problems!

## 📋 Available Resources

### Documentation
- **[README.md](README.md)** - Main documentation with iOS Shortcuts as primary focus
- **[docs/IOS_SHORTCUTS.md](docs/IOS_SHORTCUTS.md)** - Detailed iOS Shortcuts guide
- **[docs/IOS_INSTALLATION_GUIDE.md](docs/IOS_INSTALLATION_GUIDE.md)** - Visual installation guide with screenshots
- **[docs/API.md](docs/API.md)** - API documentation including new iOS Shortcuts endpoint

### Shortcuts Templates
- **[ios-shortcuts/VibeMath.shortcut](ios-shortcuts/VibeMath.shortcut)** - Full-featured shortcut
- **[ios-shortcuts/VibeMath-Lite.shortcut](ios-shortcuts/VibeMath-Lite.shortcut)** - Simplified version
- **[ios-shortcuts/README.md](ios-shortcuts/README.md)** - Shortcuts installation guide

## 🔧 API Endpoints

### Primary iOS Shortcuts Endpoint
```
POST /api/solve-with-key
```

**Request:**
```json
{
  "image": "base64_encoded_image_string",
  "api_key": "your_google_gemini_api_key"
}
```

**Response:**
```json
{
  "answer": "Answer: 42\nExplanation: The equation 6 × 7 equals 42 through basic multiplication."
}
```

### Legacy Endpoints
- `POST /solve` - Image file upload
- `POST /solve-json` - Base64 image (requires backend setup)

## 🎯 Features

### iOS Shortcuts Features
- 📸 **Camera Integration** - Take photos directly
- 🖼️ **Photo Library** - Select existing images
- 📋 **Clipboard Support** - Paste images
- 🔊 **Voice Results** - Optional text-to-speech
- 📱 **Widget Support** - Add to home screen
- ⌚ **Apple Watch** - Works on watchOS
- 🎯 **Siri Integration** - Voice activation

### Backend Options
1. **HuggingFace Spaces** (Recommended) - Free hosting
2. **Local Development** - For developers
3. **Docker Deployment** - Production ready

## 🚀 Deployment Options

### Option 1: HuggingFace Spaces (Easiest)
[![Deploy to HuggingFace Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-lg.svg)](https://huggingface.co/spaces/new?template=d4ydy/vibe-math)

### Option 2: Local Development
```bash
git clone https://github.com/melonwer/vibe-math.git
cd vibe-math
pip install -r requirements.txt
export GEMINI_API_KEY=your-key-here
uvicorn app.main:app --reload
```

### Option 3: Docker
```bash
docker-compose up --build
```

## 📞 Get Help

### Support Options
- **GitHub Issues**: [Report problems](https://github.com/melonwer/vibe-math/issues)
- **Email**: dmitrii.burkov@proton.me

### Common Issues
1. **Invalid API Key** - Check Google AI Studio
2. **Network Error** - Verify internet connection
3. **Image Too Large** - Use lower resolution
4. **Cannot Solve** - Retake with better lighting

## 🔄 Updates

### Automatic Updates
- **Shortcuts**: Sync via iCloud
- **Backend**: Auto-deploy on HuggingFace

### Manual Updates
- Check GitHub for new releases
- Redownload shortcuts if needed
- Update API key if required

---

<div align="center">
  <p><strong>Ready to solve math problems instantly with iOS Shortcuts?</strong></p>
  <p>
    <a href="https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131">📱 Download iOS Shortcut</a> |
    <a href="https://huggingface.co/spaces/new?template=d4ydy/vibe-math">🚀 Deploy Backend</a> |
    <a href="docs/IOS_SHORTCUTS.md">📖 Read Full Guide</a>
  </p>
</div>