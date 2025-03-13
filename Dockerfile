FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

COPY .env /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

EXPOSE 8001

CMD ["uvicorn", "oms.main:app", "--host", "0.0.0.0", "--port", "8001"]
