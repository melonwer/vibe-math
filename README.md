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

# 🧮 Vibe Math - iOS Instant AI Math Solver

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-teal.svg)](https://fastapi.tiangolo.com/)
[![HuggingFace Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Spaces-yellow.svg)](https://huggingface.co/spaces)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](./Dockerfile)

> **📱 Solve math problems instantly with iOS Shortcuts** – Take a photo of any handwritten or printed equation and get the answer with clear explanations in seconds. Powered by Google Gemini AI through HuggingFace Spaces.

## 🚀 Quick Start (iOS Shortcuts)

The fastest way to use Vibe Math is through **iOS Shortcuts** - no coding required!

### 📱 Install in 30 Seconds

1. **Get your free API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Install the Vibe Math Shortcut**:
   - 📲 [Download Vibe Math Shortcut](https://www.icloud.com/shortcuts/a7beba54aa404434b2d0d6b82b590ece)
   - 🔗 Or scan the QR code below:
   
   <div align="center">
     <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.icloud.com%2Fshortcuts%2F8fa7beba54aa404434b2d0d6b82b590ece" alt="Vibe Math iOS Shortcut QR Code" width="200"/>
   </div>
   

3. **First-time setup**: Tap three dots for the setup
4. **Replace GEMINI_API_KEY** with **your API key** at Text box
5. **Start solving**: Run the script, take a photo of any math problem, and get instant results!

### 🎯 How It Works

1. **Take a photo** of any math problem (handwritten or printed)
2. **iOS Shortcuts** automatically processes the image
3. **HuggingFace Spaces** hosts the backend service
4. **Google Gemini AI** analyzes and solves the problem
5. **Get results** with step-by-step explanations in seconds

## 🛠️ Alternative Setup Methods

### Method 1: HuggingFace Spaces (Recommended Backend)
Deploy your own backend in minutes:

[![Deploy to HuggingFace Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-lg.svg)](https://huggingface.co/spaces/new?template=d4ydy/vibe-math)

1. **Fork this repository**
2. **Go to [HuggingFace Spaces](https://huggingface.co/spaces/new)**
3. **Select "Docker" as Space type**
4. **Set environment variable**: `GEMINI_API_KEY=your-key-here`
5. **Deploy** - your backend is ready!

### Method 2: Local Development
For developers who want to run locally:

#### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get yours here](https://makersuite.google.com/app/apikey))

#### Installation
```bash
# Clone the repository
git clone https://github.com/melonwer/vibe-math.git
cd vibe-math

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Docker Deployment
```bash
# Build and run with Docker
docker build -t vibe-math:latest .
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key-here vibe-math:latest

# Or use Docker Compose
docker-compose up --build
```

## 📱 iOS Shortcuts Integration

### 🔗 API Endpoints for iOS Shortcuts

| Endpoint | Method | Description | iOS Shortcuts Usage |
|----------|--------|-------------|---------------------|
| `/api/solve-with-key` | POST | Solve with API key | **Primary endpoint for iOS Shortcuts** |
| `/solve-json` | POST | Solve with base64 image | Legacy endpoint (requires backend setup) |

### 📋 iOS Shortcuts Setup Guide

#### Option 1: One-Click Install (Recommended)
- **Download**: [Vibe Math Shortcut](https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131)
- **Setup**: Enter your Google Gemini API key once
- **Use**: Share any image to the shortcut or run from Shortcuts app

#### Option 2: Manual Setup
If you prefer to build your own shortcut:

1. **Open Shortcuts app** on iOS
2. **Create new shortcut**
3. **Add actions**:
   - `Take Photo` or `Select from Photos`
   - `Convert Image to Base64`
   - `Get Contents of URL`:
     - URL: `https://your-backend.com/api/solve-with-key`
     - Method: `POST`
     - Headers: `Content-Type: application/json`
     - Body: `{"image": "[Base64 Image]", "api_key": "[Your API Key]"}`
   - `Get Dictionary Value`: `answer`
   - `Show Result`

### 🎨 iOS Shortcuts Features

- **📸 Camera Integration**: Take photos directly
- **🖼️ Photo Library**: Select existing images
- **🔊 Voice Results**: Optional text-to-speech for answers
- **📱 Widget Support**: Add to home screen
- **⌚ Apple Watch**: Works on watchOS too

## 🔧 API Documentation

### iOS Shortcuts Endpoint

#### `POST /api/solve-with-key`
**Description**: Solve math problems with API key authentication - designed for iOS Shortcuts

**Request Body**:
```json
{
  "image": "base64_encoded_image_string",
  "api_key": "your_google_gemini_api_key"
}
```

**Response**:
```json
{
  "answer": "Answer: 42\nExplanation: The equation 6 × 7 equals 42 through basic multiplication."
}
```

**Example iOS Shortcuts Usage**:
```bash
curl -X POST https://your-backend.com/api/solve-with-key \
  -H "Content-Type: application/json" \
  -d '{"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", "api_key": "your-key-here"}'
```

### Legacy Endpoints

#### `POST /solve`
Upload image file (multipart/form-data)

#### `POST /solve-json`
Send base64 image (application/json)

#### `GET /health`
Health check endpoint

## 🔐 Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key | - |
| `PORT` | ❌ | Server port | `8000` |
| `HOST` | ❌ | Server host | `0.0.0.0` |
| `LOG_LEVEL` | ❌ | Logging level | `INFO` |
| `MODEL_NAME` | ❌ | Gemini model name | `gemini-1.5-flash` |
| `MAX_TOKENS` | ❌ | Max tokens for responses | `500` |
| `TEMPERATURE` | ❌ | AI temperature | `0.2` |

## 🧪 Testing

Run the test suite:
```bash
# Install development dependencies
make dev-install

# Run all tests
make test

# Run linting
make lint

# Format code
make format
```

## 📸 Screenshots & Demo

### iOS Shortcuts in Action
<div align="center">
  <img src="https://via.placeholder.com/300x600/007AFF/FFFFFF?text=iOS+Shortcuts+Demo" alt="iOS Shortcuts Demo" width="300"/>
  <br>
  <em>Take a photo → Get instant math solutions</em>
</div>

### Live Demo
- **HuggingFace Spaces**: [Try it now](https://huggingface.co/spaces/d4ydy/vibe-math)
- **API Playground**: Interactive Swagger UI at `/docs`

## 🤝 Contributing

I welcome contributions! Here's how you can help:

### Development Setup
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and add tests
4. **Run tests**: `pytest`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**

### iOS Shortcuts Contributions
- **Improve the shortcut**: Submit updates to the iOS Shortcuts template
- **Add features**: Voice input, history, sharing options
- **Documentation**: Help improve setup guides and screenshots

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for new functions
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for providing the powerful AI model
- **FastAPI** for the excellent web framework
- **HuggingFace Spaces** for hosting and deployment
- **iOS Shortcuts** community for inspiration
- **OpenAI Python SDK** for seamless API integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/melonwer/vibe-math/issues)
- **Discussions**: [GitHub Discussions](https://github.com/melonwer/vibe-math/discussions)

---

<div align="center">
  <p>Made with ❤️ by melonwer</p>
  <p>
    <a href="https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131">📱 Get the iOS Shortcut</a> | 
    <a href="https://huggingface.co/spaces/d4ydy/vibe-math">🚀 Try on HuggingFace Spaces</a>
  </p>
</div>