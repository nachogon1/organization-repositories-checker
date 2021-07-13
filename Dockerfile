# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]