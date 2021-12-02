# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /starwars-store
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app_restful.py"]
