# Use an official Nginx image as the base image
FROM nginx:latest
# Remove any existing config files
RUN rm /etc/nginx/conf.d/*
# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/
# Expose port 80 for Nginx
# Instala PostgreSQL y otras dependencias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    libpq-dev \
    python3-dev \
    curl \
    netcat-openbsd
EXPOSE 80