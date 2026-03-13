# 現在整備中。今後更新予定。

# NDportfolio-001

## 概要

これはNDの取り組みとして作成した成果物のポートフォリオです。

## データソース

データは以下のサイトから取得しています。

- [e-Stat](https://www.e-stat.go.jp/)\
  元データは`data/raw`に格納、Git管理対象外(.gitignore)。\
  詳細は`data/raw`のREADMEを確認してください。

## 環境

Python 3.12.12

## 主に使用するライブラリ

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- statsmodels

## Install dependencies

```
`pip install -r requirements.txt`
```

## ディレクトリ階層

```
NDportfolio-001
├── README.md
├── LICENSE
├── requirements.txt
├── .python-version
├── data
│   ├── processed
│   └── raw
├── notebooks
├── reports
│   ├── figures
│   └── tables
├── src
└── tableau
```

## Tableauダッシュボード

https://public.tableau.com/app/profile/rin.sato5926/vizzes

## 再現手順

1. リポジトリのクローン\
   `git clone <repository-url>`\
   `cd NDportfolio-001`
1. pythonのインストール\
   `pyenv install 3.12.12`\
   `pyenv local 3.12.12`
1. 仮想環境構築\
   `python -m venv .venv`\
   `source .venv/bin/activate`
1. 依存関係のインストール\
   `pip install -r requirements.txt`
1. Run analysis\
   Open notebooks in `notebooks/`.
