import json

def get_personality_result(answers):
    # Map numeric answers (1-5) to letter codes (A-E)
    num_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    answers = [num_to_letter.get(a, 'C') for a in answers]  # default to 'C' if invalid

    traits = {
        'I': 0, 'E': 0,
        'N': 0, 'S': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }

    # Load the same personality_questions.json used in your test
    with open("data/questions/personality_questions.json", "r") as f:
        questions = json.load(f)

    for i, answer in enumerate(answers):
        dimension = questions[i]["dimension"]  # e.g., "N/S"
        preferred = questions[i]["direction"]  # e.g., "N"

        trait1, trait2 = dimension.split("/")  # N vs S

        if preferred == trait1:
            first, second = trait1, trait2
        else:
            first, second = trait2, trait1

        if answer == "A":
            traits[first] += 2
        elif answer == "B":
            traits[first] += 1
        elif answer == "C":
            pass  # neutral
        elif answer == "D":
            traits[second] += 1
        elif answer == "E":
            traits[second] += 2

    result = ''
    result += 'I' if traits['I'] >= traits['E'] else 'E'
    result += 'N' if traits['N'] >= traits['S'] else 'S'
    result += 'T' if traits['T'] >= traits['F'] else 'F'
    result += 'J' if traits['J'] >= traits['P'] else 'P'

    return result

