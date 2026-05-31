FROM python:3.12-slim
WORKDIR /app
COPY fastapi/requirements.txt ./
RUN pip install --upgrade pip && python -m pip install -r requirements.txt
COPY fastapi/. .
COPY nginx ./nginx
EXPOSE 8001
CMD ["gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
