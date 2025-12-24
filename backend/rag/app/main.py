from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.rag.routes import chat, auth, translation, personalization, chapter_routes
from backend.rag.core import logging_config

app = FastAPI(title="Physical AI & Humanoid Robotics Textbook API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(translation.router)
app.include_router(personalization.router)
app.include_router(chapter_routes.router)

@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics Textbook API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)