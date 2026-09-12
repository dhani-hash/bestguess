def ask_question(row, question):

    feature = question["feature"]
    value = question["value"]
    question_type = question["type"]

    actual_value = row[feature].strip()


    # -----------------------------
    # Categorical question
    # -----------------------------

    if question_type == "categorical":

        return actual_value == value


    # -----------------------------
    # Numeric question
    # -----------------------------

    if question_type == "numeric":

        try:
            actual_value = float(actual_value)
        except ValueError:
            return False

        return actual_value >= value


    return False