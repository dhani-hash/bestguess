import pandas as pd
from collections import defaultdict, Counter


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/superheroes_clean.csv")


# ==========================================
# 2. FEATURES
# ==========================================

features = [
    "Alignment",
    "Gender",
    "Eye_color",
    "Hair_color",
    "Species",
    "Creator",
    "Tier",
    "Level",
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
# 3. SAME TRAIN / TEST SPLIT
# ==========================================

train_data = []
test_data = []

for character, group in df.groupby("Character"):

    rows = group.to_dict("records")

    if len(rows) >= 2:

        train_data.extend(rows[:-1])
        test_data.append(rows[-1])


print("==========================================")
print("TEST-SET SIGNATURE ANALYSIS")
print("==========================================")

print("Total dataset rows:", len(df))
print("Training rows:", len(train_data))
print("Testing rows:", len(test_data))
print("Features used:", len(features))


# ==========================================
# 4. CREATE SIGNATURE
# ==========================================

def create_signature(row):

    signature = []

    for feature in features:

        value = row.get(feature, "")

        if pd.isna(value):
            value = ""

        value = str(value).strip()

        # Normalize missing values
        if value == "":
            value = "<MISSING>"

        signature.append(value)

    return tuple(signature)


# ==========================================
# 5. BUILD TRAINING SIGNATURE MAP
# ==========================================

signature_to_characters = defaultdict(list)

for row in train_data:

    signature = create_signature(row)

    character = row["Character"]

    signature_to_characters[signature].append(character)


# ==========================================
# 6. FIND BEST POSSIBLE PREDICTION
# ==========================================

correct_upper_bound = 0

unknown_signatures = 0

collision_signatures = 0


for row in test_data:

    signature = create_signature(row)

    possible_characters = signature_to_characters.get(
        signature,
        []
    )

    # No training character has this signature
    if len(possible_characters) == 0:

        unknown_signatures += 1

        continue


    counts = Counter(possible_characters)

    best_character, best_count = counts.most_common(1)[0]

    correct_upper_bound += best_count / len(possible_characters)


# ==========================================
# 7. COUNT COLLISIONS
# ==========================================

for signature, characters in signature_to_characters.items():

    unique_characters = set(characters)

    if len(unique_characters) > 1:

        collision_signatures += 1


# ==========================================
# 8. CALCULATE UPPER BOUND
# ==========================================

upper_bound_accuracy = (
    correct_upper_bound
    / len(test_data)
) * 100


# ==========================================
# 9. RESULTS
# ==========================================

print()
print("==========================================")
print("SIGNATURE RESULTS")
print("==========================================")

print(
    "Unique training signatures:",
    len(signature_to_characters)
)

print(
    "Training signatures with collisions:",
    collision_signatures
)

print(
    "Test signatures unseen during training:",
    unknown_signatures
)

print(
    "Maximum possible accuracy:",
    upper_bound_accuracy,
    "%"
)

print()
print("==========================================")
print("ANALYSIS COMPLETE")
print("==========================================")