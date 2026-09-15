import pandas as pd


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(
    "data/superheroes_clean.csv"
)


# ==========================================
# 2. ALL 17 FEATURES
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


features = (
    categorical_features
    + numeric_features
)


# ==========================================
# 3. CREATE FEATURE SIGNATURE
# ==========================================

def create_signature(row):

    signature = []

    for feature in features:

        value = row[feature]

        # ------------------------------
        # Missing value
        # ------------------------------

        if pd.isna(value) or str(value).strip() == "":
            signature.append("MISSING")

        else:
            signature.append(
                str(value).strip()
            )

    return tuple(signature)


# ==========================================
# 4. GROUP ROWS BY SIGNATURE
# ==========================================

signature_groups = {}


for _, row in df.iterrows():

    signature = create_signature(row)

    character = row["Character"]

    if signature not in signature_groups:

        signature_groups[signature] = set()

    signature_groups[signature].add(
        character
    )


# ==========================================
# 5. BASIC STATISTICS
# ==========================================

total_rows = len(df)

unique_signatures = len(
    signature_groups
)


# ==========================================
# 6. FIND COLLISIONS
# ==========================================

colliding_signatures = []

characters_in_collisions = set()


for signature, characters in signature_groups.items():

    # More than one character
    # has exactly the same signature

    if len(characters) > 1:

        colliding_signatures.append(
            (signature, characters)
        )

        characters_in_collisions.update(
            characters
        )


# ==========================================
# 7. THEORETICAL UPPER BOUND
# ==========================================

maximum_possible_correct = 0


for signature, characters in signature_groups.items():

    # For a signature shared by multiple
    # characters, the best possible classifier
    # can only choose one character.

    maximum_possible_correct += 1


maximum_possible_accuracy = (
    maximum_possible_correct
    / total_rows
    * 100
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print()
print("==========================================")
print("17-FEATURE SIGNATURE ANALYSIS")
print("==========================================")


print(
    "Total rows:",
    total_rows
)


print(
    "Features used:",
    len(features)
)


print(
    "Unique signatures:",
    unique_signatures
)


print(
    "Signatures containing multiple characters:",
    len(colliding_signatures)
)


print(
    "Characters involved in collisions:",
    len(characters_in_collisions)
)


print()
print("==========================================")
print("THEORETICAL UPPER BOUND")
print("==========================================")


print(
    "Maximum possible correct:",
    maximum_possible_correct
)


print(
    "Maximum possible accuracy:",
    maximum_possible_accuracy,
    "%"
)


print()
print("==========================================")
print("SIGNATURE ANALYSIS COMPLETE")
print("==========================================")