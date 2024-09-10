-- Active: 1725902722961@@127.0.0.1@5432@task
COPY task.document (text, create_date, rubrics)
FROM '/data/posts.csv' DELIMITER ','
CSV HEADER;

CREATE SCHEMA IF NOT EXISTS task;

CREATE TABLE IF NOT EXISTS task.document (
    id SERIAL NOT NULL,
    text TEXT NOT NULL,
    create_date DATE NOT NULL,
    rubrics VARCHAR(30)[] NOT NULL,
    
    PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS document_text_idx
ON task.document
USING GIN (to_tsvector('russian', text));


CREATE TABLE IF NOT EXISTS task.document (
    id SERIAL NOT NULL,
    text VARCHAR(255) NOT NULL,
    create_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS task.rubric (
    id VARCHAR(30) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS task.document_rubric (
    document_id INTEGER NOT NULL,
    rubric_id VARCHAR(30) NOT NULL,
    PRIMARY KEY (document_id, rubric_id),
    FOREIGN KEY (document_id) REFERENCES task.document(id),
    FOREIGN KEY (rubric_id) REFERENCES task.rubric(id)
);