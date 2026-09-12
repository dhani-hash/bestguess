import math


def entropy(labels):

    if len(labels) == 0:
        return 0

    total = len(labels)

    counts = {}

    for label in labels:

        if label not in counts:
            counts[label] = 0

        counts[label] += 1

    entropy_value = 0

    for count in counts.values():

        probability = count / total

        entropy_value -= (
            probability * math.log2(probability)
        )

    return entropy_value