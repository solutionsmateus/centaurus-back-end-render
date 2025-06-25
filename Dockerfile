FROM python:3.10-slim-bullseye # Ou python:3.9-slim-buster, dependendo da sua versão Python

ENV PYTHONUNBUFFERED 1
ENV PORT 10000 # Render.com usa a porta 10000 por padrão

WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    fonts-liberation \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE ${PORT}

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
