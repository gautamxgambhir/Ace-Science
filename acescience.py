import requests
from typing import Final
from dotenv import load_dotenv
import os
from pdf_processor import select_random_page

load_dotenv()
API_KEY: Final[str] = os.getenv("API_KEY")

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def generate_response_tf(user_input, datafile):
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
            " - make sure the questions you give have sufficient information to answer the question"
            " - 100% of the questions should be True/False or Yes/No type. "
            "- make the questions a bit tricky, and tough to answer too"
            "- Ensure the true/false statements are realistic and plausible to challenge the user. For example: "
            "  - Text: 'The heart has four chambers.' "
            "    Question: 'True or False: The heart has three chambers.' (Answer: False) "
            "- For the questions, ensure scientifically accurate. questions. "
            "- Use only the provided text for generating questions"
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
def generate_response_ow(user_input, datafile):
    data_list = select_random_page(data_file=datafile)
    chapter_name = data_list[0]
    page_number = data_list[1]
    text = data_list[2]

    system_instruction = {
        "role": "system",
        "content": (
            "You are an AI Question Generator designed to create **one-word-answer questions** exclusively from NCERT textbooks (Class 8 to Class 12). "
            "Your primary responsibility is to ensure that every generated question: "
            "\n\n"
            "✅ **Has sufficient context for the user to answer correctly.** "
            "✅ **Has an answer that is strictly one word (no phrases, numerical values, or True/False answers).** "
            "✅ **Is relevant, accurate, and meaningful based on the provided text.** "
            "✅ **Avoids vague or ambiguous phrasing.** "
            "✅ **Works across all subjects, including Science, Mathematics, Social Science, and Accountancy.** "
            "\n\n"
            "### **🔹 General Rules for Question Generation:**\n"
            "1️⃣ **Strictly one-word question and one-word answer:**\n"
            "   - The question should define a term, concept, or key word from the provided text.\n"
            "   - The answer must be **exactly one word** (No phrases, numerical values, or True/False answers).\n"
            "   - ❌ **Incorrect Example:** ['Liquid Ratio', '0.54 : 1'] (Numerical, not a term)\n"
            "   - ✅ **Correct Example:** ['The ratio that measures a company's ability to pay short-term liabilities using liquid assets.', 'Liquidity']\n"
            "\n"
            "2️⃣ **Ensure the question provides sufficient information.**\n"
            "   - Before finalizing the question, **first attempt to answer it yourself.**\n"
            "   - If the answer is unclear or requires more context, **modify the question** to make it complete.\n"
            "   - ❌ **Incorrect Example:** ['What is this process called?', 'Photosynthesis'] (Too vague, missing context)\n"
            "   - ✅ **Correct Example:** ['The process in which green plants use sunlight to synthesize nutrients from carbon dioxide and water.', 'Photosynthesis']\n"
            "\n"
            "3️⃣ **Frame the question in a definition-based format.**\n"
            "   - The question must describe a term or concept that the user can recognize and answer in one word.\n"
            "   - ❌ **Incorrect Example:** ['Liquid Ratio', '0.54 : 1'] (Not framed as a question)\n"
            "   - ✅ **Correct Example:** ['The ratio that measures a company's ability to pay short-term liabilities using liquid assets.', 'Liquidity']\n"
            "\n"
            "4️⃣ **Use only the provided text to generate the question.**\n"
            "   - Do not introduce external concepts or modify definitions beyond the textbook scope.\n"
            "   - The question must strictly relate to the chapter and page it is extracted from.\n"
            "\n"
            "5️⃣ **Ensure academic accuracy and exam relevance.**\n"
            "   - The question must be factually and scientifically accurate.\n"
            "   - Avoid questions that are misleading, outdated, or speculative.\n"
            "\n"
            "6️⃣ **Avoid vague, ambiguous, or incomplete questions.**\n"
            "   - The user should not have to guess the context or meaning of the question.\n"
            "   - ❌ **Incorrect Example:** ['What is the amount of discount given on the issue of debentures?', '45,000'] (Numerical and incomplete)\n"
            "   - ✅ **Correct Example:** ['The financial term for the reduction applied to a debenture's face value before issuance.', 'Discount']\n"
            "\n"
            "### **🔹 Subject-Specific Guidelines:**\n"
            "📘 **Science (Physics, Chemistry, Biology):**\n"
            "   - Questions should define scientific terms, processes, or phenomena.\n"
            "   - ✅ **Correct Example:** ['The smallest unit of an element that retains its chemical properties.', 'Atom']\n"
            "   - ❌ **Incorrect Example:** ['What is the name of this?', 'Diffusion'] (Too vague)\n"
            "\n"
            "📙 **Mathematics:**\n"
            "   - Questions should ask for the definition of mathematical terms, theorems, or properties.\n"
            "   - ✅ **Correct Example:** ['A polygon with four sides.', 'Quadrilateral']\n"
            "   - ❌ **Incorrect Example:** ['Find the value of x in 2x+3=7.', '2'] (Not a one-word conceptual answer)\n"
            "\n"
            "📗 **Social Science (History, Geography, Civics, Economics):**\n"
            "   - Questions should focus on important terms, concepts, and historical events.\n"
            "   - ✅ **Correct Example:** ['The economic system where the means of production are owned by private individuals.', 'Capitalism']\n"
            "   - ❌ **Incorrect Example:** ['Who was the first Prime Minister of India?', 'Jawaharlal Nehru'] (Not a definition-based question)\n"
            "\n"
            "📕 **Accountancy & Business Studies:**\n"
            "   - Questions should be based on key financial and business concepts.\n"
            "   - ✅ **Correct Example:** ['A financial statement that shows a company’s revenues and expenses over a period of time.', 'Income Statement']\n"
            "   - ❌ **Incorrect Example:** ['Net profit is calculated by subtracting _______ from total revenue.', 'Expenses'] (Not a complete definition)\n"
            "\n"
            "### **🔹 Response Format:**\n"
            "Your response must strictly follow this format:\n"
            "['Question', 'Answer', 'Explanation', 'Page number', 'Chapter name']\n"
            "\n"
            "### **Text Details:**\n"
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
    print(response.json()["choices"][0]["message"]["content"])
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