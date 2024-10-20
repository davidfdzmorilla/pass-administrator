# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias necesarias para Kivy, X11 y Mesa3D para renderizado por software
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
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
    libmtdev1 \
    xclip \
    xsel \
    && rm -rf /var/lib/apt/lists/*  

# Copiar los archivos del proyecto
WORKDIR /app
COPY . /app

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Configurar las variables de entorno necesarias para Kivy y renderizado por software
ENV KIVY_METRICS_DENSITY=1.0
ENV DISPLAY=:0
ENV LIBGL_ALWAYS_SOFTWARE=1

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
