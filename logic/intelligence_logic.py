def get_intelligence_result(answers):
    # correct_answers is the answer key: letter codes for each question
    correct_answers = ['C', 'A', 'A', 'B', 'C', 'B', 'C', 'A', 'B', 'B']

    # Calculate how many answers match the correct answers
    score = sum(1 for a, c in zip(answers, correct_answers) if a == c)

    # Determine intelligence level based on score range
    if score >= 8:
        return "High Intelligence"
    elif score >= 5:
        return "Average Intelligence"
    else:
        return "Low Intelligence"

