---
title: Vibe Math
emoji: 📱
colorFrom: purple
colorTo: blue
sdk: docker
sdk_version: "3.11"
app_file: app/main.py
pinned: false
---

# Vibe Math - iOS Shortcuts Powered Math Solver

Solve math problems instantly using your iPhone camera and AI!

## 📱 Quick Start

This HuggingFace Space powers the **Vibe Math iOS Shortcut** - a revolutionary way to solve math problems using just your iPhone camera.

### 🚀 How to Use

1. **Install the iOS Shortcut**: [Download Vibe Math Shortcut](https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131)
2. **Get your Google Gemini API key**: [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Take a photo** of any math problem (handwritten or printed)
4. **Get instant results** with step-by-step explanations

### 🔧 API Endpoints

- **Primary endpoint**: `POST /api/solve-with-key`
- **Health check**: `GET /health`
- **Interactive docs**: `GET /docs`

### 📋 Example Usage

```bash
curl -X POST https://your-space-url.hf.space/api/solve-with-key \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image", "api_key": "your-gemini-key"}'
```

### 🎯 Features

- 📸 **Camera Integration**: Works with iOS Shortcuts
- 🧮 **Math Recognition**: Handwritten and printed equations
- 🤖 **AI Powered**: Google Gemini AI for accurate solutions
- ⚡ **Instant Results**: Get answers in seconds
- 📱 **Mobile First**: Designed for iPhone users

## 🔐 Environment Setup

Set your Google Gemini API key in the Space settings:
- **Variable**: `GEMINI_API_KEY`
- **Required**: Yes
- **Get key**: [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Development

This space runs on Docker with:
- **Python 3.11**
- **FastAPI** web framework
- **Google Gemini AI** integration
- **iOS Shortcuts** compatibility

## 📞 Support

- **GitHub**: [Vibe Math Repository](https://github.com/melonwer/vibe-math)
- **Issues**: [Report bugs or request features](https://github.com/melonwer/vibe-math/issues)
- **iOS Shortcuts**: [Download the shortcut](https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131)

---

<div align="center">
  <p>Made with ❤️ for iOS users</p>
  <p>
    <a href="https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131">📱 Get the iOS Shortcut</a>
  </p>
</div>