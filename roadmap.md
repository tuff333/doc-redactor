# 📘 Doc‑Redactor Roadmap

This roadmap outlines the planned enhancements for the Doc‑Redactor backend.  
The core training pipeline is complete and stable — the following items represent the next phase of accuracy, performance, and maintainability improvements.

---

## 🚀 Phase 1 — Accuracy Improvements (Upcoming)

### 1. Advanced Span Detection
Enhance the detection of sensitive fields using:
- Table‑aware detection
- Regex‑based field extraction
- Multi‑line field grouping
- Numeric pattern detection (%, mg/g, ppm)
- Chemical name detection (terpenes, cannabinoids, analytes)

### 2. Expanded Training Dataset
Increase dataset size from 23 → 50–100+ paired PDFs.
- Improve generalization
- Reduce false negatives
- Improve performance on diverse CoA formats

---

## 🚀 Phase 2 — Evaluation & Analytics (Upcoming)

### 3. Evaluation Module
Add a dedicated evaluation pipeline:
- Precision / Recall / F1 per document
- Confusion matrix
- Error analysis (FP/FN/partial overlaps)
- Summary reports

### 4. Logging System
Add structured logs:
- `training_logs/` directory
- Timestamped training runs
- Metrics per epoch
- Dataset statistics
- Warning/error logs

---

## 🚀 Phase 3 — Performance & Scalability (Upcoming)

### 5. GPU Support
Enable GPU‑accelerated training:
- Auto‑detect GPU
- Update spaCy config for CUDA
- 10–20× faster training

### 6. Model Versioning
Automatically save models as:
- `model_v1/`
- `model_v2/`
- `model_v3/`
- Timestamp‑based versioning
- Easy rollback and comparison

---

## 🚀 Phase 4 — Future Enhancements (Long‑Term)

### 7. Synthetic Data Generation
Automatically generate synthetic redaction examples.

### 8. Web‑based Training Dashboard
Visualize:
- Training progress
- Metrics
- Model versions
- Dataset health

### 9. Plugin Architecture
Allow custom detection rules per client or document type.

---

## 📌 Status
All items above are **planned** and not yet implemented.  
The backend is fully functional and ready for iterative improvements.