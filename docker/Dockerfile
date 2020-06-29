FROM python:3

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.dev.txt .

RUN pip install -r requirements.dev.txt

COPY . .

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
