FROM python:3.10.12-slim

WORKDIR /app

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Copy the requirements.txt from the parent directory
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the backend files into the container
COPY backend ./backend

# Copy the frontend files into the container
COPY frontend ./frontend

# Navigate to the frontend directory
WORKDIR /app/frontend

# Install frontend dependencies and build the app
RUN npm install
RUN npm audit fix
RUN npm run build

# Return to the backend directory to run the app
WORKDIR /app/backend

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout", "600", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
