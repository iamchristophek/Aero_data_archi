-- Schémas de la plateforme cœur
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS raw_vault;
CREATE SCHEMA IF NOT EXISTS business_vault;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS audit;

-- Traçabilité : un enregistrement par chargement d'interface
CREATE TABLE IF NOT EXISTS audit.load_log (
    load_id       BIGSERIAL PRIMARY KEY,
    interface     TEXT        NOT NULL,
    source_file   TEXT        NOT NULL,
    nb_lignes     INTEGER,
    statut        TEXT        NOT NULL CHECK (statut IN ('EN_COURS', 'OK', 'KO')),
    message       TEXT,
    debut_ts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    fin_ts        TIMESTAMPTZ
);
