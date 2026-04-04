FROM python:3.11-slim
LABEL maintainer="ACEest DevOps"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos "" aceest
USER aceest
EXPOSE 5000
CMD ["sh", "-c", "python -c 'from app import init_db; init_db()' && python app.py"]