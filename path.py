import os

# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# Backend Root
# ---------------------------------------------------------
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")

# ---------------------------------------------------------
# Training Data Paths
# ---------------------------------------------------------
TRAINING_ROOT = os.path.join(PROJECT_ROOT, "training_data")

ORIGINAL_DOCS_DIR = os.path.join(TRAINING_ROOT, "original")
REDACTED_DOCS_DIR = os.path.join(TRAINING_ROOT, "redacted")

# ---------------------------------------------------------
# Model Paths (future-proof)
# ---------------------------------------------------------
MODEL_ROOT = os.path.join(PROJECT_ROOT, "models")

# Example placeholders:
EMBEDDING_MODEL_PATH = os.path.join(MODEL_ROOT, "embeddings")
REDACTION_MODEL_PATH = os.path.join(MODEL_ROOT, "redaction")

# ---------------------------------------------------------
# Server Configuration
# ---------------------------------------------------------
HOST = "0.0.0.0"
PORT = 8000

# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------
def ensure_dirs():
    """Create required directories if missing."""
    for path in [
        TRAINING_ROOT,
        ORIGINAL_DOCS_DIR,
        REDACTED_DOCS_DIR,
        MODEL_ROOT,
    ]:
        os.makedirs(path, exist_ok=True)