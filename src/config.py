from pathlib import Path

# プロジェクトルート
ROOT = Path(__file__).resolve().parents[1]

# データディレクトリ
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"

# 出力ディレクトリ
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"

# Tableau
TABLEAU = ROOT / "tableau"