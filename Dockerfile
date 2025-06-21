FROM debian:bookworm-slim


WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcups2 \
    libgtk-3-0 \
    libgbm1 \
    python3.11-venv \
    python3-pip \
    libxss1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python3 -m venv /venv
RUN . /venv/bin/activate
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
