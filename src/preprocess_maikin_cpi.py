from pathlib import Path
import re
import pandas as pd

ANNUAL_MONTH = 99
BASE_YEAR = 2019

MAIKIN_INDUSTRY_MAP = {
    'TL  ': '調査産業計',
    'C   ': '鉱業，採石業，砂利採取業',
    'D   ': '建設業',
    'E   ': '製造業',
    'F   ': '電気・ガス・熱供給・水道業',
    'G   ': '情報通信業',
    'H   ': '運輸業，郵便業',
    'I   ': '卸売業，小売業',
    'J   ': '金融業，保険業',
    'K   ': '不動産業，物品賃貸業',
    'L   ': '学術研究，専門・技術サービス業',
    'M   ': '宿泊業，飲食サービス業',
    'N   ': '生活関連サービス業，娯楽業',
    'O   ': '教育，学習支援業',
    'P   ': '医療，福祉',
    'Q   ': '複合サービス事業',
    'R   ': 'サービス業(他に分類されないもの)',
}

MAIKIN_SIZE_MAP = {
    '0': '30人以上',
    '4': '500人以上',
    '5': '100〜499人',
    '7': '30〜99人',
    '9': '5〜29人',
    'T': '5人以上',
}

MAIKIN_EMPLOYMENT_MAP = {
    0: '形態計',
    1: '一般',
    2: 'パート',
}

MAIKIN_KEEP_COLS = [
    '年', '月', '産業分類', '規模', '就業形態',
    '現金給与総額', 'きまって支給する給与', '所定内給与', '所定外給与', '特別給与',
    '総実労働時間', '所定内労働時間', '所定外労働時間',
    '出勤日数', '前月末労働者数', '増加労働者数', '減少労働者数',
    '本月末労働者数', 'パートタイム労働者数'
]

INDEX_BASE_COLS = [
    '現金給与総額', 'きまって支給する給与', '所定内給与', '所定外給与', '特別給与',
    '総実労働時間', '所定内労働時間', '所定外労働時間'
]

MAIKIN_FINAL_COLS = [
    '年', '月', '規模', '就業形態',
    '現金給与総額', 'きまって支給する給与', '所定内給与', '所定外給与', '特別給与',
    '総実労働時間', '所定内労働時間', '所定外労働時間',
    '前月末労働者数', '本月末労働者数', 'パートタイム労働者数',
    '現金給与総額指数', 'きまって支給する給与指数', '所定内給与指数',
    '所定外給与指数', '特別給与指数', '総実労働時間指数',
    '所定内労働時間指数', '所定外労働時間指数'
]

REAL_TARGET_COLS = [
    '現金給与総額指数', 'きまって支給する給与指数', '所定内給与指数',
    '所定外給与指数', '特別給与指数',
    '現金給与総額', 'きまって支給する給与', '所定内給与',
    '所定外給与', '特別給与'
]


def load_maikin(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding='shift-jis')


def clean_maikin_codes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['月'] = df['月'].replace({'CY': ANNUAL_MONTH}).astype(int)
    df['産業分類'] = df['産業分類'].replace(MAIKIN_INDUSTRY_MAP)
    df['規模'] = df['規模'].replace(MAIKIN_SIZE_MAP)
    df['就業形態'] = df['就業形態'].replace(MAIKIN_EMPLOYMENT_MAP)
    return df


def prepare_maikin(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.filter(MAIKIN_KEEP_COLS)
    df = df.query('産業分類 == "調査産業計"').reset_index(drop=True)
    return df


def build_base_2019(df: pd.DataFrame) -> pd.DataFrame:
    base = (
        df.query('年 == @BASE_YEAR and 月 == @ANNUAL_MONTH')
          .filter(['産業分類', '規模', '就業形態'] + INDEX_BASE_COLS)
          .rename(columns={col: f'{col}_{BASE_YEAR}' for col in INDEX_BASE_COLS})
    )

    if base.duplicated(['産業分類', '規模', '就業形態']).any():
        raise ValueError('基準年データが一意ではありません。')

    return base


def add_index_columns(df: pd.DataFrame, base: pd.DataFrame) -> pd.DataFrame:
    merged = df.merge(base, on=['産業分類', '規模', '就業形態'], how='left')

    for col in INDEX_BASE_COLS:
        base_col = f'{col}_{BASE_YEAR}'
        if merged[base_col].isna().any():
            raise ValueError(f'{base_col} に欠損があります。')
        merged[f'{col}指数'] = merged[col] / merged[base_col] * 100

    return merged


def finalize_maikin(df: pd.DataFrame) -> pd.DataFrame:
    return df.filter(MAIKIN_FINAL_COLS)


def load_cpi(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding='shift-jis')


def parse_year_month(value: str) -> tuple[int | None, int | None]:
    value = str(value)

    m = re.fullmatch(r'(\d{4})年(\d{1,2})月', value)
    if m:
        return int(m.group(1)), int(m.group(2))

    m = re.fullmatch(r'(\d{4})年', value)
    if m:
        return int(m.group(1)), ANNUAL_MONTH

    return None, None


def prepare_cpi(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.filter(['時間軸（年・月）', 'value'])
    df[['年', '月']] = df['時間軸（年・月）'].apply(lambda x: pd.Series(parse_year_month(x)))

    if df[['年', '月']].isna().any().any():
        raise ValueError('CPIの年月パースに失敗した行があります。')

    df = (
        df.sort_values(['年', '月'])
          .reset_index(drop=True)
          .filter(['年', '月', 'value'])
          .rename(columns={'value': 'CPI(持ち家除く総合)'})
    )
    return df


def merge_maikin_cpi(df_maikin: pd.DataFrame, df_cpi: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(df_maikin, df_cpi, on=['年', '月'], how='left')

    if df['CPI(持ち家除く総合)'].isna().any():
        raise ValueError('毎勤とCPIの結合後にCPI欠損があります。')

    return df


def add_real_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cpi = df['CPI(持ち家除く総合)']

    for col in REAL_TARGET_COLS:
        df[f'実質_{col}'] = df[col] / cpi * 100

    return df


def build_dataset(maikin_path: str | Path, cpi_path: str | Path) -> pd.DataFrame:
    df_maikin = load_maikin(maikin_path)
    df_maikin = clean_maikin_codes(df_maikin)
    df_maikin = prepare_maikin(df_maikin)
    base_2019 = build_base_2019(df_maikin)
    df_maikin = add_index_columns(df_maikin, base_2019)
    df_maikin = finalize_maikin(df_maikin)

    df_cpi = load_cpi(cpi_path)
    df_cpi = prepare_cpi(df_cpi)

    df = merge_maikin_cpi(df_maikin, df_cpi)
    df = add_real_columns(df)
    return df


def save_dataset(df: pd.DataFrame, output_path: str | Path) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')