# Vibe Math Vercel Deployment Guide

This guide provides step-by-step instructions for deploying the Vibe Math backend on Vercel, replacing the unreliable HuggingFace Spaces backend.

## Prerequisites

Before starting, ensure you have:
- A Vercel account (sign up at [vercel.com](https://vercel.com))
- Node.js installed on your machine
- A Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))
- Git installed (optional but recommended)

## Step 1: Verify Project Files

Ensure you have all the required files in your project directory:

```
vibe-math/
├── api/
│   ├── health.js              # Health check endpoint
│   ├── solve-json.js          # Base64 image endpoint
│   └── solve-with-key.js      # iOS Shortcuts endpoint
├── package.json              # Project dependencies
├── vercel.json               # Vercel configuration (fixed)
└── .env                      # Environment variables (local only)
```

### Check package.json
Your [`package.json`](package.json) should include:
```json
{
  "name": "vibe-math-api",
  "version": "1.0.0",
  "description": "Vibe Math API for solving math problems using Google Gemini",
  "main": "index.js",
  "scripts": {
    "dev": "vercel dev",
    "deploy": "vercel --prod"
  },
  "dependencies": {
    "@google/generative-ai": "^0.21.0",
    "cors": "^2.8.5"
  },
  "devDependencies": {},
  "keywords": [
    "math",
    "ai",
    "gemini",
    "api"
  ],
  "author": "melonwer",
  "license": "MIT"
}
```

### Check vercel.json
Your [`vercel.json`](vercel.json) should look like this (already fixed):
```json
{
  "version": 2,
  "functions": {
    "api/solve-with-key.js": {
      "maxDuration": 30
    },
    "api/solve-json.js": {
      "maxDuration": 30
    },
    "api/health.js": {
      "maxDuration": 10
    }
  },
  "rewrites": [
    {
      "source": "/api/solve-with-key",
      "destination": "/api/solve-with-key.js"
    },
    {
      "source": "/api/solve-json",
      "destination": "/api/solve-json.js"
    },
    {
      "source": "/api/health",
      "destination": "/api/health.js"
    },
    {
      "source": "/(.*)",
      "destination": "/api/health.js"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ],
  "env": {
    "GEMINI_API_KEY": "GEMINI_API_KEY"
  }
}
```

## Step 2: Install Vercel CLI

If you haven't already, install the Vercel CLI globally:

```bash
npm install -g vercel
```

Verify the installation:

```bash
vercel --version
```

## Step 3: Log in to Vercel

Log in to your Vercel account:

```bash
vercel login
```

This will open a browser window where you can authorize the CLI.

## Step 4: Set Up Environment Variables Locally (Optional)

Create a `.env` file in your project root for local development:

```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

Replace `your_actual_api_key_here` with your actual Google Gemini API key.

## Step 5: Deploy to Vercel

### Initial Deployment

Run the deployment command:

```bash
vercel --prod
```

You'll be prompted with several questions:
- Set up and deploy? → `yes`
- Which scope? → Select your account (e.g., "melonwer's projects")
- Link to existing project? → `no`
- What's your project's name? → `vibe-math-api` (or your preferred name)
- In which directory is your code located? → `./`
- Want to use the default Deployment Protection settings? → `yes`

Vercel will then deploy your project and provide you with a URL like `https://vibe-math-api-yourusername.vercel.app`.

## Step 6: Configure Environment Variables in Vercel

### Using Vercel CLI

Add your Gemini API key as an environment variable:

```bash
vercel env add GEMINI_API_KEY
```

When prompted:
- Select `production` for the environment
- Paste your Gemini API key (starts with "AIza")
- Confirm the value

### Using Vercel Dashboard (Alternative Method)

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to `Settings` → `Environment Variables`
4. Add a new environment variable:
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key
   - Environments: Select `Production`, `Preview`, and `Development`
5. Click `Add`

## Step 7: Redeploy with Environment Variables

After setting up the environment variables, redeploy your project:

```bash
vercel --prod
```

## Step 8: Test the Deployed Functions

### Get Your Deployment URL

After successful deployment, note your URL (e.g., `https://vibe-math-api-yourusername.vercel.app`).

### Test Health Check Endpoint

```bash
curl https://vibe-math-api-yourusername.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2023-07-31T01:08:30.420Z",
  "version": "1.0.0",
  "message": "API is running properly"
}
```

### Test solve-with-key Endpoint

Create a test file `test-request.json`:
```json
{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
  "api_key": "YOUR_GEMINI_API_KEY"
}
```

Then test the endpoint:
```bash
curl -X POST https://vibe-math-api-yourusername.vercel.app/api/solve-with-key \
  -H "Content-Type: application/json" \
  -d @test-request.json
```

### Test solve-json Endpoint

Create a test file `test-request-solve.json`:
```json
{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
}
```

Then test the endpoint:
```bash
curl -X POST https://vibe-math-api-yourusername.vercel.app/api/solve-json \
  -H "Content-Type: application/json" \
  -d @test-request-solve.json
```

## Step 9: Update iOS Shortcuts

### Method 1: Edit Existing Shortcut

1. Open the Shortcuts app on your iOS device
2. Find the "Vibe Math" shortcut
3. Tap the three dots (⋯) to edit
4. Find the "URL" action (around line 66-69 in the original shortcut)
5. Replace the URL with your new Vercel endpoint: `https://vibe-math-api-yourusername.vercel.app/api/solve-with-key`
6. Tap "Done" to save

### Method 2: Create New Shortcut

1. Open the Shortcuts app
2. Tap the "+" button to create a new shortcut
3. Add the following actions:
   - "Choose from Menu" with options: "Take Photo", "Select from Photos", "Use Clipboard"
   - Based on selection, add "Take Photo", "Get Latest Photos", or "Get Clipboard" actions
   - "Base64 Encode" action
   - "Ask for Input" for API key (text input)
   - "Get Contents of URL" action:
     - URL: `https://vibe-math-api-yourusername.vercel.app/api/solve-with-key`
     - Method: POST
     - Headers: Add "Content-Type" with value "application/json"
     - Body: JSON with `{"image": "[Base64 Image]", "api_key": "[API Key]"}`
   - "Get Dictionary Value" for key "answer"
   - "Show Result" with the answer
   - "Speak Text" with the answer
   - "Create Note" with title "Vibe Math Result" and body including the problem and solution

### Test the Updated Shortcut

1. Run the updated shortcut
2. Take a photo of a math problem or select one from your photos
3. Enter your Gemini API key when prompted
4. Verify that you get a response

## Step 10: Monitor and Maintain

### View Logs

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to the `Logs` tab to view function execution logs

### Set Up Analytics

1. In your Vercel dashboard, go to `Analytics`
2. Enable analytics for your project
3. Monitor usage and performance metrics

### Automatic Deploys

If you want to set up automatic deployments from Git:

1. In your Vercel dashboard, go to your project
2. Go to `Settings` → `Git`
3. Connect your Git repository
4. Vercel will automatically deploy when you push changes to your repository

## Troubleshooting

### Deployment Fails

**Error**: `The 'functions' property cannot be used in conjunction with the 'builds' property`
- **Solution**: This should now be fixed in the updated [`vercel.json`](vercel.json) file

**Error**: Missing dependencies
- **Solution**: Ensure all dependencies are listed in [`package.json`](package.json)

### Environment Variables Not Working

**Symptom**: API returns errors about missing API key
- **Solution**: 
  1. Verify you've added `GEMINI_API_KEY` to environment variables
  2. Redeploy after adding environment variables
  3. Check that the API key is valid

### API Returns Errors

**Symptom**: 500 Internal Server Error
- **Solution**:
  1. Check the Vercel function logs in the dashboard
  2. Verify your Gemini API key is valid and has quota
  3. Ensure the image is properly base64 encoded

### iOS Shortcut Issues

**Symptom**: Shortcut doesn't work with new endpoint
- **Solution**:
  1. Double-check the URL in the shortcut
  2. Ensure you're entering the correct API key
  3. Check that the image format is supported

## Cost Considerations

Vercel's free tier includes:
- 100GB bandwidth per month
- 10,000 serverless function invocations per month
- Unlimited projects

For typical Vibe Math usage, this should be sufficient to stay within the free tier.

## Conclusion

You've successfully deployed the Vibe Math backend on Vercel! This serverless solution provides:
- Better reliability than HuggingFace Spaces
- Automatic scaling
- Potential free hosting within Vercel's generous free tier
- Easy maintenance and monitoring

Your iOS Shortcuts should now work reliably with the new Vercel backend.