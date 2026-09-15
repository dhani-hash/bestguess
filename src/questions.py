def ask_question(row, question):

    feature = question["feature"]
    value = question["value"]
    question_type = question["type"]

    actual_value = row[feature]

    # Categorical question
    if question_type == "categorical":

        actual_value = str(actual_value).strip()
        expected_value = str(value).strip()

        return actual_value == expected_value

    # Numeric question
    if question_type == "numeric":

        try:
            actual_value = float(actual_value)
            value = float(value)
        except (ValueError, TypeError):
            return False

        return actual_value >= value

    return False