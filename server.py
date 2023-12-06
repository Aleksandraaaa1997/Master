from flask import Flask, render_template, request
#from flask_ngrok import run_with_ngrok
import random

app = Flask(__name__)

#run_with_ngrok(app)

questions = []
a = 0  # Initialize 'a'

def update_questions():
    global questions, a
    index=1

    a = random.randint(2, 5)

    if index == 1:
        id_question=1
        text = "Skratiti dati razlomak"
        fraction_up_number1=random.randint(2,20)
        fraction_up_number2 = random.randint(2,20)
        fraction_down = random.randint(2,10)
        while (fraction_up_number1+fraction_up_number2)%fraction_down != 0:
            fraction_up_number1 = random.randint(2, 20)
            fraction_up_number2 = random.randint(2, 20)
            fraction_down = random.randint(2, 10)
        corret_answer = (fraction_up_number1+fraction_up_number2)/fraction_down
        incorrect_answer_1=corret_answer+1
        incorrect_answer_2 = corret_answer+2
        incorrect_answer_3 = corret_answer+3



    # Sample quiz data
    questions = [
        {
            'id': 1,
            'question': text + f" <math> <mfrac> <mrow> <mn>{fraction_up_number1}</mn> <mo>+</mo> <mn>{fraction_up_number2}</mn> </mrow> <mrow> <mn>{fraction_down}</mn> </mrow> </mfrac> </math>",
            'options': [int(corret_answer), int(incorrect_answer_2), int(incorrect_answer_1)],
            'correct_answer': int(corret_answer)
        },
        {
            'id': 2,
            'question': f'Koji od zadatih grafika opisuje funkciju y = {a}*x?',
            'image_options': ['output_function1.jpg', 'output_function2.jpg', 'output_function3.jpg'],
            'correct_answer': 'output_function1.jpg'
        },
        # Add more questions as needed
    ]
    return questions, a

@app.route('/')
def index():
    update_questions()

    generate_and_save_functions(a, 'output')
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for question in questions:
        selected_option = request.form.get(f'question_{question["id"]}')
        print(selected_option)
        print(question['correct_answer'])
        if selected_option == question['correct_answer'] or str(selected_option) == str(question['correct_answer']):
            score += 1

    return render_template('result.html', score=score, total=len(questions))

import os
import numpy as np
import matplotlib.pyplot as plt

def generate_and_save_functions(a, filename_prefix):
    plt.switch_backend('agg')  # Use a non-GUI backend to avoid threading issues

    # Generate x values
    x = np.linspace(-10, 10, 100)

    # Define the three functions
    y1 = a * x
    y2 = np.full_like(x, a)
    y3 = a * x**2

    # Plot y = a*x
    plt.figure(figsize=(6, 4))
    plt.plot(x, y1)
 #   plt.title('Function: y = a*x')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.savefig(os.path.join('../App_Master_1/static', f'{filename_prefix}_function1.jpg'))
    plt.close()

    # Plot y = a
    plt.figure(figsize=(6, 4))
    plt.plot(x, y2)
 #   plt.title('Function: y = a')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.savefig(os.path.join('../App_Master_1/static', f'{filename_prefix}_function2.jpg'))
    plt.close()

    # Plot y = a*x^2
    plt.figure(figsize=(6, 4))
    plt.plot(x, y3)
#    plt.title('Function: y = a*x^2')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.savefig(os.path.join('../App_Master_1/static', f'{filename_prefix}_function3.jpg'))
    plt.close()



# Add a decorator to set cache control for all routes
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run()
