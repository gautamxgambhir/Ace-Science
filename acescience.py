import requests
from typing import Final
from dotenv import load_dotenv
import os
from pdf_processor import select_random_page

load_dotenv()
API_KEY: Final[str] = os.getenv("API_KEY")

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def generate_response(user_input, datafile):
    data_list = select_random_page(data_file=datafile)
    chapter_name = data_list[0]
    page_number = data_list[1]
    text = data_list[2]

    system_instruction = {
        "role": "system",
        "content": (
            "you have to give only one question"
            "dont include any additional text or commentary outside the specified format"
            "You are an AI Question Generator designed to create concise, meaningful, and exam-relevant questions exclusively from the NCERT Class 10 textbooks. "
            "Your task is to generate questions strictly based on the given text and the following rules: "
            "\n\n"
            "### Guidelines for Generating Questions: "
            "  - 100% of the questions should be True/False or Yes/No type. "
            "- For True/False questions, modify the text slightly to generate **false statements** where applicable. "
            "- make the questions a bit tricky, and tough to answer too"
            "- Ensure the false statements are realistic and plausible to challenge the user. For example: "
            "  - Text: 'The heart has four chambers.' "
            "    Question: 'True or False: The heart has three chambers.' (Answer: False) "
            "- For the questions, ensure scientifically accurate. questions. "
            "- Use only the provided text for generating questions but allow slight modifications to create false statements. "
            "- Avoid asking questions that require users to reference the provided text directly. "
            "- Ensure that the questions are meaningful, scientifically accurate, and exam-relevant. "
            "- Avoid formula-based questions and repetitive or vague queries. "
            "\n\n"
            "### Format for Response: "
            "['Question', 'Answer', 'Explanation', 'Page number', 'Chapter name']"
            "\n\n"
            "### Important Rules: "
            "- Your response must strictly follow the format: ['Question', 'Answer', 'Explanation', 'Page number', 'Chapter name']. "
            "- Do not add any additional text or commentary outside the specified format. "
            "- Modify the provided text slightly to create challenging false statements while maintaining scientific accuracy. "
            "- Avoid generating questions where the text provided is required to answer the question. "
            "- The explanation should be 1-2 sentences and clarify the reasoning behind the answer. "
            "- Prioritize clarity and exam relevance in all questions. "
            "\n\n"
            "Make sure to include chapter number and name both, in explanation you give, in a NEW LINE"
            "DO NOT GIVE PAGE NUMBER IN EXPLANATION"
            "### Text Details: "
            f"The content you are working with is from '{chapter_name}', Page: {page_number}. "
            f"The text is: '{text}'."
        )
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [system_instruction, {"role": "user", "content": user_input}],
        "max_tokens": 200,
        "temperature": 0.7,
        "top_p": 1.0,
    }

    response = requests.post(API_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        return "Error generating question. Please try again."

    return response.json()["choices"][0]["message"]["content"]


def ai_check_answer(user_input):    
    system_instruction = {
        "role": "system",
        "content": (
            "You are an AI designed to validate answers for questions based on the NCERT Class 10 textbooks. "
            "Your task is to determine if the user's answer is correct or incorrect based on the provided question and correct answer. "
            "\n\n"
            "### Guidelines for Validating Answers: "
            "- For True/False or Yes/No questions: "
            "  - Accept variations such as 'Yes', 'True', 'Correct', or similar synonyms as correct for 'True'. "
            "  - Accept variations such as 'No', 'False', 'Incorrect', or similar synonyms as correct for 'False'. "
            "- For one-word answers: "
            "  - Accept synonyms, alternate phrasings, and variations in spelling if they convey the same meaning as the correct answer. "
            "  - Example: 'Mitochondria' and 'Mitochondrion' should both be considered correct. "
            "- Evaluate modified false statements carefully and ensure correctness. "
            "- If the user's answer matches the intent of the correct answer, even if phrased differently, mark it as 'correct'. "
            "- If the user's answer is irrelevant, factually incorrect, or out of context, mark it as 'incorrect'. "
            "\n\n"
            "### Response Format: "
            "- Respond only with 'correct' or 'incorrect'. "
            "- Do not add any additional commentary, explanations, or text. "
            "\n\n"
            "### Examples: "
            "1. Question: 'Is nephron the structural and functional unit of the kidney?'\n"
            "   User's Answer: 'Yes'\n"
            "   Correct Answer: 'True'\n"
            "   Response: 'correct'\n"
            "\n"
            "2. Question: 'True or False: The heart has three chambers.'\n"
            "   User's Answer: 'False'\n"
            "   Correct Answer: 'False'\n"
            "   Response: 'correct'\n"
            "\n"
            "3. Question: 'What is the powerhouse of the cell?'\n"
            "   User's Answer: 'It is mitochondria.'\n"
            "   Correct Answer: 'Mitochondria'\n"
            "   Response: 'correct'\n"
        )
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [system_instruction, {"role": "user", "content": user_input}],
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 1.0,
    }

    response = requests.post(API_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        return "Error validating answer."

    return response.json()["choices"][0]["message"]["content"]