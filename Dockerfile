FROM python

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY config.yaml /app/
COPY database/init.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER=usr
ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_DB=task

RUN /bin/bash -c "\
    service postgresql start && \
    su - postgres -c \"psql -c 'CREATE USER $POSTGRES_USER WITH PASSWORD '\''$POSTGRES_PASSWORD'\'';'\" && \
    su - postgres -c \"psql -c 'CREATE DATABASE $POSTGRES_DB;'\" && \
    su - postgres -c \"psql -c 'GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;'\" && \
    su - postgres -c \"psql -d $POSTGRES_DB -a -f /docker-entrypoint-initdb.d/init.sql\" && \
    service postgresql stop"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
