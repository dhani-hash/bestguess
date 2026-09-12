from entropy import entropy


def information_gain(parent_labels, feature_values):

    parent_entropy = entropy(parent_labels)

    yes_labels = []
    no_labels = []

    for label, value in zip(parent_labels, feature_values):

        if value == 1:
            yes_labels.append(label)
        else:
            no_labels.append(label)

    total = len(parent_labels)

    yes_weight = len(yes_labels) / total
    no_weight = len(no_labels) / total

    child_entropy = (
        yes_weight * entropy(yes_labels)
        + no_weight * entropy(no_labels)
    )

    return parent_entropy - child_entropy