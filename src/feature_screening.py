import pandas as pd
import math


# ============================================================
# FEATURE SCREENING
# ============================================================

INPUT_FILE = "data/superheroes_clean.csv"


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("==========================================")
print("FEATURE SCREENING")
print("==========================================")

print("Total rows:", len(df))
print("Unique characters:", df["Character"].nunique())


# ============================================================
# 2. FEATURES
# ============================================================

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


features = categorical_features + numeric_features


# ============================================================
# 3. ENTROPY FUNCTION
# ============================================================

def entropy(labels):

    counts = {}

    for label in labels:

        if label not in counts:
            counts[label] = 0

        counts[label] += 1


    total = len(labels)

    result = 0.0


    for count in counts.values():

        probability = count / total

        result -= probability * math.log2(probability)


    return result


# ============================================================
# 4. INFORMATION GAIN FOR A FEATURE
# ============================================================

def feature_information_gain(df, feature):

    data = df[[feature, "Character"]].dropna()

    if len(data) == 0:
        return 0.0


    parent_entropy = entropy(
        data["Character"].tolist()
    )


    total = len(data)

    weighted_entropy = 0.0


    # --------------------------------------------------------
    # Categorical feature
    # --------------------------------------------------------

    if feature in categorical_features:

        groups = data.groupby(feature)


        for _, group in groups:

            probability = len(group) / total

            group_entropy = entropy(
                group["Character"].tolist()
            )

            weighted_entropy += (
                probability * group_entropy
            )


    # --------------------------------------------------------
    # Numeric feature
    # --------------------------------------------------------

    else:

        values = pd.to_numeric(
            data[feature],
            errors="coerce"
        )

        valid = data[values.notna()].copy()

        valid[feature] = pd.to_numeric(
            valid[feature]
        )


        if len(valid) == 0:
            return 0.0


        # Use median as a simple binary split

        threshold = valid[feature].median()


        yes_group = valid[
            valid[feature] >= threshold
        ]

        no_group = valid[
            valid[feature] < threshold
        ]


        if len(yes_group) > 0:

            probability = len(yes_group) / len(valid)

            weighted_entropy += (
                probability
                * entropy(
                    yes_group["Character"].tolist()
                )
            )


        if len(no_group) > 0:

            probability = len(no_group) / len(valid)

            weighted_entropy += (
                probability
                * entropy(
                    no_group["Character"].tolist()
                )
            )


    information_gain = (
        parent_entropy
        - weighted_entropy
    )


    return information_gain


# ============================================================
# 5. CALCULATE SCORE FOR EVERY FEATURE
# ============================================================

results = []


print("\nCalculating feature scores...")
print("Please wait...\n")


for feature in features:

    if feature not in df.columns:

        print(
            "Skipping missing feature:",
            feature
        )

        continue


    gain = feature_information_gain(
        df,
        feature
    )


    results.append(
        (
            feature,
            gain
        )
    )


# ============================================================
# 6. SORT FEATURES
# ============================================================

results.sort(
    key=lambda x: x[1],
    reverse=True
)


# ============================================================
# 7. DISPLAY RESULTS
# ============================================================

print("==========================================")
print("FEATURE INFORMATION GAIN")
print("==========================================")

for rank, (feature, gain) in enumerate(
    results,
    start=1
):

    print(
        f"{rank:2d}. "
        f"{feature:20s} "
        f"IG = {gain:.6f}"
    )


# ============================================================
# 8. TOP FEATURES
# ============================================================

print("\n==========================================")
print("TOP FEATURES")
print("==========================================")

for feature, gain in results[:10]:

    print(
        f"{feature:20s} "
        f"{gain:.6f}"
    )


print("\n==========================================")
print("SCREENING COMPLETE")
print("==========================================")