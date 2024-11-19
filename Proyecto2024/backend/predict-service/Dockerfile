FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout", "600","--access-logfile", "-", "--error-logfile", "-", "predict:app"]