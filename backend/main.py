import sys, os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import models
from database import engine
from routes.auth_routes import router as auth_router
from routes.task_routes import router as task_router

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fix path — go up one level from backend to find frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

app.include_router(auth_router)
app.include_router(task_router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.get("/login-page")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")