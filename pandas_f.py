import pandas as pd
import numpy as np

def print_section(title):
    print("\n" + "="*40)
    print(title)
    print("="*40)

# --- DataFrameの基本 ---
print_section("DataFrameの基本")

data = {
    "名前": ["田中", "佐藤", "鈴木", "高橋"],
    "年齢": [25, 30, 35, 40],
    "得点": [80, 90, np.nan, 70]
}
df = pd.DataFrame(data)
print(df)

# --- 基本情報 ---
print_section("基本情報")

print("列:", df.columns)
print("インデックス:", df.index)
print("データ型:\n", df.dtypes)
print("要約統計量:\n", df.describe())

# --- データ抽出 ---
print_section("データ抽出")

print("1列目（名前）:\n", df["名前"])
print("行と列指定（loc）:\n", df.loc[0, "年齢"])
print("位置指定（iloc）:\n", df.iloc[1, 2])

# --- 条件抽出 ---
print_section("条件抽出")

print("年齢>=30の人:\n", df[df["年齢"] >= 30])

# --- 欠損値処理 ---
print_section("欠損値処理")

print("欠損値の有無:\n", df.isnull())
print("欠損値の有無:\n", df.notnull())
df_filled = df.fillna(df["得点"].mean())
print("平均で補完:\n", df_filled)

# --- 列の追加・削除 ---
print_section("列の追加・削除")

df["合格"] = df["得点"] >= 75
print("列追加:\n", df)
df_dropped = df.drop("合格", axis=1)
print("列削除:\n", df_dropped)

# --- 並び替え ---
print_section("並び替え")

print("年齢順ソート(降順):\n", df.sort_values("年齢", ascending=False))
print("年齢順ソート(昇順):\n", df.sort_values("年齢", ascending=True))

# --- グループ化と集計 ---
print_section("グループ化と集計")

data2 = {
    "部署": ["A", "A", "B", "B", "C"],
    "得点": [80, 90, 70, 60, 100]
}
df2 = pd.DataFrame(data2)
print("部署ごとの平均:\n", df2.groupby("部署")["得点"].mean())
print("部署ごとの平均と最大値:\n", df2.groupby("部署")["得点"].agg(["mean", "max"]))

# --- 結合 ---
print_section("結合")

df_left = pd.DataFrame({"ID": [1, 2, 3], "名前": ["田中", "佐藤", "鈴木"]})
df_right = pd.DataFrame({"ID": [2, 3, 4], "得点": [80, 90, 100]})

# 内部結合（inner join）
merged_inner = pd.merge(df_left, df_right, on="ID", how="inner")
print("内部結合 (inner join):\n", merged_inner)

# 左外部結合（left join）
merged_left = pd.merge(df_left, df_right, on="ID", how="left")
print("左外部結合 (left join):\n", merged_left)

# 右外部結合（right join）
merged_right = pd.merge(df_left, df_right, on="ID", how="right")
print("右外部結合 (right join):\n", merged_right)

# 完全外部結合（outer join）
merged_outer = pd.merge(df_left, df_right, on="ID", how="outer")
print("完全外部結合 (outer join):\n", merged_outer)

# --- CSV入出力 ---
print_section("CSV入出力")

# 実際に保存・読み込みする場合はコメントアウトを外す
# df.to_csv("sample.csv", index=False)
# df_loaded = pd.read_csv("sample.csv")
# print(df_loaded.head())
print("（CSVの入出力はコメントアウト済み）")
