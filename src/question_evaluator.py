import csv
from information_gain import information_gain


INPUT_FILE = "data/superheroes_clean.csv"


# ---------------------------------------
# Load dataset
# ---------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = list(csv.DictReader(file))


# ---------------------------------------
# Target
# ---------------------------------------

target = "Character"


# ---------------------------------------
# Candidate questions
# ---------------------------------------

categorical_features = [
    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Creator"
]


questions = []


# ---------------------------------------
# Generate categorical questions
# ---------------------------------------

for feature in categorical_features:

    values = set()

    for row in data:

        value = row[feature].strip()

        if value != "":
            values.add(value)

    for value in values:

        questions.append({
            "feature": feature,
            "value": value
        })


# ---------------------------------------
# Evaluate questions
# ---------------------------------------

results = []


for question in questions:

    feature = question["feature"]
    value = question["value"]

    question_answers = []
    characters = []

    for row in data:

        # Answer to question
        if row[feature].strip() == value:
            answer = 1
        else:
            answer = 0

        question_answers.append(answer)
        characters.append(row[target])

    gain = information_gain(
        characters,
        question_answers
    )

    results.append({
        "question": f"{feature} = {value}",
        "gain": gain
    })


# ---------------------------------------
# Sort by information gain
# ---------------------------------------

results.sort(
    key=lambda x: x["gain"],
    reverse=True
)


# ---------------------------------------
# Display best questions
# ---------------------------------------

print("BEST QUESTIONS")
print("================")

for result in results[:20]:

    print(
        result["question"],
        "→ Information Gain:",
        result["gain"]
    )