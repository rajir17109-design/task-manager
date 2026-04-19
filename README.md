# Task Manager API

A FastAPI-based Task Manager Web Application with JWT 
authentication and SQLite database.

# Tech Stack
- FastAPI (Python)
- SQLite + SQLAlchemy
- JWT Authentication (python-jose)
- Password Hashing (bcrypt)
- Plain HTML/CSS/JS Frontend (served via Jinja2)
- pytest (Testing)

# Setup Instructions

1. Clone the repo
   git clone https://github.com/rajir17109-design/task-manager.git
   cd task-manager

2. Create virtual environment (optional)
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   cp .env.example .env
   Edit SECRET_KEY with a strong random string

5. Run the app
   cd backend
   python -m uvicorn main:app --reload

6. Open browser
   http://localhost:8000

# API Docs
   http://localhost:8000/docs

# Run Tests
   cd backend
   python -m pytest tests/test_main.py -v

# Environment Variables
   SECRET_KEY — JWT secret key
   DATABASE_URL — SQLite URL

# Deployment
   Live at: (will update after deployment)

# GitHub
   https://github.com/rajir17109-design/task-manager

# Important Note
- App deployed on Render free tier
- First load may take 50 seconds (cold start)
- Please register a new account to test
- SQLite resets on Render restart — 
  for production PostgreSQL recommended
     