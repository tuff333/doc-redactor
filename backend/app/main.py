# ---------------------------------------------------------
# File: backend/app/main.py
# Clean FastAPI entrypoint for Doc‑Redactor
# ---------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules
from .routes import (
    upload,
    view,
    save,
    redact_text,
    redact_multiple,
    redact_box,
    chat,
    suggest,
    tags,
    redact_suggest,
    redact_auto,
    archive_routes,
    download,
    history,
)

app = FastAPI(title="Document Redaction System")

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # You can tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(upload.router)
app.include_router(view.router)
app.include_router(save.router)
app.include_router(redact_text.router)
app.include_router(redact_multiple.router)
app.include_router(redact_box.router)
app.include_router(chat.router)
app.include_router(suggest.router)
app.include_router(tags.router)
app.include_router(redact_suggest.router)
app.include_router(redact_auto.router)
app.include_router(archive_routes.router)
app.include_router(download.router)
app.include_router(history.router)


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Document Redaction System backend is running (hybrid version)."}