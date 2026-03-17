from pathlib import Path

# プロジェクトルート
ROOT = Path(__file__).resolve().parents[1]

# データディレクトリ
DATA_DIR = ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# 出力ディレクトリ
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

# Tableau
TABLEAU_DIR = ROOT / "tableau"

MAIKIN_RAW = DATA_RAW_DIR / "hon-maikin-k-jissu.csv"
CPI_RAW = DATA_RAW_DIR / "FEH_00200573_260317110412.csv"
MAIKIN_CPI_OUTPUT = DATA_PROCESSED_DIR / "maikin_cpi.csv"

DIRS_TO_CREATE = [
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    TABLEAU_DIR,
]

def ensure_dirs() -> None:
    for path in DIRS_TO_CREATE:
        path.mkdir(parents=True, exist_ok=True)