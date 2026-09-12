import csv

from decision_tree import build_tree
from play import predict
from question_generator import questions


# ==========================================
# 1. LOAD CLEANED DATASET
# ==========================================

with open(
    "data/superheroes_clean.csv",
    "r",
    encoding="utf-8"
) as file:

    data = list(csv.DictReader(file))


print("Characters loaded:", len(data))
print("Questions generated:", len(questions))


# ==========================================
# 2. BUILD DECISION TREE
# ==========================================

print()
print("Building decision tree...")
print("Please wait...")


tree = build_tree(
    data,
    questions
)


print("Decision tree built successfully!")


# ==========================================
# 3. PLAY GAME
# ==========================================

print()
guess = predict(tree)


print()
print("My guess is:", guess)