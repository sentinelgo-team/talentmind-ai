# ─────────────────────────────────────────────
#  TalentMind AI  ─  Dockerfile
#  Multi-stage build for production deployment
# ─────────────────────────────────────────────

# ── Stage 1: Builder ─────────────────────────
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: Production ───────────────────────
FROM python:3.11-slim AS production

# Security: Create non-root user
RUN groupadd -r talentmind \
    && useradd -r -g talentmind -d /app -s /sbin/nologin talentmind

# Set working directory
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /home/talentmind/.local

# Copy application code
COPY --chown=talentmind:talentmind . .

# Create required directories
RUN mkdir -p \
    data/uploads \
    data/processed \
    data/reports \
    data/vector_db \
    logs \
    && chown -R talentmind:talentmind data logs

# Switch to non-root user
USER talentmind

# Environment variables
ENV PATH=/home/talentmind/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
    --start-period=40s --retries=3 \
    CMD python -c "import requests; \
    requests.get('http://localhost:8501/_stcore/health')" \
    || exit 1

# Entry point
CMD ["python", "-m", "streamlit", "run", \
     "app/main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]