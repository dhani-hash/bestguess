import csv

with open("data/Superheroes.csv", "r", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

columns = list(data[0].keys())

print("================================")
print("DATASET INFORMATION")
print("================================")

print("Rows:", len(data))
print("Columns:", len(columns))

print("\nCOLUMN DETAILS")
print("--------------------------------")

for column in columns:

    values = [row[column].strip() for row in data]

    non_empty = [value for value in values if value != ""]

    unique_values = set(non_empty)

    print(
        column,
        "| unique:", len(unique_values),
        "| empty:", len(values) - len(non_empty)
    )

print("\n================================")
print("TARGET INFORMATION")
print("================================")

target = "Character"

characters = set(
    row[target].strip()
    for row in data
    if row[target].strip() != ""
)

print("Unique characters:", len(characters))

print("\nFirst 30 characters:")

for character in list(characters)[:30]:
    print(character)
    