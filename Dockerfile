FROM python:3.10-slim

# Install ffmpeg
RUN apt update && apt install -y ffmpeg

# Set work directory
WORKDIR /app

# Copy semua file
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Jalankan Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]
