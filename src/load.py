import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

CLEAN_DIR = Path("data/processed/clean")
QUARANTINE_DIR = Path("data/processed/quarantine")


def get_engine():
    """Veritabanına bağlantı kurar. Bilgileri .env dosyasından okur."""
    load_dotenv()
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    port = os.getenv("DB_PORT", "5432")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{db}")


def get_processed_files(engine):
    """Daha önce yüklenmiş dosyaların adlarını döndürür."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT file_name FROM processed_files"))
        return {row[0] for row in result}


def load_file(engine, path):
    """Tek bir günün temiz ve karantina verisini yükler."""
    clean = pd.read_csv(path)
    quarantine = pd.read_csv(QUARANTINE_DIR / path.name)
    clean["source_file"] = path.name
    quarantine["source_file"] = path.name

    with engine.begin() as conn:
        clean.to_sql("sensor_readings", conn, if_exists="append", index=False)
        quarantine.to_sql("quarantine", conn, if_exists="append", index=False)
        conn.execute(
            text("INSERT INTO processed_files (file_name, clean_rows, quarantine_rows) "
                 "VALUES (:file, :clean, :quarantine)"),
            {"file": path.name, "clean": len(clean), "quarantine": len(quarantine)},
        )


def main():
    engine = get_engine()
    already_loaded = get_processed_files(engine)

    loaded = 0
    skipped = 0
    failed = 0

    for path in sorted(CLEAN_DIR.glob("day_*.csv")):
        if path.name in already_loaded:
            skipped += 1
            continue

        try:
            load_file(engine, path)
        except Exception as e:
            print(f"HATA: {path.name} -> {e}")
            failed += 1
            continue

        loaded += 1

    print(f"Yüklenen: {loaded}, Atlanan (zaten yüklü): {skipped}, Hatalı: {failed}")


if __name__ == "__main__":
    main()