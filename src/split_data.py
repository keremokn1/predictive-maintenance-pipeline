import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/ai4i2020.csv")
OUTPUT_DIR = Path("data/incoming")
ROWS_PER_DAY = 100


def main():
    df = pd.read_csv(RAW_FILE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    day = 0
    for start in range(0, len(df), ROWS_PER_DAY):
        day += 1
        chunk = df.iloc[start:start + ROWS_PER_DAY]
        chunk.to_csv(OUTPUT_DIR / f"day_{day:03d}.csv", index=False)

    print(f"{day} günlük dosya oluşturuldu.")


if __name__ == "__main__":
    main()