"""
Three raw downloads are too large for the repository (EIA INTL.zip ~24 MB; UNCTAD US_RCA.7z ~9 MB,
125 MB unpacked; UNCTAD US_TermsOfTrade.7z). This script re-creates the small extracts that are committed
and used by build_dataset.py. Re-download the archives from the URLs in data/SOURCES.md, place them in
data/raw/eia and data/raw/unctad, then run:  python src/extract_large_raw.py
"""
from pathlib import Path
import zipfile

import pandas as pd
import py7zr

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

# EIA: petroleum and other liquids consumption (series INTL.5-2-<country>-TBPD.A) for all countries
with zipfile.ZipFile(RAW / "eia" / "INTL.zip") as z, z.open("INTL.txt") as f, \
        open(RAW / "eia" / "EIA_INTL_petroleum_consumption_all_countries_TBPD_A.jsonl", "w") as out:
    for raw_line in f:
        line = raw_line.decode("utf-8")
        if '"series_id":"INTL.5-2-' in line and '-TBPD.A"' in line:
            out.write(line)

# UNCTAD: India rows of the RCA and terms-of-trade bulk files
for archive, extract in [("US_RCA.7z", "UNCTAD_US_RCA_India_extract.csv"),
                         ("US_TermsOfTrade.7z", "UNCTAD_US_TermsOfTrade_India_extract.csv")]:
    with py7zr.SevenZipFile(RAW / "unctad" / archive) as z:
        z.extractall(path=RAW / "unctad" / "extracted")
    csv = RAW / "unctad" / "extracted" / archive.replace(".7z", ".csv")
    df = pd.read_csv(csv, dtype=str)
    df[df["Economy Label"].eq("India")].to_csv(RAW / "unctad" / extract, index=False)
print("extracts written")
