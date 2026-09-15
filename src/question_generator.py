import csv


INPUT_FILE = "data/superheroes_clean.csv"


# ==========================================
# FEATURES
# ==========================================

categorical_features = [
    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Creator",
    "Tier",
    "Level"
]


numeric_features = [
    "Combat",
    "Durability",
    "Intelligence",
    "Power",
    "Speed",
    "Strength",
    "IQ",
    "Speed_velocity",
    "Strength_force"
]


# ==========================================
# LOAD DATASET
# ==========================================

with open(INPUT_FILE, "r", encoding="utf-8") as file:

    data = list(
        csv.DictReader(file)
    )


questions = []


# ==========================================
# 1. CATEGORICAL QUESTIONS
# ==========================================

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


# ==========================================
# 2. NUMERIC QUESTIONS
# ==========================================

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


    if len(values) < 2:
        continue


    # --------------------------------------
    # Get unique actual values
    # --------------------------------------

    unique_values = sorted(
        set(values)
    )


    if len(unique_values) < 2:
        continue


    # --------------------------------------
    # Create boundaries between actual values
    #
    # Example:
    #
    # 100, 120
    #
    # boundary = 110
    #
    # --------------------------------------

    candidate_thresholds = []

    for i in range(
        len(unique_values) - 1
    ):

        left = unique_values[i]

        right = unique_values[i + 1]


        threshold = (
            left + right
        ) / 2


        candidate_thresholds.append(
            threshold
        )


    # --------------------------------------
    # Too many possible thresholds
    #
    # Keep a manageable number spread
    # across the complete numeric range.
    # --------------------------------------

    MAX_THRESHOLDS = 25


    if len(candidate_thresholds) > MAX_THRESHOLDS:

        step = (
            len(candidate_thresholds)
            / MAX_THRESHOLDS
        )


        selected_thresholds = []


        for i in range(MAX_THRESHOLDS):

            index = int(
                i * step
            )

            selected_thresholds.append(
                candidate_thresholds[index]
            )


        candidate_thresholds = (
            selected_thresholds
        )


    # --------------------------------------
    # Create numeric questions
    # --------------------------------------

    for threshold in candidate_thresholds:

        questions.append({

            "feature": feature,

            "value": threshold,

            "type": "numeric"

        })


# ==========================================
# DISPLAY RESULT
# ==========================================

print(
    "TOTAL QUESTIONS GENERATED:",
    len(questions)
)


print()

print(
    "FIRST 50 QUESTIONS"
)

print(
    "=================="
)


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