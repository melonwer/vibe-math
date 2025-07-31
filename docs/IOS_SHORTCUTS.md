# 📱 iOS Shortcuts Setup Guide

This guide will help you set up Vibe Math on your iPhone or iPad using iOS Shortcuts for instant math problem solving.

## 🚀 Quick Setup (2 Minutes)

### Step 1: Get Your API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your key (starts with `AIza...`)

### Step 2: Install the Shortcut
**Option A: One-Click Install**
- 📲 [Download Vibe Math Shortcut](https://www.icloud.com/shortcuts/c22a63e866814b4c9b5f59fe574e3131)

**Option B: QR Code**
<div align="center">
  <img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https%3A%2F%2Fwww.icloud.com%2Fshortcuts%2F8f3a4b2c5d4e6f7a8b9c0d1e2f3a4b5c" alt="Vibe Math iOS Shortcut QR Code" width="300"/>
</div>

### Step 3: First-Time Setup
1. **Tap three dots** for the setup
2. **Replace your API key** with **GEMINI_API_KEY** at Text box
3. **Run the script** for the first time
4. **Start solving** math problems instantly!

## 📋 How to Use

### Method 1: Camera (Recommended)
1. **Open Shortcuts app**
2. **Tap "Vibe Math"**
3. **Take a photo** of the math problem
4. **Get instant results** with explanations

### Method 2: Photo Library
1. **Open Photos app**
2. **Select any image** with math problems
3. **Tap Share button**
4. **Choose "Vibe Math"** from share sheet
5. **View results** immediately

### Method 3: Files App
1. **Open Files app**
2. **Find your math image**
3. **Long press the file**
4. **Select "Vibe Math"**
5. **Get your answer**

## 🎨 Customization Options

### Add to Home Screen
1. **Open Shortcuts app**
2. **Find "Vibe Math"**
3. **Tap the three dots** (⋯)
4. **Select "Add to Home Screen"**
5. **Choose icon** and name
6. **Tap "Add"**

### Create Widget
1. **Long press home screen**
2. **Tap "+" (Add Widget)**
3. **Search "Shortcuts"**
4. **Select widget size**
5. **Choose "Vibe Math"**
6. **Place on home screen**

### Siri Integration
1. **Open Shortcuts app**
2. **Find "Vibe Math"**
3. **Tap the three dots** (⋯)
4. **Tap "Add to Siri"**
5. **Record phrase**: "Solve math"
6. **Say "Hey Siri, solve math"** to launch

## 🔧 Manual Setup (Advanced Users)

If you prefer to build your own shortcut:

### Required Components
1. **Get Image** action
2. **Convert Image** to Base64
3. **Get Contents of URL** action
4. **Parse JSON** response
5. **Show Result** action

### Configuration Details
- **URL**: `https://your-backend.com/api/solve-with-key`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "image": "[Base64 Image Data]",
  "api_key": "[Your API Key]"
}
```

### Sample Shortcut Structure
```
1. Take Photo
2. Convert to Base64
3. Ask for Input (API Key - saved to variable)
4. Get Contents of URL
   - URL: https://your-backend.com/api/solve-with-key
   - Method: POST
   - Headers: Content-Type: application/json
   - Body: {"image": "Base64", "api_key": "API_KEY"}
5. Get Dictionary Value: answer
6. Show Result
```

## 📸 Screenshots Guide

### Taking Good Photos
- **Good lighting** - avoid shadows
- **Clear focus** - tap to focus on math
- **Straight angle** - avoid perspective distortion
- **Close enough** - fill most of the frame
- **Clean background** - avoid clutter

### Examples of Good vs Bad Photos

**✅ Good Examples:**
- Printed textbook problems
- Neatly written equations
- High contrast (dark pen on white paper)
- Single problem per photo

**❌ Bad Examples:**
- Blurry or out of focus
- Multiple problems in one photo
- Poor lighting or shadows
- Handwriting too small
- Crumpled paper

## 🔍 Troubleshooting

### Common Issues

#### "Invalid API Key"
- **Check**: API key starts with `AIza...`
- **Verify**: Key is active in Google AI Studio
- **Solution**: Re-enter key in shortcut settings

#### "Image Too Large"
- **Problem**: Image file > 5MB
- **Solution**: Use lower resolution or compress image
- **Tip**: iOS photos are usually fine

#### "Cannot Solve Problem"
- **Check**: Image is clear and focused
- **Verify**: Math problem is visible
- **Solution**: Retake photo with better lighting

#### "Network Error"
- **Check**: Internet connection
- **Verify**: Backend URL is correct
- **Solution**: Try again or check backend status

### Reset API Key
1. **Open Shortcuts app**
2. **Find "Vibe Math"**
3. **Tap the three dots** (⋯)
4. **Scroll to settings**
5. **Update API key**

## 🎯 Advanced Features

### Batch Processing
Process multiple images at once:
1. **Select multiple photos**
2. **Share to Vibe Math**
3. **Get results** for each image

### History Tracking
Save results to Notes:
1. **Add action**: "Create Note"
2. **Include**: Image + Answer + Date
3. **Save to**: "Vibe Math History" folder

### Voice Results
Enable text-to-speech:
1. **Add action**: "Speak Text"
2. **Input**: Answer from API
3. **Voice**: Choose your preferred voice

## 📱 Compatibility

### Supported Devices
- **iPhone**: iOS 14+
- **iPad**: iPadOS 14+
- **Apple Watch**: watchOS 7+ (limited features)

## 🔄 Updates

### Automatic Updates
- **Shortcuts**: Updates automatically via iCloud
- **Backend**: Deployed on HuggingFace Spaces

### Manual Updates
1. **Check GitHub** for new versions
2. **Redownload shortcut** if needed
3. **Update API key** if required

## 📞 Get Help

### Support Options
- **GitHub Issues**: [Report problems](https://github.com/melonwer/vibe-math/issues)
- **Email**: dmitrii.burkov@proton.me

---

<div align="center">
  <p><strong>Ready to solve math problems instantly?</strong></p>
  <p>
    <a href="https://www.icloud.com/shortcuts/a7beba54aa404434b2d0d6b82b590ece">📱 Get the iOS Shortcut</a> | 
    <a href="https://vercel.com/melonwers-projects/vibe-math-api">🚀 Try on Vercel App</a> | 
    <a href="https://huggingface.co/spaces/d4ydy/vibe-math">🤗 Try on HuggingFace Spaces</a>
  </p>
</div>