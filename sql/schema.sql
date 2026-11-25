-- Temiz sensör kayıtları
CREATE TABLE IF NOT EXISTS sensor_readings (
    udi                  INTEGER PRIMARY KEY,
    product_id           TEXT,
    type                 TEXT CHECK (type IN ('L', 'M', 'H')),
    air_temp_k           DOUBLE PRECISION,
    process_temp_k       DOUBLE PRECISION,
    rotational_speed_rpm INTEGER,
    torque_nm            DOUBLE PRECISION,
    tool_wear_min        INTEGER,
    machine_failure      INTEGER CHECK (machine_failure IN (0, 1)),
    twf                  INTEGER,
    hdf                  INTEGER,
    pwf                  INTEGER,
    osf                  INTEGER,
    rnf                  INTEGER,
    strain_minnm         DOUBLE PRECISION,
    source_file          TEXT
);

-- Karantinaya alınan kayıtlar
CREATE TABLE IF NOT EXISTS quarantine (
    udi                  INTEGER PRIMARY KEY,
    product_id           TEXT,
    type                 TEXT,
    air_temp_k           DOUBLE PRECISION,
    process_temp_k       DOUBLE PRECISION,
    rotational_speed_rpm INTEGER,
    torque_nm            DOUBLE PRECISION,
    tool_wear_min        INTEGER,
    machine_failure      INTEGER,
    twf                  INTEGER,
    hdf                  INTEGER,
    pwf                  INTEGER,
    osf                  INTEGER,
    rnf                  INTEGER,
    strain_minnm         DOUBLE PRECISION,
    quarantine_reason    TEXT,
    source_file          TEXT
);

-- Hangi günlük dosyaların yüklendiği
CREATE TABLE IF NOT EXISTS processed_files (
    file_name       TEXT PRIMARY KEY,
    clean_rows      INTEGER,
    quarantine_rows INTEGER,
    processed_at    TIMESTAMP DEFAULT NOW()
);