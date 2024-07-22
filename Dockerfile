
FROM python:3.9-slim

# Instala PostgreSQL y otras dependencias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    libpq-dev \
    python3-dev \
    curl \
    netcat-openbsd
ENV PYTHONUNBUFFERED=1

RUN curl -o /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for && \
    chmod +x /usr/local/bin/wait-for

# Copia y hace ejecutable el script entrypoint.sh
COPY --link ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
WORKDIR /LidzTest

# Copia los archivos de requerimientos y los instala
COPY requirements.txt /LidzTest/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /LidzTest/

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]