from flask import Flask, render_template, jsonify, request
from acescience import generate_response_tf,generate_response_ow, generate_response_mcq, ai_check_answer

app = Flask(__name__)

session_data = {
    "current_question": None,
    "answer": None,
    "explanation": None,
    "asked_questions": set()
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tfquiz")
def tfquiz():
    return render_template("tfquiz.html")

@app.route("/owquiz")
def owquiz():
    return render_template("owquiz.html")

@app.route("/mcqquiz")
def mcqquiz():
    return render_template("mcqquiz.html")

@app.route("/ask_question", methods=["POST", "GET"])
def ask_question():
    retries = 3
    while retries > 0:
        type = request.args.get('type', 'no_type')
        if type == 'truefalse':
            subject = request.args.get('file', 'general')
            if subject == 'general':
                response = "Please select a subject to generate a question."
                return jsonify({"question":response})
            else:
                response = generate_response_tf("['Question', 'Answer', 'Explanation']", datafile=subject)
                try:
                    parsed_response = eval(response)
                    question, answer, explanation = parsed_response
                    if question in session_data["asked_questions"]:
                        retries -= 1
                        continue
                    session_data["current_question"] = question
                    session_data["answer"] = answer
                    session_data["explanation"] = explanation
                    session_data["asked_questions"].add(question)
                    return jsonify({"question": question})
                except Exception:
                    retries -= 1
        elif type == 'oneword':
            subject = request.args.get('file', 'general')
            if subject == 'general':
                response = "Please select a subject to generate a question."
                return jsonify({"question":response})
            else:
                response = generate_response_ow("['Question', 'Answer', 'Explanation']", datafile=subject)
                try:
                    parsed_response = eval(response)
                    question, answer, explanation = parsed_response
                    if question in session_data["asked_questions"]:
                        retries -= 1
                        continue
                    session_data["current_question"] = question
                    session_data["answer"] = answer
                    session_data["explanation"] = explanation
                    session_data["asked_questions"].add(question)
                    return jsonify({"question": question})
                except Exception:
                    retries -= 1
        elif type == 'mcq':
            subject = request.args.get('file', 'general')
            if subject == 'general':
                response = "Please select a subject to generate a question."
                return jsonify({"question":response})
            else:
                response = generate_response_mcq("['Question', 'Answer', 'Explanation', 'Page number', 'Chapter name', 'option 1', 'option 2', 'option 3', 'option 4']", datafile=subject)
                # print(response)
                try:
                    parsed_response = eval(response)
                    question, answer, explanation, page_num, chapter_name, option1, option2, option3, option4 = parsed_response
                    if question in session_data["asked_questions"]:
                        retries -= 1
                        continue
                    session_data["current_question"] = question
                    session_data["answer"] = answer
                    session_data["explanation"] = explanation
                    session_data["option1"] = option1
                    session_data["option2"] = option2
                    session_data["option3"] = option3
                    session_data["option4"] = option4
                    options = [option1, option2, option3, option4]
                    session_data["asked_questions"].add(question)
                    print(f'("question": {question}, "options": {options}, "correct_option": {answer})')
                    return jsonify({"question": question, "options": options, "correct_option": answer})
                except Exception:
                    retries -= 1        
        else:
            return jsonify({"error": "Invalid question type. Please try again."})
    return jsonify({"error": "Failed to generate a question. Try again."})

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    user_answer = data.get('user_answer', '')
    correct_answer = session_data.get("answer", "")

    validation_input = f"Question: '{session_data['current_question']}'\nUser's Answer: '{user_answer}'\nCorrect Answer: '{correct_answer}'"

    try:
        validation_result = ai_check_answer(validation_input)
        if validation_result.lower().strip() == "correct":
            result = "Correct"
        else:
            result = "Incorrect"
    except Exception as e:
        print(f"Error in ai_check_answer: {e}")
        result = "Error validating answer. Please try again."

    print(f"Validation Input: {validation_input}, Result: {result}")
    return jsonify({"result": result})

@app.route("/show_explanation", methods=["POST"])
def show_explanation():
    explanation = session_data.get("explanation", "No explanation available.")
    answer = session_data.get("answer", "No explanation available.")
    return jsonify({"explanation": f"'{answer}'\n {explanation}"})

if __name__ == "__main__":
    app.run(debug=True)
    ask_question()