FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/br/com/app/src/main

EXPOSE 8081

CMD ["flask", "--app", "br.com.app.src.main.Main", "run", "--host=0.0.0.0", "--port=8081"]