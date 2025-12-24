# Physical AI & Humanoid Robotics Interactive Textbook

An AI-native, fast, simple, beautiful interactive textbook that teaches Physical AI & Humanoid Robotics. This system feels like a real AI-powered educational system — not a static book.

## Features

- 📚 **Docusaurus-based interactive textbook** with 6-8 short, modern chapters
- 🤖 **RAG-powered chatbot** that answers ONLY from textbook content with grounded, accurate, and cited responses
- 🎯 **Personalized explanations** based on user background
- 🌐 **One-click Urdu translation** for every chapter
- 📝 **Auto-generated content** including chapter summaries, quizzes, and learning boosters
- 🏗️ **Clean, modular architecture** using FastAPI backend and Docusaurus frontend

## Architecture

- **Frontend**: Docusaurus deployed on Vercel
- **Backend**: FastAPI deployed on Railway
- **Database**: Neon (PostgreSQL) for user data
- **Vector DB**: Qdrant for RAG functionality
- **Auth**: Better-Auth for user management

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- Qdrant instance (local or cloud)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn rag.app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key
```

## Project Structure

```
backend/
├── rag/                   # RAG service with FastAPI
│   ├── app/
│   │   └── main.py        # Main FastAPI application for RAG service
│   ├── models/
│   ├── services/
│   └── routes/
├── agents/                # AI agent services
├── auth/                  # Better-Auth integration
├── database/              # Database schemas and migrations
└── shared/
    └── types.py           # Shared data types and interfaces

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── styles/
├── static/
│   └── textbook-content/
│       └── chapters/
├── docusaurus.config.js
└── package.json
```

## Key Components

### 1. RAG Service
- Uses sentence-transformers/all-MiniLM-L6-v2 for embeddings
- Vector storage in Qdrant with cosine similarity
- Top-k (4-6) retrieval with reranking
- OpenAI GPT-4 for response generation

### 2. AI Agents
- **Summary Agent**: Auto-generates chapter summaries
- **Quiz Agent**: Creates quizzes based on chapter content
- **Translator Agent**: Handles Urdu translation with formatting preservation
- **Personalization Agent**: Adapts content based on user background

### 3. Personalization Engine
- Classifies user background into categories (beginner, intermediate, advanced, researcher)
- Adjusts content complexity, examples, and explanations accordingly

### 4. Translation Service
- Preserves markdown formatting during Urdu translation
- Uses HuggingFace translation models

## Demo

To experience the 90-second demo:

1. Browse the textbook content
2. Ask questions to the AI assistant
3. Personalize your experience based on your background
4. Try the Urdu translation feature
5. Explore auto-generated summaries and quizzes

Visit the `/demo` page in the application for a guided tour.

## Constitution & Principles

This project follows the Physical AI & Humanoid Robotics Interactive Textbook Constitution:

- **Education-First Design**: Textbook readable in under 45 minutes with 6-8 short chapters
- **AI-Native Integration**: RAG chatbot answers only from textbook content with citations
- **Accessibility & Localization**: One-click Urdu translation for every chapter
- **Clean Architecture**: Docusaurus frontend on Vercel, FastAPI backend on Railway
- **Resource Efficiency**: Free tier constraints respected, minimal UI, fast demo
- **User Experience Priority**: Smooth reading experience with chatbot, personalization, and translation

## Testing

The application is designed to be demo-ready in 90 seconds with all core features functional:

- Textbook content accessible
- RAG chatbot responding with textbook-only answers
- User authentication working
- Personalization based on user background
- Urdu translation functionality
- Auto-generated summaries and quizzes

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set build command to `npm run build`
3. Set output directory to `build`

### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set build command to `pip install -r requirements.txt`
3. Set start command to `uvicorn rag.app.main:app --host 0.0.0.0 --port $PORT`

## Contributing

We welcome contributions to improve the Physical AI & Humanoid Robotics Interactive Textbook. Please follow the education-first design principles and maintain the AI-native integration approach.

## License

This project is licensed under the terms specified in the repository.