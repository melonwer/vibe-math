# Vibe Math API Documentation

## Overview
Vibe Math API is a FastAPI-based service that uses Google's Gemini AI to solve math problems from images.

## Base URL
```
http://localhost:8000
```

## Authentication
The API requires a valid `GEMINI_API_KEY` environment variable to be set.

## Endpoints

### 1. Health Check
**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "/path/to/log/file.log"
}
```

### 2. Root Endpoint
**GET** `/`

Returns basic API information.

**Response:**
```json
{
  "message": "Vibe Math API is running",
  "version": "1.0.0",
  "endpoints": ["/solve", "/solve-json", "/api/solve-with-key", "/health"]
}
```

### 3. Solve from Image Upload
**POST** `/solve`

Upload an image file to solve a math problem.

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required): Image file (PNG, JPG, JPEG, max 5MB)

**Response:**
```json
{
  "answer": "Answer: 42\nExplanation: The solution is derived by..."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid file type or missing file
- `413 Payload Too Large`: File exceeds 5MB limit
- `500 Internal Server Error`: Processing error

### 4. Solve from Base64 Image
**POST** `/solve-json`

Send a base64-encoded image to solve a math problem.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "image": "base64-encoded-image-string"
}
```

**Response:**
```json
{
  "answer": "Answer: 42\nExplanation: The solution is derived by..."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid JSON or image data
- `500 Internal Server Error`: Processing error

### 5. Solve with API Key (iOS Shortcuts)
**POST** `/api/solve-with-key`

Solve math problems with API key authentication - designed specifically for iOS Shortcuts integration. This endpoint allows users to provide their Google Gemini API key directly in the request, eliminating the need for environment variable setup.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "image": "base64-encoded-image-string",
  "api_key": "your-google-gemini-api-key"
}
```

**Response:**
```json
{
  "answer": "Answer: 42\nExplanation: The equation 6 × 7 equals 42 through basic multiplication."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid JSON, image data, or missing parameters
- `401 Unauthorized`: Invalid API key provided
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Processing error
- `503 Service Unavailable`: Service temporarily unavailable

**iOS Shortcuts Example:**
```bash
curl -X POST https://your-backend.com/api/solve-with-key \
  -H "Content-Type: application/json" \
  -d '{"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", "api_key": "AIzaSy..."}'
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error description"
}
```

Common HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Temporary service issue

## Rate Limiting
The API implements rate limiting based on Gemini's API limits. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

## Example Usage

### cURL Examples

**Health Check:**
```bash
curl -X GET http://localhost:8000/health
```

**Solve from Image Upload:**
```bash
curl -X POST http://localhost:8000/solve \
  -F "file=@/path/to/math_problem.jpg"
```

**Solve from Base64:**
```bash
curl -X POST http://localhost:8000/solve-json \
  -H "Content-Type: application/json" \
  -d '{"image": "base64-encoded-image-string"}'
```

### Python Example

```python
import requests
import base64

# Upload image
with open('math_problem.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/solve', files=files)
    print(response.json())

# Base64 image
with open('math_problem.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()
    
response = requests.post(
    'http://localhost:8000/solve-json',
    json={'image': image_data}
)
print(response.json())
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `HOST` | Server host (default: 0.0.0.0) | No |
| `PORT` | Server port (default: 8000) | No |
| `LOG_LEVEL` | Logging level (default: INFO) | No |

## Docker Usage

```bash
# Build and run with Docker
docker-compose up --build

# Or run directly
docker build -t vibe-math .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key vibe-math