from setuptools import setup, find_packages

setup(
    name="physical-ai-textbook-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.105.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.23",
        "qdrant-client>=1.7.0",
        "openai>=1.3.7",
        "sentence-transformers>=2.2.2",
        "torch>=2.1.1",
        "numpy>=1.24.3",
        "python-multipart>=0.0.6",
        "passlib[bcrypt]>=1.7.4",
        "python-jose[cryptography]>=3.3.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.9",
    ],
)