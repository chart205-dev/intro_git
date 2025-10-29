import numpy as np

def print_section(title):
    print("\n" + "="*40)
    print(title)
    print("="*40)

# --- 基本配列作成 ---
print_section("基本配列作成")

a = np.array([1, 2, 3])
b = np.arange(0, 10, 2)     # [0, 2, 4, 6, 8]
c = np.linspace(0, 1, 5)    # [0. , 0.25, 0.5 , 0.75, 1. ]

print("a:", a)
print("b:", b)
print("c:", c)

# --- 配列の形状操作 ---
print_section("配列の形状操作")

A = np.array([[1, 2, 3], [4, 5, 6]])
print("A shape:", A.shape)
print("A 転置:\n", A.T)

B = np.arange(1, 13, 1).reshape(3, 4)
print("B:\n", B)

# --- ブロードキャスト演算 ---
print_section("ブロードキャスト演算")

print("A + 10:\n", A + 10)
print("A + [10, 20, 30]:\n", A + np.array([10, 20, 30]))

# --- 要素ごとの計算 ---
print_section("要素ごとの計算")

print("A の2乗:\n", A ** 2)
print("A の平均:", A.mean())
print("A の標準偏差:", A.std())
print("A の分散:", A.var())
print("A の最大値:", A.max(), "位置:", A.argmax())
print("A の最大値:", A.min(), "位置:", A.argmin())

# --- 条件抽出 ---
print_section("条件抽出")

arr = np.array([10, 20, 30, 40, 50])
mask = arr > 25
print("arr > 25 の要素:", mask)
print("25より大きい要素:", arr[mask])
mask = arr < 25
print("arr < 25 の要素:", mask)
print("25より大きい要素:", arr[mask])
mask = arr == 20
print("arr == 25 の要素:", mask)
print("25より大きい要素:", arr[mask])

# --- 行列演算 ---
print_section("行列演算")

X = np.array([[1, 2], [3, 4]])
Y = np.array([[5, 6], [7, 8]])
print("行列和:\n", np.add(X, Y))  # または X + Y
print("行列積:\n", np.dot(X, Y))  # または X @ Y

# --- 疑似乱数 ---
print_section("疑似乱数")

np.random.seed(0)
rand_arr = np.random.randn(5)
print("標準正規分布から生成:", rand_arr)
