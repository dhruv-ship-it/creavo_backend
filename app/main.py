from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.session import engine
from app.api.routes import auth, topic, script, seo, comment, lead, sale

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Creavo Backend")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Fallback port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add rate limiting exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(topic.router, prefix="/api/topics", tags=["topics"])
app.include_router(script.router, prefix="/api/scripts", tags=["scripts"])
app.include_router(seo.router, prefix="/api/seo", tags=["seo"])
app.include_router(comment.router, prefix="/api/comments", tags=["comments"])
app.include_router(lead.router, prefix="/api/leads", tags=["leads"])
app.include_router(sale.router, prefix="/api/sales", tags=["sales"])

@app.get("/")
@limiter.limit("100/minute")
def root(request: Request):
    return {"message": "Creavo backend running"}

@app.get("/health")
@limiter.limit("100/minute")
def health(request: Request):
    try:
        with engine.connect() as connection:
            return {
                "status": "ok",
                "db": "connected",
                "version": "1.0"
            }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "db": "not connected",
                "version": "1.0",
                "detail": str(e)
            }
        )
