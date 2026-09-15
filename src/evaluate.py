import pandas as pd

from decision_tree import build_tree
from questions import ask_question
from question_generator import questions


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/superheroes_clean.csv")


# ==========================================
# 2. TRAIN / TEST SPLIT
# ==========================================

train_data = []
test_data = []

for character, group in df.groupby("Character"):

    rows = group.to_dict("records")

    # We need at least 2 rows
    if len(rows) >= 2:

        # All except last row -> training
        train_data.extend(rows[:-1])

        # Last row -> testing
        test_data.append(rows[-1])


print("Total rows:", len(df))
print("Training rows:", len(train_data))
print("Testing rows:", len(test_data))


# ==========================================
# 3. USE GENERATED QUESTIONS
# ==========================================

# IMPORTANT:
# Questions are generated in question_generator.py
# We import them here instead of generating them again.

print("Questions generated:", len(questions))


# ==========================================
# 4. TRAIN THE TREE
# ==========================================

print("\nBuilding decision tree using TRAINING data...")
print("Please wait...")


tree = build_tree(
    train_data,
    questions
)


print("Decision tree built successfully!")


# ==========================================
# 5. TREE DIAGNOSTICS
# ==========================================

def analyze_tree(tree, depth=0):

    # --------------------------------------
    # Leaf node
    # --------------------------------------

    if "character" in tree:

        return {
            "nodes": 1,
            "leaves": 1,
            "max_depth": depth
        }


    # --------------------------------------
    # Analyze YES branch
    # --------------------------------------

    yes_stats = analyze_tree(
        tree["yes"],
        depth + 1
    )


    # --------------------------------------
    # Analyze NO branch
    # --------------------------------------

    no_stats = analyze_tree(
        tree["no"],
        depth + 1
    )


    # --------------------------------------
    # Combine statistics
    # --------------------------------------

    return {

        "nodes": (
            1
            + yes_stats["nodes"]
            + no_stats["nodes"]
        ),

        "leaves": (
            yes_stats["leaves"]
            + no_stats["leaves"]
        ),

        "max_depth": max(
            yes_stats["max_depth"],
            no_stats["max_depth"]
        )
    }


# ------------------------------------------
# Calculate tree statistics
# ------------------------------------------

stats = analyze_tree(tree)


print("\n========== TREE DIAGNOSTICS ==========")

print(
    "Total tree nodes:",
    stats["nodes"]
)

print(
    "Total leaves:",
    stats["leaves"]
)

print(
    "Maximum depth:",
    stats["max_depth"]
)


# ==========================================
# 6. PREDICT ONE ROW
# ==========================================

def predict_row(tree, row):

    # --------------------------------------
    # If we reached a leaf
    # --------------------------------------

    if "character" in tree:

        return tree["character"]


    # --------------------------------------
    # Get question stored at this node
    # --------------------------------------

    question = tree["question"]


    # --------------------------------------
    # Automatically answer the question
    # using the row
    # --------------------------------------

    answer = ask_question(
        row,
        question
    )


    # --------------------------------------
    # Follow appropriate branch
    # --------------------------------------

    if answer:

        return predict_row(
            tree["yes"],
            row
        )

    else:

        return predict_row(
            tree["no"],
            row
        )


# ==========================================
# 7. TEST THE TREE
# ==========================================

print("\nTesting model...")


correct = 0


for row in test_data:

    prediction = predict_row(
        tree,
        row
    )

    actual = row["Character"]


    if prediction == actual:

        correct += 1


# ==========================================
# 8. TEST ACCURACY
# ==========================================

accuracy = correct / len(test_data)


print("\n========== RESULTS ==========")

print(
    "Correct predictions:",
    correct
)

print(
    "Total test rows:",
    len(test_data)
)

print(
    "Accuracy:",
    accuracy * 100,
    "%"
)


# ==========================================
# 9. TRAINING ACCURACY
# ==========================================

train_correct = 0


for row in train_data:

    prediction = predict_row(
        tree,
        row
    )

    actual = row["Character"]


    if prediction == actual:

        train_correct += 1


train_accuracy = (
    train_correct
    / len(train_data)
)


print(
    "\n========== TRAINING RESULTS =========="
)

print(
    "Correct training predictions:",
    train_correct
)

print(
    "Total training rows:",
    len(train_data)
)

print(
    "Training accuracy:",
    train_accuracy * 100,
    "%"
)
# ==========================================
# 10. ANALYZE QUESTIONS USED BY THE TREE
# ==========================================

from collections import Counter


def collect_questions(tree, counter):

    # --------------------------------------
    # If leaf node, stop
    # --------------------------------------

    if "character" in tree:
        return

    # --------------------------------------
    # Get question used at this node
    # --------------------------------------

    question = tree["question"]

    feature = question["feature"]

    counter[feature] += 1

    # --------------------------------------
    # Continue through both branches
    # --------------------------------------

    collect_questions(
        tree["yes"],
        counter
    )

    collect_questions(
        tree["no"],
        counter
    )


# ------------------------------------------
# Count feature usage
# ------------------------------------------

feature_usage = Counter()

collect_questions(
    tree,
    feature_usage
)


# ==========================================
# DISPLAY FEATURE USAGE
# ==========================================

print(
    "\n========== TREE FEATURE USAGE =========="
)

for feature, count in feature_usage.most_common():

    print(
        feature,
        "->",
        count,
        "splits"
    )