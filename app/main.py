import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional

from .models import LoginRequest
from .db import query, query_one
import os

title = os.getenv("APP_NAME", "dev")

app = FastAPI(title=title)
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: Optional[str] = None):
    # XSS: намеренно рендерим message без экранирования через шаблон (см. index.html)
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: Optional[str] = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or ""})

@app.get("/search")
def search(q: Optional[str] = None):
    if q:
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        return JSONResponse(content={"items": query(sql, (f"%{q}%",))})
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        return JSONResponse(content={"items": query(sql)})


@app.post("/login")
def login(payload: LoginRequest):
    try:
        sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
        row = query_one(sql, (payload.username, payload.password))
        if not row:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return {"status": "ok", "user": row["username"], "token": "dummy"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # В случае ошибок валидации
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )