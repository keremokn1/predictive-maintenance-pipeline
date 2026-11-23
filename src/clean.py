import pandas as pd
from pathlib import Path

INCOMING_DIR = Path("data/incoming")
CLEAN_DIR = Path("data/processed/clean")
QUARANTINE_DIR = Path("data/processed/quarantine")

# Orijinal sütun adı -> sade sütun adı
COLUMN_NAMES = {
    "UDI": "udi",
    "Product ID": "product_id",
    "Type": "type",
    "Air temperature [K]": "air_temp_k",
    "Process temperature [K]": "process_temp_k",
    "Rotational speed [rpm]": "rotational_speed_rpm",
    "Torque [Nm]": "torque_nm",
    "Tool wear [min]": "tool_wear_min",
    "Machine failure": "machine_failure",
    "TWF": "twf",
    "HDF": "hdf",
    "PWF": "pwf",
    "OSF": "osf",
    "RNF": "rnf",
}
FAILURE_MODES = ["twf", "hdf", "pwf", "osf", "rnf"]


def check_columns(df):
    """Dosya seviyesi kontrol: Beklenen sütunların hepsi var mı?
    Eksik sütun varsa ValueError fırlat, dosyanın tamamı reddedilsin."""
    for col in COLUMN_NAMES:
        if col not in df.columns:
            raise ValueError(f"Eksik sütun: {col}")
        



def add_quarantine_reasons(df):
    """Satır seviyesi kontrol: Her satıra bir 'quarantine_reason' sütunu ekler.
    Sorunsuz satırlarda bu sütun boş ("") kalır."""
    df["quarantine_reason"] = ""

    mode_sum = df[FAILURE_MODES].sum(axis=1)
    failure_mismatch = (
        ((df["machine_failure"] == 1) & (mode_sum == 0)) |
        ((df["machine_failure"] == 0) & (mode_sum > 0))
    )

    df.loc[failure_mismatch, "quarantine_reason"] = "failure_flag_mismatch"

    missing = df.isna().any(axis=1)
    df.loc[missing, "quarantine_reason"] = "missing_value"
    
    return df


def clean_file(path):
    df = pd.read_csv(path)
    check_columns(df)
    df = df.rename(columns=COLUMN_NAMES)
    df["strain_minnm"] = df["torque_nm"] * df["tool_wear_min"]
    df = add_quarantine_reasons(df)

    is_bad = df["quarantine_reason"] != ""
    clean = df[~is_bad].drop(columns="quarantine_reason")
    quarantine = df[is_bad]
    return clean, quarantine


def main():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    total_clean = 0
    total_quarantine = 0
    rejected = 0

    for path in sorted(INCOMING_DIR.glob("day_*.csv")):
        try:
            clean, quarantine = clean_file(path)
        except ValueError as e:
            print(f"REDDEDİLDİ: {path.name} -> {e}")
            rejected += 1
            continue

        clean.to_csv(CLEAN_DIR / path.name, index=False)
        quarantine.to_csv(QUARANTINE_DIR / path.name, index=False)
        total_clean += len(clean)
        total_quarantine += len(quarantine)

    print(f"Temiz: {total_clean}, Karantina: {total_quarantine}, Reddedilen dosya: {rejected}")


if __name__ == "__main__":
    main()