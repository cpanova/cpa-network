FROM python:3.11-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /app

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
