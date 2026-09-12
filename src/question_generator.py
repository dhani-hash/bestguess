import csv


INPUT_FILE = "data/superheroes_clean.csv"


# Features we want to turn into questions
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


with open(INPUT_FILE, "r", encoding="utf-8") as file:

    data = list(csv.DictReader(file))


questions = []


# -----------------------------------
# 1. Categorical features
# -----------------------------------

for feature in categorical_features:

    if feature not in data[0]:
        continue

    values = set()

    for row in data:

        value = row[feature].strip()

        if value != "":
            values.add(value)

    for value in values:

        questions.append({
            "feature": feature,
            "value": value,
            "type": "categorical"
        })


# -----------------------------------
# 2. Numeric features
# -----------------------------------

for feature in numeric_features:

    if feature not in data[0]:
        continue

    values = []

    for row in data:

        value = row[feature].strip()

        try:
            values.append(float(value))
        except ValueError:
            pass

    if len(values) == 0:
        continue

    # Use several threshold questions
    minimum = min(values)
    maximum = max(values)

    thresholds = [
        minimum + (maximum - minimum) * 0.25,
        minimum + (maximum - minimum) * 0.50,
        minimum + (maximum - minimum) * 0.75
    ]

    for threshold in thresholds:

        questions.append({
            "feature": feature,
            "value": threshold,
            "type": "numeric"
        })


# -----------------------------------
# Display questions
# -----------------------------------

print("TOTAL QUESTIONS GENERATED:", len(questions))

print()
print("FIRST 50 QUESTIONS")
print("==================")

for question in questions[:50]:

    if question["type"] == "categorical":

        print(
            f"Is {question['feature']} = "
            f"{question['value']}?"
        )

    else:

        print(
            f"Is {question['feature']} >= "
            f"{question['value']:.1f}?"
        )