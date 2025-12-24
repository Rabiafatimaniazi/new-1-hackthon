# Physical AI & Humanoid Robotics Textbook - Backend

This is the backend API for the Physical AI & Humanoid Robotics Interactive Textbook, built with FastAPI.

## Features

- RAG-powered chatbot for textbook content
- User authentication and profile management
- Personalized content adaptation
- Urdu translation service
- Auto-generated summaries and quizzes
- Chapter management system

## Prerequisites

- Python 3.8+
- OpenAI API key
- Qdrant vector database instance
- PostgreSQL database (for production)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ENVIRONMENT=development  # or production
```

## Running the Server

```bash
# Using uvicorn directly
uvicorn backend.rag.app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the start script
python start_server.py
```

## API Documentation

Once the server is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

- **FastAPI**: Main web framework
- **Qdrant**: Vector database for RAG functionality
- **OpenAI**: For response generation and content processing
- **Sentence Transformers**: For embedding generation
- **Pydantic**: Data validation and settings management

## Endpoints

- `/chat/query` - RAG-powered chat with textbook content
- `/auth/` - User authentication (signup, login, profile)
- `/chapters/` - Chapter management and retrieval
- `/personalization/` - Content personalization
- `/translation/` - Urdu translation service
- `/agents/` - Auto-generated content (summaries, quizzes)

## Development

This project follows a modular architecture with services, models, and routes separated into distinct modules. When adding new features:

1. Create models in `backend/rag/models/`
2. Implement services in `backend/rag/services/`
3. Define routes in `backend/rag/routes/`
4. Add integration in `backend/rag/app/main.py`

## Error Handling and Logging

The application uses structured logging with rotation. Logs are stored in the `logs/` directory.