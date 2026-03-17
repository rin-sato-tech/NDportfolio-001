# 現在整備中。今後更新予定。

# NDportfolio-001

## 概要

これはNDの取り組みとして作成した成果物のポートフォリオです。公的統計データを用いて、前処理・分析・可視化を行いました。\
現在のリポジトリでは、前処理ロジックは`src/`に実装し、Notebookは主に確認・検証・分析に使用します。

## このリポジトリで扱うもの

- 毎月勤労統計調査データの前処理
- CPI (消費者物価指数)との結合
- 賃金系列の指数化・実質化
- 加工済みデータの出力
- その後の分析・可視化

## データソース

データは主に政府統計ポータルe-Statから取得しています。
([e-Stat](https://www.e-stat.go.jp/))

- 毎月勤労統計調査
- 消費者物価指数 (CPI)
  `data/raw`には元データを配置します。\
  元データはGit管理対象外です。\

## 環境

Python 3.12.12

## 主に使用するライブラリ

- pandas

## 依存関係のインストール

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
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── preprocess_maikin_cpi.py
├── reports/
│   ├── figures/
│   └── tables/
└── tableau/
```

## 役割分担

`src/`
前処理ロジックの正本を置く場所です。\
CSV読込、整形、指数化、CPI結合、実質化、保存など、再現可能な処理はここに実装します。\
`notebooks/`
確認・検証・分析・可視化のための場所です。\
本番用の前処理ロジックはここに重複しでもたず、`src/`の関数を呼び出して使うことを前提とします。

## 実行方法

1. リポジトリのクローン
   ```
   git clone <repository-url>
   cd NDportfolio-001
   ```
1. pythonのインストール
   ```
   pyenv install 3.12.12
   pyenv local 3.12.12
   ```
1. 仮想環境構築
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
1. 依存関係のインストール
   ```
   pip install -r requirements.txt
   ```
1. 元データを配置\
   元データを`data/raw/`に配置してください。\
   例：
   - 毎月勤労統計調査のCSV
   - 消費者物価指数のCSV
1. 前処理を実行\
   前処理の正本は`src/preprocess_maikin_cpi.py`です。\
   プロジェクトルートで以下を実行します。
   ```
   python -m src.preprocess_maikin_cpi
   ```
1. Notebookで確認・分析
   前処理後は`notebooks/`のNotebookでデータ確認、分析、可視化を行います。

## 出力

加工済みデータは`data/processed/`に保存します。

## Tableauダッシュボード

Tableau用のファイルは`tableau/`で管理します。
公開ダッシュボード：

```
https://public.tableau.com/app/profile/rin.sato5926/vizzes
```

## 今後の改善予定

- READMEの充実
- Notebookの整理
- 分析テーマごとの前処理・分析コードの分割
- 可視化成果物の追加
