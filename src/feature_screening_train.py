import pandas as pd
import math


# ============================================================
# EXPERIMENT 16
# TRAINING-ONLY FEATURE SCREENING
# ============================================================

INPUT_FILE = "data/superheroes_clean.csv"


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("==========================================")
print("TRAINING-ONLY FEATURE SCREENING")
print("==========================================")

print("Total rows:", len(df))
print("Unique characters:", df["Character"].nunique())


# ============================================================
# 2. SAME TRAIN / TEST SPLIT AS evaluate.py
# ============================================================

train_data = []
test_data = []

for character, group in df.groupby("Character"):

    rows = group.to_dict("records")

    # Only characters with at least 2 rows
    if len(rows) >= 2:

        # All except last row -> training
        train_data.extend(rows[:-1])

        # Last row -> testing
        test_data.append(rows[-1])


train_df = pd.DataFrame(train_data)
test_df = pd.DataFrame(test_data)


print("\n==========================================")
print("TRAIN / TEST SPLIT")
print("==========================================")

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))


# ============================================================
# 3. FEATURES
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


features = (
    categorical_features
    + numeric_features
)


# ============================================================
# 4. ENTROPY
# ============================================================

def entropy(labels):

    counts = {}

    for label in labels:

        if label not in counts:
            counts[label] = 0

        counts[label] += 1


    total = len(labels)

    if total == 0:
        return 0.0


    result = 0.0


    for count in counts.values():

        probability = count / total

        result -= (
            probability
            * math.log2(probability)
        )


    return result


# ============================================================
# 5. INFORMATION GAIN
# ============================================================

def feature_information_gain(
    data,
    feature
):

    if feature not in data.columns:
        return 0.0


    subset = data[
        [feature, "Character"]
    ].copy()


    # Remove missing values

    subset = subset.dropna()


    if len(subset) == 0:
        return 0.0


    parent_entropy = entropy(
        subset["Character"].tolist()
    )


    total = len(subset)


    # ========================================================
    # CATEGORICAL FEATURE
    # ========================================================

    if feature in categorical_features:

        weighted_entropy = 0.0


        groups = subset.groupby(
            feature
        )


        for _, group in groups:

            probability = (
                len(group) / total
            )


            group_entropy = entropy(
                group["Character"].tolist()
            )


            weighted_entropy += (
                probability
                * group_entropy
            )


    # ========================================================
    # NUMERIC FEATURE
    # ========================================================

    else:

        subset[feature] = pd.to_numeric(
            subset[feature],
            errors="coerce"
        )


        subset = subset.dropna(
            subset=[feature]
        )


        if len(subset) == 0:
            return 0.0


        # ----------------------------------------------------
        # Use median as the binary split
        # ----------------------------------------------------

        threshold = subset[
            feature
        ].median()


        yes_group = subset[
            subset[feature] >= threshold
        ]


        no_group = subset[
            subset[feature] < threshold
        ]


        weighted_entropy = 0.0


        # YES branch

        if len(yes_group) > 0:

            probability = (
                len(yes_group)
                / len(subset)
            )


            weighted_entropy += (
                probability
                * entropy(
                    yes_group[
                        "Character"
                    ].tolist()
                )
            )


        # NO branch

        if len(no_group) > 0:

            probability = (
                len(no_group)
                / len(subset)
            )


            weighted_entropy += (
                probability
                * entropy(
                    no_group[
                        "Character"
                    ].tolist()
                )
            )


    # ========================================================
    # INFORMATION GAIN
    # ========================================================

    information_gain = (
        parent_entropy
        - weighted_entropy
    )


    return information_gain


# ============================================================
# 6. SCREEN FEATURES USING TRAINING DATA ONLY
# ============================================================

print("\n==========================================")
print("CALCULATING TRAINING FEATURE SCORES")
print("==========================================")

print("Using training data ONLY...")
print("Please wait...\n")


results = []


for feature in features:

    if feature not in train_df.columns:

        print(
            "Skipping missing feature:",
            feature
        )

        continue


    gain = feature_information_gain(
        train_df,
        feature
    )


    results.append(
        (
            feature,
            gain
        )
    )


# ============================================================
# 7. SORT
# ============================================================

results.sort(
    key=lambda x: x[1],
    reverse=True
)


# ============================================================
# 8. DISPLAY ALL FEATURES
# ============================================================

print("==========================================")
print("TRAINING FEATURE INFORMATION GAIN")
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
# 9. TOP FEATURES
# ============================================================

print("\n==========================================")
print("TOP FEATURES")
print("==========================================")

for feature, gain in results[:10]:

    print(
        f"{feature:20s} "
        f"{gain:.6f}"
    )


# ============================================================
# 10. FEATURE GROUPS FOR NEXT EXPERIMENT
# ============================================================

print("\n==========================================")
print("CANDIDATE FEATURE GROUPS")
print("==========================================")


top_5 = [
    feature
    for feature, gain in results[:5]
]


top_8 = [
    feature
    for feature, gain in results[:8]
]


top_10 = [
    feature
    for feature, gain in results[:10]
]


print("\nTOP 5:")
print(top_5)


print("\nTOP 8:")
print(top_8)


print("\nTOP 10:")
print(top_10)


print("\n==========================================")
print("SCREENING COMPLETE")
print("==========================================")