import pandas as pd


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/superheroes_clean.csv")


print("==========================================")
print("FEATURE DIAGNOSTIC")
print("==========================================")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nAll dataset columns:")
print("------------------------------------------")

for i, column in enumerate(df.columns, start=1):
    print(i, ".", column)


# ==========================================
# 2. ANALYZE EACH FEATURE
# ==========================================

print("\n==========================================")
print("FEATURE DETAILS")
print("==========================================")

for column in df.columns:

    unique_values = df[column].nunique(dropna=True)

    missing_values = df[column].isna().sum()

    print(
        f"{column:25} "
        f"unique={unique_values:5} "
        f"missing={missing_values:5}"
    )


# ==========================================
# 3. CURRENTLY USED FEATURES
# ==========================================

used_features = [

    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Creator",

    "Combat",
    "Durability",
    "Intelligence",
    "Power",
    "Speed",
    "Strength"
]


# ==========================================
# 4. UNUSED FEATURES
# ==========================================

unused_features = [

    column
    for column in df.columns
    if column not in used_features
]


print("\n==========================================")
print("CURRENTLY USED FEATURES")
print("==========================================")

for feature in used_features:
    print("-", feature)


print("\n==========================================")
print("UNUSED FEATURES")
print("==========================================")

for feature in unused_features:
    print("-", feature)


print("\nTotal used features:", len(used_features))
print("Total unused features:", len(unused_features))