







FROM apache/airflow:2.10.4-python3.11

USER root

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    software-properties-common \
    apt-transport-https \
    curl \
    wget \
    unzip \
    gcc \
    python3-dev \
    openjdk-17-jdk \
    && apt-get clean


# Utiliser une image de base Ubuntu
FROM ubuntu:22.04

# Définir les variables d'environnement pour éviter les questions interactives lors de l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    curl \
    xdg-utils \
    fonts-liberation \
    libasound2 \
    libgbm-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Ajouter la clé GPG et le dépôt officiel de Google Chrome
RUN wget -qO - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Installer la dernière version de Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Vérifier l'installation de Google Chrome
RUN google-chrome --version

# Installer ChromeDriver correspondant à la version de Google Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+' | cut -d '.' -f 1) && \
    echo "Chrome version: $CHROME_VERSION" && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    echo "ChromeDriver version: $DRIVER_VERSION" && \
    wget -q "https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Vérifier l'installation de ChromeDriver
RUN chromedriver --version


# Vérification des versions installées
RUN java -version && google-chrome --version && chromedriver --version

ENV JAVA_HOME /usr/lib/jvm/java11-openjdk-arm64




# debut
# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    curl \
    xdg-utils \
    fonts-liberation \
    libasound2 \
    libgbm-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Ajouter la clé GPG et le dépôt officiel de Google Chrome
RUN  apt-get update && \
     wget -qO - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
         echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Installer la dernière version de Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}') && \
    echo "Google Chrome version: $CHROME_VERSION"
# Vérifier l'installation de Google Chrome
RUN google-chrome --version

RUN wget https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.53/linux64/chromedriver-linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/chromedriver && \
    mv /tmp/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip  /tmp/chromedriver

# fin







USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark