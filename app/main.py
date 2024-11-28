from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from prometheus_client import make_asgi_app
import time

from .models import ToxicityRequest, ToxicityResponse
from .config import get_settings
from .utils import ToxicityAnalyzer
from .metrics import (
    MetricsMiddleware, TEXTS_PROCESSED, 
    BATCH_SIZE, REQUEST_COUNT, REQUEST_LATENCY
)
from .templates import get_index_html

settings = get_settings()

app = FastAPI(
    title="Toxicity Analysis API",
    description="High-performance API for text toxicity analysis",
    version="1.0.0"
)

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add middlewares
app.add_middleware(CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MetricsMiddleware)

# Initialize toxicity analyzer
analyzer = ToxicityAnalyzer(max_workers=settings.max_workers)

@app.get("/", response_class=HTMLResponse)
async def root():
    return get_index_html()

@app.post("/analyze", response_model=ToxicityResponse)
async def analyze_texts(
    request: Request,
    body: ToxicityRequest,
) -> ToxicityResponse:
    """Analyze texts for toxicity"""
    try:
        # Record metrics
        TEXTS_PROCESSED.inc(len(body.texts))
        BATCH_SIZE.observe(body.batch_size or settings.batch_size)
        
        results, processing_time = await analyzer.process_texts(
            texts=body.texts,
            batch_size=body.batch_size or settings.batch_size
        )
        
        return ToxicityResponse(
            results=results,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }