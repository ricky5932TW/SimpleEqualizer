FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libasound2-dev \
        portaudio19-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    HOST=0.0.0.0 \
    PORT=5000 \
    FLASK_DEBUG=0 \
    OPEN_BROWSER=0 \
    SQLITE_PATH=/app/data/simpleequalizer.sqlite3

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libasound2 \
        libasound2-plugins \
        libglib2.0-0 \
        libpulse0 \
        libportaudio2 \
        pulseaudio-utils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY . .
COPY docker/asound-pulse.conf /etc/asound.conf
RUN mkdir -p /app/data /app/static/temp_img

EXPOSE 5000
VOLUME ["/app/data"]

CMD ["python", "web_gui.py"]
