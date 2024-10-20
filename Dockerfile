# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias necesarias para Kivy y X11
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libgles2-mesa \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    xvfb \
    libx11-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxcomposite-dev \
    libasound2-dev \
    libxi-dev \
    libxss-dev \
    libxtst-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos del proyecto
WORKDIR /app
COPY . /app

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Configurar las variables de entorno necesarias para Kivy
ENV KIVY_METRICS_DENSITY=1.0
ENV DISPLAY=:0

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
