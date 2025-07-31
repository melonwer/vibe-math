const cors = require("cors");

// Configure CORS
const corsHandler = cors({
  origin: "*",
  methods: ["GET", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
});

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

  // Only allow GET requests
  if (req.method !== "GET") {
    return res.status(405).json({ detail: "Method not allowed" });
  }

  try {
    // Get API key from environment variables
    const apiKey = process.env.GEMINI_API_KEY;
    const isApiKeySet = !!apiKey;
    
    // Determine health status
    const status = isApiKeySet ? "healthy" : "degraded";
    const statusCode = isApiKeySet ? 200 : 503;
    
    // Prepare response
    const response = {
      status: status,
      timestamp: new Date().toISOString(),
      version: "1.0.0",
      api_key_set: isApiKeySet,
      message: isApiKeySet 
        ? "API is healthy and ready to process requests" 
        : "API is in degraded state - GEMINI_API_KEY environment variable is not configured"
    };
    
    // Return response with appropriate status code
    return res.status(statusCode).json(response);
  } catch (error) {
    console.error("Error in health check:", error.message);
    
    // Return error response
    return res.status(500).json({
      status: "unhealthy",
      timestamp: new Date().toISOString(),
      version: "1.0.0",
      api_key_set: false,
      error: error.message,
      message: "An unexpected error occurred during health check"
    });
  }
};