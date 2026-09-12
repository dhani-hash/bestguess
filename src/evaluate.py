import csv

from decision_tree import build_tree


# -----------------------------
# 1. Load dataset
# -----------------------------

with open("data/characters.csv", "r") as file:
    data = list(csv.DictReader(file))


# -----------------------------
# 2. Get features
# -----------------------------

features = list(data[0].keys())

target = features[0]

features = features[1:]


# -----------------------------
# 3. Create X and Y
# -----------------------------

X = []
Y = []

for row in data:

    X.append([
        1 if row[feature].lower() == "true" else 0
        for feature in features
    ])

    Y.append(row[target])


# -----------------------------
# 4. Train/Test split
# -----------------------------

split = int(len(X) * 0.8)

X_train = X[:split]
Y_train = Y[:split]

X_test = X[split:]
Y_test = Y[split:]


print("Total samples:", len(X))
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 5. Build tree using training data
# -----------------------------

tree = build_tree(
    X_train,
    Y_train,
    features
)


# -----------------------------
# 6. Prediction function
# -----------------------------

def predict_sample(tree, sample):

    while "character" not in tree:

        question = tree["question"]

        index = features.index(question)

        if sample[index] == 1:
            tree = tree["yes"]
        else:
            tree = tree["no"]

    return tree["character"]


# -----------------------------
# 7. Test model
# -----------------------------

correct = 0

for sample, actual in zip(X_test, Y_test):

    prediction = predict_sample(tree, sample)

    print(
        "Actual:",
        actual,
        "| Predicted:",
        prediction
    )

    if prediction == actual:
        correct += 1


# -----------------------------
# 8. Accuracy
# -----------------------------

accuracy = correct / len(Y_test)

print()
print("Correct:", correct)
print("Total:", len(Y_test))
print("Accuracy:", accuracy * 100, "%")