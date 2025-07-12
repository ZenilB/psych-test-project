def get_attitude_result(answers):
    positive = answers.count('A')
    neutral = answers.count('B')
    negative = answers.count('C')

    # Debugging output to check counts
    print("Positive Count:", positive, "Neutral Count:", neutral, "Negative Count:", negative)

    if positive >= 7:
        return "Positive Attitude"
    elif negative >= 6:
        return "Negative Attitude"
    else:
        return "Neutral Attitude"

