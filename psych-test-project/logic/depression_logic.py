def get_depression_result(answers):
    score = 0
    for answer in answers:
        if answer == 'A':  # Not at all
            score += 0
        elif answer == 'B':  # Several days
            score += 1
        elif answer == 'C':  # More than half the days
            score += 2
        elif answer == 'D':  # Nearly every day
            score += 3

    if score >= 21:
        return "Severe Depression", score
    elif score >= 15:
        return "Moderate Depression", score
    elif score >= 8:
        return "Mild Depression", score
    else:
        return "Minimal Depression", score