from information_gain import information_gain
from questions import ask_question


# ====================================
# Tree control parameters
# ====================================

MAX_DEPTH = 10
MIN_SAMPLES = 5


# ====================================
# Build Decision Tree
# ====================================

def build_tree(
    data,
    questions,
    default=None,
    depth=0
):

    # --------------------------------
    # 1. Empty branch
    # --------------------------------

    if len(data) == 0:

        return {
            "character": default
        }


    # --------------------------------
    # 2. Get characters
    # --------------------------------

    labels = [
        row["Character"]
        for row in data
    ]


    # --------------------------------
    # 3. If all characters are same
    # --------------------------------

    if len(set(labels)) == 1:

        return {
            "character": labels[0]
        }


    # --------------------------------
    # 4. Maximum tree depth reached
    # --------------------------------

    if depth >= MAX_DEPTH:

        return {
            "character": most_common(labels)
        }


    # --------------------------------
    # 5. Too few samples
    # --------------------------------

    if len(data) <= MIN_SAMPLES:

        return {
            "character": most_common(labels)
        }


    # --------------------------------
    # 6. No questions left
    # --------------------------------

    if len(questions) == 0:

        return {
            "character": most_common(labels)
        }


    # --------------------------------
    # 7. Find BEST question
    # --------------------------------

    best_question = None
    best_gain = -1


    for question in questions:

        # Convert question into YES/NO
        # values for every character

        question_values = [
            1 if ask_question(row, question) else 0
            for row in data
        ]


        # Calculate information gain

        gain = information_gain(
            labels,
            question_values
        )


        # Keep highest gain question

        if gain > best_gain:

            best_gain = gain
            best_question = question


    # --------------------------------
    # 8. Safety check
    # --------------------------------

    if best_question is None:

        return {
            "character": most_common(labels)
        }


    # --------------------------------
    # 9. Split dataset
    # --------------------------------

    yes_data = []
    no_data = []


    for row in data:

        if ask_question(row, best_question):

            yes_data.append(row)

        else:

            no_data.append(row)


    # --------------------------------
    # 10. Avoid useless split
    # --------------------------------

    if len(yes_data) == 0 or len(no_data) == 0:

        return {
            "character": most_common(labels)
        }


    # --------------------------------
    # 11. Remove used question
    # --------------------------------

    remaining_questions = [

        question
        for question in questions
        if question != best_question

    ]


    # --------------------------------
    # 12. Fallback character
    # --------------------------------

    default_character = most_common(labels)


    # --------------------------------
    # 13. Build YES branch
    # --------------------------------

    yes_branch = build_tree(

        yes_data,

        remaining_questions,

        default_character,

        depth + 1

    )


    # --------------------------------
    # 14. Build NO branch
    # --------------------------------

    no_branch = build_tree(

        no_data,

        remaining_questions,

        default_character,

        depth + 1

    )


    # --------------------------------
    # 15. Return tree node
    # --------------------------------

    return {

        "question": best_question,

        "yes": yes_branch,

        "no": no_branch

    }


# ====================================
# Find most common character
# ====================================

def most_common(labels):

    counts = {}


    for label in labels:

        if label not in counts:

            counts[label] = 0

        counts[label] += 1


    return max(
        counts,
        key=counts.get
    )


# ====================================
# Print tree
# ====================================

def print_tree(tree, indent=""):

    # --------------------------------
    # Leaf node
    # --------------------------------

    if "character" in tree:

        print(
            indent +
            "-> " +
            str(tree["character"])
        )

        return


    # --------------------------------
    # Question node
    # --------------------------------

    question = tree["question"]


    print(
        indent +
        "Question: " +
        str(question)
    )


    print(
        indent +
        " YES:"
    )


    print_tree(
        tree["yes"],
        indent + "    "
    )


    print(
        indent +
        " NO:"
    )


    print_tree(
        tree["no"],
        indent + "    "
    )