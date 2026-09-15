import pandas as pd

from questions import ask_question


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/superheroes_clean.csv")


# ==========================================
# 2. GENERATE QUESTIONS
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


for feature in categorical_features:

    values = df[feature].dropna().unique()

    for value in values:

        questions.append({
            "feature": feature,
            "value": value,
            "type": "categorical"
        })


for feature in numeric_features:

    values = pd.to_numeric(
        df[feature],
        errors="coerce"
    ).dropna()

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
# 3. GROUP ROWS BY SIGNATURE
# ==========================================

signature_groups = {}


for _, row in df.iterrows():

    row_dict = row.to_dict()

    signature = tuple(
        ask_question(row_dict, question)
        for question in questions
    )

    character = row_dict["Character"]

    if signature not in signature_groups:
        signature_groups[signature] = []

    signature_groups[signature].append(character)


# ==========================================
# 4. FIND THEORETICAL BEST ACCURACY
# ==========================================

correct = 0

for signature, characters in signature_groups.items():

    counts = {}

    for character in characters:

        if character not in counts:
            counts[character] = 0

        counts[character] += 1

    # Best possible character for this signature
    best_character = max(
        counts,
        key=counts.get
    )

    # Number of rows we can correctly identify
    correct += counts[best_character]


accuracy = correct / len(df)


# ==========================================
# 5. RESULTS
# ==========================================

print("\n========== THEORETICAL UPPER BOUND ==========")

print("Total rows:", len(df))

print("Unique signatures:", len(signature_groups))

print("Maximum possible correct:", correct)

print(
    "Maximum possible accuracy:",
    accuracy * 100,
    "%"
)