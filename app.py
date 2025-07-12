from flask import Flask, render_template, request, redirect, url_for, session
import json
import csv
import os
from datetime import datetime
from logic.personality_logic import get_personality_result
from logic.intelligence_logic import get_intelligence_result
from logic.attitude_logic import get_attitude_result
from logic.depression_logic import get_depression_result

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure data directories and files exist
os.makedirs('data', exist_ok=True)

if not os.path.exists('user.csv'):
   with open('user.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username', 'email', 'password', 'full_name', 'gender',
                     'registration_date', 'x1', 'x2', 'x3', 'x4', 'x5', 'verified'])

if not os.path.exists('data/results.csv'):
    with open('data/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'test_type', 'score', 'result'])

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gender = request.form['gender']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        registered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # CSV file path
        user_file = 'user.csv'

        # If the file does not exist, create it with header
        if not os.path.exists(user_file):
            with open(user_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'gender', 'full_name', 'email', 'password', 'registered_at'])

        # Append the user data
        with open(user_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, full_name, gender, email, password, registered_at])
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not os.path.exists('user.csv'):
            return render_template('login.html', error="User database not found. Please register first.")

        with open('user.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print("DEBUG: Checking", row)  # <-- Add this for debugging
                if row['username'] == username and row['password'] == password:
                    session['username'] = username
                    return redirect(url_for('dashboard'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    last_result = None
    with open('data/results.csv', 'r') as file:
        results = list(csv.reader(file))
        for row in reversed(results[1:]):
            if row[0] == username:
                last_result = {
                    'username': row[0],
                    'test': row[1],
                    'score': row[2],
                    'result': row[3],
                    'link': url_for('result_page', test=row[1], score=row[2], result=row[3])
                }
                break

    return render_template('dashboard.html', username=username, last_result=last_result)


# Result page
@app.route('/result')
def result_page():
    test_type = request.args.get('test')
    score = request.args.get('score')
    result = request.args.get('result')

    # Detailed personality results data
    results_data = {
        "INTP": {
            'result_title': 'The Logician',
            'result_description': 'Innovative, curious, and intellectual. You love exploring abstract ideas.',
            'result_traits': ['Analytical', 'Inventive', 'Reserved'],
            'quote': '“The important thing is not to stop questioning.” – Albert Einstein',
            'tips': [
                'Stay grounded while exploring big ideas.',
                'Take time to connect emotionally.',
                'Channel your curiosity into action.'
            ]
        },
        "ENTJ": {
            'result_title': 'The Commander',
            'result_description': 'Bold, strategic, and driven. You thrive in leadership and challenge.',
            'result_traits': ['Decisive', 'Efficient', 'Confident'],
            'quote': '“Leadership is the capacity to translate vision into reality.” – Warren Bennis',
            'tips': [
                'Balance ambition with empathy.',
                'Create space for others to contribute.',
                'Rest is also productive.'
            ]
        },
        "ENTP": {
            'result_title': 'The Debater',
            'result_description': 'Quick-witted, outgoing, and smart. You challenge the status quo.',
            'result_traits': ['Energetic', 'Curious', 'Innovative'],
            'quote': '“The unexamined life is not worth living.” – Socrates',
            'tips': [
                'Turn debate into collaboration.',
                'Follow through on your ideas.',
                'Listen deeply, not just logically.'
            ]
        },
        'ESFP': {
            'result_title': 'The Entertainer',
            'result_description': 'Enthusiastic, spontaneous, and energetic. You thrive in social situations.',
            'result_traits': ['Sociable', 'Spontaneous', 'Energetic'],
            'quote': '“Life is either a daring adventure or nothing at all.” – Helen Keller',
            'tips': [
                'Embrace your energy with purpose.',
                'Remember to reflect occasionally.',
                'Stay grounded in meaningful relationships.'
            ]
        },
        'INFJ': {
            'result_title': 'The Advocate',
            'result_description': 'Insightful, idealistic, and principled. You aim to make a difference in the world.',
            'result_traits': ['Empathetic', 'Visionary', 'Determined'],
            'quote': '“The best way to find yourself is to lose yourself in the service of others.” – Mahatma Gandhi',
            'tips': [
                'Don’t forget to care for yourself while helping others.',
                'Embrace your quiet strength.',
                'Pursue causes that align with your core values.'
            ]
        },
        'INTJ': {
            'result_title': 'The Analyst',
            'result_description': 'Strategic, logical, and independent. You enjoy solving complex problems.',
            'result_traits': ['Analytical', 'Decisive', 'Independent'],
            'quote': '“A wise man can learn more from a foolish question than a fool can learn from a wise answer.” – Bruce Lee',
            'tips': [
                'Allow space for emotions alongside logic.',
                'Collaborate, even if you prefer working alone.',
                'Balance vision with patience.'
            ]
        },
        'INFP': {
            'result_title': 'The Mediator',
            'result_description': 'Compassionate, imaginative, and idealistic. You seek inner harmony and truth.',
            'result_traits': ['Empathetic', 'Creative', 'Idealistic'],
            'quote': '“We are what we pretend to be, so we must be careful about what we pretend to be.” – Kurt Vonnegut',
            'tips': [
                'Ground your ideals in practical action.',
                'Protect your emotional boundaries.',
                'Share your inner world — it’s valuable.'
            ]
        },
        'ENFP': {
            'result_title': 'The Campaigner',
            'result_description': 'Enthusiastic, open-minded, and imaginative. You love exploring ideas and people.',
            'result_traits': ['Energetic', 'Curious', 'Inspirational'],
            'quote': '“Logic will get you from A to B. Imagination will take you everywhere.” – Albert Einstein',
            'tips': [
                'Focus your energy to avoid burnout.',
                'Follow through on your many ideas.',
                'Let your creativity be a source of strength.'
            ]
        },
        'ENFJ': {
            'result_title': 'The Protagonist',
            'result_description': 'Charismatic, inspiring, and empathetic. You lead by uplifting others.',
            'result_traits': ['Motivational', 'Supportive', 'Influential'],
            'quote': '“Leadership is not about being in charge. It is about taking care of those in your charge.” – Simon Sinek',
            'tips': [
                'Lead with both confidence and humility.',
                'Take breaks from giving to restore your energy.',
                'Surround yourself with honest and kind feedback.'
            ]
        },
        "ISTJ": {
            'result_title': 'The Logistician',
            'result_description': 'Responsible, organized, and reliable. You value traditions and structure.',
            'result_traits': ['Dependable', 'Detailed', 'Principled'],
            'quote': '“Discipline is the bridge between goals and accomplishment.” – Jim Rohn',
            'tips': [
                'Embrace flexibility where needed.',
                'Don’t be afraid to try new methods.',
                'Balance work with relaxation.'
            ]
        },
        "ISFJ": {
            'result_title': 'The Defender',
            'result_description': 'Loyal, practical, and kind. You enjoy helping others in quiet ways.',
            'result_traits': ['Caring', 'Conscientious', 'Loyal'],
            'quote': '“Kindness is the language which the deaf can hear and the blind can see.” – Mark Twain',
            'tips': [
                'Recognize your own needs, too.',
                'Set boundaries without guilt.',
                'Let your kindness empower, not exhaust.'
            ]
        },
        "ESTJ": {
            'result_title': 'The Executive',
            'result_description': 'Organized, decisive, and loyal. You naturally take charge of situations.',
            'result_traits': ['Leader', 'Efficient', 'Grounded'],
            'quote': '“The way to get started is to quit talking and begin doing.” – Walt Disney',
            'tips': [
                'Consider emotional perspectives too.',
                'Loosen control when needed.',
                'Appreciate spontaneity in others.'
            ]
        },
        "ESFJ": {
            'result_title': 'The Consul',
            'result_description': 'Warmhearted, conscientious, and cooperative. You love supporting your community.',
            'result_traits': ['Social', 'Supportive', 'Reliable'],
            'quote': '“Alone we can do so little; together we can do so much.” – Helen Keller',
            'tips': [
                'Care for yourself as much as for others.',
                'Trust your own voice.',
                'Avoid overcommitting.'
            ]
        },
        "ISTP": {
            'result_title': 'The Virtuoso',
            'result_description': 'Bold and practical experimenters. You love building, fixing, and figuring things out.',
            'result_traits': ['Independent', 'Tactical', 'Adventurous'],
            'quote': '“Tell me and I forget. Teach me and I remember. Involve me and I learn.” – Benjamin Franklin',
            'tips': [
                'Channel curiosity productively.',
                'Nurture emotional self-awareness.',
                'Balance freedom with connection.'
            ]
        },
        "ISFP": {
            'result_title': 'The Adventurer',
            'result_description': 'Flexible, charming, and artistic. You value self-expression and new experiences.',
            'result_traits': ['Sensitive', 'Creative', 'Spontaneous'],
            'quote': '“To live is the rarest thing in the world. Most people exist, that is all.” – Oscar Wilde',
            'tips': [
                'Express your feelings more openly.',
                'Step outside comfort zones.',
                'Value routine when needed.'
            ]
        },
        "ESTP": {
            'result_title': 'The Entrepreneur',
            'result_description': 'Energetic and perceptive. You excel in fast-paced, real-world environments.',
            'result_traits': ['Dynamic', 'Bold', 'Practical'],
            'quote': '“In the middle of every difficulty lies opportunity.” – Albert Einstein',
            'tips': [
                'Think long-term, not just in the moment.',
                'Listen more than you speak.',
                'Channel your energy constructively.'
            ]
        }
    }

    # Prepare result info based on test type and result
    if test_type == 'personality':
        result_info = results_data.get(result, {
            'result_title': 'Unknown Personality Type',
            'result_description': 'Description not found for this personality type.',
            'result_traits': [],
            'quote': '',
            'tips': []
        })
    elif test_type == 'intelligence':
        # Provide generic messages for intelligence test results
        intelligence_levels = {
            'High Intelligence': ("High Intelligence",
                                  "Excellent performance. You show strong logical and reasoning skills."),
            'Average Intelligence': ("Average Intelligence",
                                     "Good performance. You have solid logical and reasoning skills."),
            'Low Intelligence': ("Low Intelligence",
                                           "There may be room for improvement in logical and reasoning skills.")
        }
        title, desc = intelligence_levels.get(result, ("Unknown Intelligence Result", "No description available."))
        result_info = {
            'result_title': title,
            'result_description': desc,
            'result_traits': [],
            'quote': '“The true sign of intelligence is not knowledge but imagination.” – Albert Einstein',
            'tips': ['Keep practicing problem solving.',
                     'Engage in critical thinking exercises.',
                     'Challenge yourself with puzzles and brain games.']
        }
    elif test_type == 'attitude':
        attitude_levels = {
            'Positive Attitude': ("Positive Attitude", "You have a very positive and healthy mindset."),
            'Neutral Attitude': ("Neutral Attitude", "Your attitude is generally balanced."),
            'Negative Attitude': ("Negative Attitude", "Consider working on developing a more positive outlook.")
        }
        title, desc = attitude_levels.get(result, ("Unknown Attitude Result", "No description available."))
        result_info = {
            'result_title': title,
            'result_description': desc,
            'result_traits': [],
            'quote': '“Your attitude, not your aptitude, will determine your altitude.” – Zig Ziglar',
            'tips': ['Stay optimistic.',
                     'Practice gratitude daily.',
                     'Engage in positive self-talk.']
        }
    elif test_type == 'depression':
        depression_levels = {
            'Severe Depression': ("Severe Depression", "It is recommended to seek professional help."),
            'Moderate Depression': ("Moderate Depression", "Consider talking to a counselor or therapist."),
            'Mild Depression': ("Mild Depression", "Monitor your mood and consider self-care strategies."),
            'Minimal Depression': ("Minimal or No Depression", "You are doing well emotionally.")
        }
        title, desc = depression_levels.get(result, ("Unknown Depression Result", "No description available."))
        result_info = {
            'result_title': title,
            'result_description': desc,
            'result_traits': [],
            'quote': '“Even the darkest night will end and the sun will rise.” – Victor Hugo',
            'tips': ['Stay connected with loved ones.',
                     'Engage in regular physical activity.',
                     'Seek support when needed.']
        }
    else:
        result_info = {
            'result_title': 'Unknown Test',
            'result_description': 'No details are available for this test.',
            'result_traits': [],
            'quote': '',
            'tips': []
        }

    image_url = url_for('static', filename=f'images/results/{test_type}_{result}.jpg')

    return render_template('result.html',
                           test=test_type,
                           score=score,
                           result=result,
                           result_type=test_type.capitalize(),
                           result_title=result_info['result_title'],
                           result_description=result_info['result_description'],
                           result_traits=result_info['result_traits'],
                           quote=result_info['quote'],
                           tips=result_info['tips'],
                           image_url=image_url)

# Handle all test routes dynamically
@app.route('/<test_type>_test', methods=['GET', 'POST'])
def test(test_type):
    if 'username' not in session:
        return redirect(url_for('login'))

    question_file_path = f"data/questions/{test_type}_questions.json"
    questions = []

    if os.path.exists(question_file_path):
        with open(question_file_path) as f:
            questions = json.load(f)

    if request.method == 'POST':
        answers = []
        missing = []
        for i in range(10):
            key = f'q{i}'
            val = request.form.get(key)
            if val is None:
                missing.append(key)
            else:
                answers.append(int(val))

        if missing:
            error_msg = f"Please answer all questions. Missing: {', '.join(missing)}"
            return render_template(f"{test_type}_test.html", questions=questions, error=error_msg)

        score = sum(answers)

        if test_type == 'personality':
            result = get_personality_result(answers)
        elif test_type == 'intelligence':
            # Map numeric answers to letters A-D for intelligence
            num_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
            letter_answers = [num_to_letter.get(ans, 'A') for ans in answers]
            result = get_intelligence_result(letter_answers)
        elif test_type == 'attitude':
    # Map numeric answers to letter codes expected by attitude logic
            letter_map = {1: 'C', 2: 'C', 3: 'B', 4: 'A', 5: 'A'}
            letter_answers = [letter_map.get(ans, 'B') for ans in answers]

    # get_attitude_result expects a list of letters and returns the attitude category
            result = get_attitude_result(letter_answers)

    # Optional: you can calculate a score for progress bar or saving, e.g. count of 'A's
            score = letter_answers.count('A')

        elif test_type == 'depression':
            num_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
            letter_answers = [num_to_letter.get(ans, 'A') for ans in answers]
            result, score = get_depression_result(letter_answers)

        else:
            result = "Unknown"

        # Save result with score and result string (for depression, we have result and score)
        # For others, 'score' is an int, for depression 'score' is returned from logic
        if test_type == 'depression':
            # Use updated score from logic scoring
            effective_score = score
        else:
            effective_score = score

        with open('data/results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([session['username'], test_type, effective_score, result])

        return redirect(url_for('result_page', test=test_type, score=effective_score, result=result))

    return render_template(f"{test_type}_test.html", questions=questions)

if __name__ == '__main__':
    app.run(debug=True)

