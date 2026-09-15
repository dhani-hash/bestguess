import pandas as pd

from questions import ask_question


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/superheroes_clean.csv")


# ==========================================
# 2. GENERATE SAME 282 QUESTIONS
# ==========================================

categorical_features = [
    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Creator"
]

numeric_features = [
    "Combat",
    "Durability",
    "Intelligence",
    "Power",
    "Speed",
    "Strength"
]


questions = []


# Categorical questions
for feature in categorical_features:

    values = df[feature].dropna().unique()

    for value in values:

        questions.append({
            "feature": feature,
            "value": value,
            "type": "categorical"
        })


# Numeric questions
for feature in numeric_features:

    values = pd.to_numeric(
        df[feature],
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        continue

    thresholds = [
        values.quantile(0.25),
        values.quantile(0.50),
        values.quantile(0.75)
    ]

    for threshold in thresholds:

        questions.append({
            "feature": feature,
            "value": threshold,
            "type": "numeric"
        })


print("Questions:", len(questions))


# ==========================================
# 3. CREATE SIGNATURE FOR EACH ROW
# ==========================================

signatures = {}

for _, row in df.iterrows():

    row_dict = row.to_dict()

    signature = tuple(
        ask_question(row_dict, question)
        for question in questions
    )

    character = row_dict["Character"]

    if signature not in signatures:
        signatures[signature] = set()

    signatures[signature].add(character)


# ==========================================
# 4. ANALYZE COLLISIONS
# ==========================================

total_signatures = len(signatures)

colliding_signatures = 0
characters_in_collisions = 0

for signature, characters in signatures.items():

    if len(characters) > 1:

        colliding_signatures += 1
        characters_in_collisions += len(characters)


print("\n========== SIGNATURE ANALYSIS ==========")

print("Total rows:", len(df))
print("Unique signatures:", total_signatures)

print("Signatures containing multiple characters:",
      colliding_signatures)

print("Characters involved in collisions:",
      characters_in_collisions)