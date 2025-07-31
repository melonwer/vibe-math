const { GoogleGenerativeAI } = require("@google/generative-ai");
const cors = require("cors");

// Configure CORS
const corsHandler = cors({
  origin: "*",
  methods: ["POST", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
});

// Configuration
const MODEL_NAME = "gemini-1.5-flash";
const MAX_TOKENS = 500;
const TEMPERATURE = 0.2;

// System prompt
const SYSTEM_PROMPT = (
  "You are an expert science and math tutor who provides clear, thoughtful, and brief explanations. Given an image of a problem, " +
  "Your response must strictly follow this format: 'Answer: [Your final numerical or symbolic answer]\nExplanation: [A concise 1-2 sentence explanation of the solution steps or concept].' " +
  "If the problem is unclear or cannot be solved from the image, state 'Cannot solve: [reason]' instead of an answer."
);

// Helper function to process and validate image data
function processImage(imageData) {
  try {
    if (imageData.startsWith('data:image')) {
      // Handle data URI format
      if (imageData.includes(',')) {
        imageData = imageData.split(',')[1];
      }
    }
    
    // Validate base64
    Buffer.from(imageData, 'base64');
    return `data:image/png;base64,${imageData}`;
  } catch (error) {
    throw new Error("Invalid image data provided");
  }
}

// Helper function to call Gemini API
async function callGeminiAPI(imageUri, apiKey) {
  try {
    // Initialize Google Generative AI with the environment API key
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });
    
    // Create the prompt with the image
    const prompt = {
      contents: [{
        role: "user",
        parts: [
          { text: SYSTEM_PROMPT },
          { 
            inline_data: {
              mime_type: "image/png",
              data: imageUri.split(',')[1] // Extract base64 data from URI
            }
          },
          { text: "Solve this." }
        ]
      }]
    };
    
    // Generate content
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    if (!text) {
      throw new Error("No response from AI model");
    }
    
    return text.trim();
  } catch (error) {
    if (error.message.includes("API key") || error.message.includes("authentication")) {
      throw new Error("Invalid API key provided");
    } else if (error.message.includes("quota") || error.message.includes("rate limit")) {
      throw new Error("Rate limit exceeded. Please try again later.");
    } else if (error.message.includes("connection") || error.message.includes("network")) {
      throw new Error("Service temporarily unavailable. Please try again later.");
    } else {
      throw new Error(`Internal server error: ${error.message}`);
    }
  }
}

// Main handler function
module.exports = async (req, res) => {
  // Handle preflight requests
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // Apply CORS
  await new Promise((resolve, reject) => {
    corsHandler(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });

  // Only allow POST requests
  if (req.method !== "POST") {
    return res.status(405).json({ detail: "Method not allowed" });
  }

  try {
    // Parse request body
    const { image } = req.body;

    // Validate input
    if (!image || typeof image !== "string") {
      return res.status(400).json({ detail: "Image must be a non-empty string" });
    }

    // Get API key from environment variables
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ detail: "API key not configured" });
    }

    // Process image
    const dataUri = processImage(image);

    // Call Gemini API
    const answer = await callGeminiAPI(dataUri, apiKey);

    // Return response
    return res.status(200).json({ answer });
  } catch (error) {
    console.error("Error processing request:", error.message);
    
    // Handle specific error cases
    if (error.message === "Invalid image data provided") {
      return res.status(400).json({ detail: error.message });
    } else if (error.message === "Invalid API key provided") {
      return res.status(500).json({ detail: "Invalid API key configuration" });
    } else if (error.message === "Rate limit exceeded. Please try again later.") {
      return res.status(429).json({ detail: error.message });
    } else if (error.message === "Service temporarily unavailable. Please try again later.") {
      return res.status(503).json({ detail: error.message });
    } else {
      return res.status(500).json({ detail: "An unexpected error occurred" });
    }
  }
};