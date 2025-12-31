import os
import uvicorn
from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI(
    # You can keep your existing title, description, version, etc. here if you had them
    # title="My App",
    # description="My awesome app",
    # version="1.0.0",
)

# ==================== YOUR EXISTING CODE STARTS HERE ====================
# Paste ALL your routes, logic, middleware, etc. exactly as they were before.
# Nothing needs to change in this section.

@app.get("/")
async def root():
    return {"message": "Hello World - Deployed successfully on Render!"}

# Example additional route - replace with your actual routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add all your other routes, dependencies, models, etc. below...
# (Keep everything exactly as it was - no changes needed)

# ==================== YOUR EXISTING CODE ENDS HERE ====================

# This block only runs when you execute `python main.py` directly
if __name__ == "__main__":
    # Use Render's PORT environment variable if available, otherwise default to 8000 for local dev
    port = int(os.environ.get("PORT", 8000))
    
    # Critical for Render: bind to 0.0.0.0 so it's publicly accessible
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)  # reload=True only for local dev
