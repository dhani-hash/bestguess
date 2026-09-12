import csv


INPUT_FILE = "data/Superheroes.csv"
OUTPUT_FILE = "data/superheroes_clean.csv"


with open(INPUT_FILE, "r", encoding="utf-8") as file:

    data = list(csv.DictReader(file))


# Values that mean "unknown"
MISSING_VALUES = {
    "",
    "-",
    "None",
    "none",
    "N/A",
    "n/a"
}


cleaned_data = []


for row in data:

    clean_row = {}

    for column, value in row.items():

        value = value.strip()

        # Remove accidental header values
        if value == column:
            value = ""

        # Convert unknown values to empty
        if value in MISSING_VALUES:
            value = ""

        clean_row[column] = value

    cleaned_data.append(clean_row)


# Write cleaned dataset

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=data[0].keys()
    )

    writer.writeheader()

    writer.writerows(cleaned_data)


print("Cleaning complete.")
print("Original rows:", len(data))
print("Cleaned rows:", len(cleaned_data))
print("Saved to:", OUTPUT_FILE)