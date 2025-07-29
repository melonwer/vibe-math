import os
import base64
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise RuntimeError("GEMINI_API_KEY environment variable is required")

# Configuration
MODEL_NAME = "gemini-1.5-flash"
MAX_TOKENS = 500
TEMPERATURE = 0.2

# Initialize OpenAI client
client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=GEMINI_API_KEY
)

# System prompt
SYSTEM_PROMPT = (
    "You are an expert science and math tutor who provides clear, thoughtful, and brief explanations. Given an image of a problem, "
    "Your response must strictly follow this format: 'Answer: [Your final numerical or symbolic answer]\nExplanation: [A concise 1-2 sentence explanation of the solution steps or concept].' "
    "If the problem is unclear or cannot be solved from the image, state 'Cannot solve: [reason]' instead of an answer."
)

# Pydantic models
class ImagePayload(BaseModel):
    image: str
    
    @validator('image')
    def validate_image(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Image must be a non-empty string')
        return v

class ImagePayloadWithKey(BaseModel):
    image: str
    api_key: str
    
    @validator('image')
    def validate_image(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Image must be a non-empty string')
        return v
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('API key must be a non-empty string')
        return v

class ErrorResponse(BaseModel):
    detail: str
    status_code: int

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    logger.info("Starting Vibe Math API")
    yield
    logger.info("Shutting down Vibe Math API")

# Create FastAPI app
app = FastAPI(
    title="Vibe Math API",
    description="AI-powered math problem solver using Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
async def process_image(image_data: str) -> str:
    """Process and validate image data"""
    try:
        if image_data.startswith('data:image'):
            # Handle data URI format
            if ',' in image_data:
                image_data = image_data.split(',')[1]
        
        # Validate base64
        base64.b64decode(image_data)
        return f"data:image/png;base64,{image_data}"
    except Exception as e:
        logger.error(f"Invalid image data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image data provided"
        )

async def call_gemini_api_with_key(image_uri: str, api_key: str) -> str:
    """Make API call to Gemini with custom API key"""
    try:
        # Create a new client with the provided API key
        custom_client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta",
            api_key=api_key
        )
        
        response = await custom_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": "Solve this."}
                ]}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No response from AI model"
            )
            
        return response.choices[0].message.content.strip()
        
    except RateLimitError:
        logger.error("Rate limit exceeded")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    except APIConnectionError:
        logger.error("Connection error to Gemini API")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable. Please try again later."
        )
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        if "API key" in str(e) or "authentication" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key provided"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing your request"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

async def call_gemini_api(image_uri: str) -> str:
    """Make API call to Gemini using environment API key"""
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": "Solve this."}
                ]}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No response from AI model"
            )
            
        return response.choices[0].message.content.strip()
        
    except RateLimitError:
        logger.error("Rate limit exceeded")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    except APIConnectionError:
        logger.error("Connection error to Gemini API")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable. Please try again later."
        )
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing your request"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

# Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Vibe Math API is running",
        "version": "1.0.0",
        "endpoints": ["/solve", "/solve-json", "/api/solve-with-key", "/health"]
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": logger.handlers[0].baseFilename if logger.handlers else None
    }

@app.post("/solve", tags=["Solve"])
async def solve(file: UploadFile = File(...)):
    """
    Solve math problem from uploaded image
    
    - **file**: Image file (PNG, JPG, JPEG supported)
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read and process image
        img_bytes = await file.read()
        if len(img_bytes) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image file too large (max 5MB)"
            )
        
        b64 = base64.b64encode(img_bytes).decode()
        data_uri = f"data:image/png;base64,{b64}"
        
        # Call Gemini API
        answer = await call_gemini_api(data_uri)
        
        logger.info(f"Successfully solved problem from uploaded image")
        return {"answer": answer}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing uploaded image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing image"
        )

@app.post("/solve-json", tags=["Solve"])
async def solve_json(payload: ImagePayload):
    """
    Solve math problem from base64 image string
    
    - **payload**: JSON payload with base64 image string
    """
    try:
        # Process image
        data_uri = await process_image(payload.image)
        
        # Call Gemini API
        answer = await call_gemini_api(data_uri)
        
        logger.info(f"Successfully solved problem from JSON payload")
        return {"answer": answer}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing JSON payload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing request"
        )

@app.post("/api/solve-with-key", tags=["iOS Shortcuts"])
async def solve_with_key(payload: ImagePayloadWithKey):
    """
    Solve math problem from base64 image string with API key authentication
    
    Designed specifically for iOS Shortcuts integration. This endpoint allows
    users to provide their Google Gemini API key directly in the request,
    eliminating the need for environment variable setup.
    
    - **payload**: JSON payload with base64 image string and API key
    """
    try:
        # Process image
        data_uri = await process_image(payload.image)
        
        # Call Gemini API with provided API key
        answer = await call_gemini_api_with_key(data_uri, payload.api_key)
        
        logger.info(f"Successfully solved problem using custom API key")
        return {"answer": answer}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request with key: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing request"
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle any unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)