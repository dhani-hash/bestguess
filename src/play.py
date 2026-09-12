


def question_to_text(question):

    feature = question["feature"]
    value = question["value"]
    question_type = question["type"]

    if question_type == "categorical":

        return (
            f"Is your character's "
            f"{feature} {value}?"
        )

    elif question_type == "numeric":

        return (
            f"Is your character's "
            f"{feature} >= {value:.1f}?"
        )

    return "Unknown question"


def predict(tree):

    while "character" not in tree:

        question = tree["question"]

        text = question_to_text(question)

        while True:

            answer = input(
                text + " (y/n): "
            ).lower().strip()

            if answer in ["y", "n"]:
                break

            print("Please answer only y or n.")


        if answer == "y":

            tree = tree["yes"]

        else:

            tree = tree["no"]


    return tree["character"]