import csv

with open("data/Superheroes.csv", "r", encoding="utf-8") as file:
    data = list(csv.DictReader(file))


# Features we are considering for Guess-Who questions

candidate_features = [
    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Universe",
    "Creator",
    "Combat",
    "Durability",
    "Intelligence",
    "Power",
    "Speed",
    "Strength",
    "Height",
    "Weight"
]


print("CANDIDATE FEATURES")
print("==================")

for feature in candidate_features:

    if feature not in data[0]:
        print(feature, "-> NOT FOUND")
        continue

    values = set()

    for row in data:
        value = row[feature].strip()

        if value != "":
            values.add(value)

    print()
    print(feature)
    print("Unique values:", len(values))
    print("Examples:", list(values)[:10])