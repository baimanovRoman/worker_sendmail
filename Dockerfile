FROM python:3.10-slim
WORKDIR /app
COPY req.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt