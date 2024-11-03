FROM python:3.12
LABEL authors="sinortax"

WORKDIR /app
COPY . .
COPY .env /app/.env
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "-c", "source /app/.env && exec python main.py"]