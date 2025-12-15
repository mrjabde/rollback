FROM python:3.9-slim

WORKDIR /app

# Installe Flask
RUN pip install flask

COPY app.py .

# Argument de build pour définir la version (1 ou 2)
ARG VER=1
ENV APP_VERSION=$VER

CMD ["python", "app.py"]