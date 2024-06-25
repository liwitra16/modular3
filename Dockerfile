# Gunakan image dasar dari Python
FROM python:3.12-slim

# Install dependencies sistem yang diperlukan
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setel direktori kerja di dalam container
WORKDIR /app

# Salin requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh isi proyek ke dalam container
COPY . .

# Setel environment variable untuk Flask
ENV FLASK_APP=app.py

# Expose port yang digunakan oleh Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["flask", "run", "--host=0.0.0.0"]
