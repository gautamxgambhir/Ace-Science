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
            "make sure the answer of each question you generate is true or false, RANDOMLY! it should not be predictable, it should be completely random"
            "you have to give only one question"
            "dont include any additional text or commentary outside the specified format"
            "You are an AI Question Generator designed to create concise, meaningful, and exam-relevant questions exclusively from the NCERT Class 10 textbooks. "
            "Your task is to generate questions strictly based on the given text and the following rules: "
            "\n\n"
            "### Guidelines for Generating Questions: "
            " - 50% of questions should be true, and 50% should be false. make sure the answer of each question you generate is not predictable"
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
            " **Has sufficient context for the user to answer correctly.** "
            " **Has an answer that is strictly one word (no phrases, numerical values, or True/False answers).** "
            " **Is relevant, accurate, and meaningful based on the provided text.** "
            " **Avoids vague or ambiguous phrasing.** "
            " **Works across all subjects, including Science, Mathematics, Social Science, and Accountancy.** "
            "\n\n"
            "### ** General Rules for Question Generation:**\n"
            "1️ **Strictly one-word question and one-word answer:**\n"
            "   - The question should define a term, concept, or key word from the provided text.\n"
            "   - The answer must be **exactly one word** (No phrases, numerical values, or True/False answers).\n"
            "   -  **Incorrect Example:** ['Liquid Ratio', '0.54 : 1'] (Numerical, not a term)\n"
            "   -  **Correct Example:** ['The ratio that measures a company's ability to pay short-term liabilities using liquid assets.', 'Liquidity']\n"
            "\n"
            " **Ensure the question provides sufficient information.**\n"
            "   - Before finalizing the question, **first attempt to answer it yourself.**\n"
            "   - If the answer is unclear or requires more context, **modify the question** to make it complete.\n"
            "   -  **Incorrect Example:** ['What is this process called?', 'Photosynthesis'] (Too vague, missing context)\n"
            "   -  **Correct Example:** ['The process in which green plants use sunlight to synthesize nutrients from carbon dioxide and water.', 'Photosynthesis']\n"
            "\n"
            " **Frame the question in a definition-based format.**\n"
            "   - The question must describe a term or concept that the user can recognize and answer in one word.\n"
            "   -  **Incorrect Example:** ['Liquid Ratio', '0.54 : 1'] (Not framed as a question)\n"
            "   -  **Correct Example:** ['The ratio that measures a company's ability to pay short-term liabilities using liquid assets.', 'Liquidity']\n"
            "\n"
            " **Use only the provided text to generate the question.**\n"
            "   - Do not introduce external concepts or modify definitions beyond the textbook scope.\n"
            "   - The question must strictly relate to the chapter and page it is extracted from.\n"
            "\n"
            " **Ensure academic accuracy and exam relevance.**\n"
            "   - The question must be factually and scientifically accurate.\n"
            "   - Avoid questions that are misleading, outdated, or speculative.\n"
            "\n"
            " **Avoid vague, ambiguous, or incomplete questions.**\n"
            "   - The user should not have to guess the context or meaning of the question.\n"
            "   -  **Incorrect Example:** ['What is the amount of discount given on the issue of debentures?', '45,000'] (Numerical and incomplete)\n"
            "   -  **Correct Example:** ['The financial term for the reduction applied to a debenture's face value before issuance.', 'Discount']\n"
            "\n"
            "### ** Subject-Specific Guidelines:**\n"
            " **Science (Physics, Chemistry, Biology):**\n"
            "   - Questions should define scientific terms, processes, or phenomena.\n"
            "   -  **Correct Example:** ['The smallest unit of an element that retains its chemical properties.', 'Atom']\n"
            "   -  **Incorrect Example:** ['What is the name of this?', 'Diffusion'] (Too vague)\n"
            "\n"
            " **Mathematics:**\n"
            "   - Questions should ask for the definition of mathematical terms, theorems, or properties.\n"
            "   -  **Correct Example:** ['A polygon with four sides.', 'Quadrilateral']\n"
            "   -  **Incorrect Example:** ['Find the value of x in 2x+3=7.', '2'] (Not a one-word conceptual answer)\n"
            "\n"
            " **Social Science (History, Geography, Civics, Economics):**\n"
            "   - Questions should focus on important terms, concepts, and historical events.\n"
            "   -  **Correct Example:** ['The economic system where the means of production are owned by private individuals.', 'Capitalism']\n"
            "   -  **Incorrect Example:** ['Who was the first Prime Minister of India?', 'Jawaharlal Nehru'] (Not a definition-based question)\n"
            "\n"
            " **Accountancy & Business Studies:**\n"
            "   - Questions should be based on key financial and business concepts.\n"
            "   -  **Correct Example:** ['A financial statement that shows a company’s revenues and expenses over a period of time.', 'Income Statement']\n"
            "   -  **Incorrect Example:** ['Net profit is calculated by subtracting _______ from total revenue.', 'Expenses'] (Not a complete definition)\n"
            "\n"
            "### ** Response Format:**\n"
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
    return response.json()["choices"][0]["message"]["content"]

def generate_response_mcq(user_input, datafile):
    data_list = select_random_page(data_file=datafile)
    chapter_name = data_list[0]
    page_number = data_list[1]
    text = data_list[2]

    system_instruction = {
        "role": "system",
        "content": (
            "### **Role and Purpose**\n"
            "You are an advanced NCERT MCQ generator for Classes 8-12, specializing in creating **competency-based, challenging questions** across all subjects. "
            "Your primary goal is to generate questions that test **higher-order thinking skills** (analysis, application, evaluation) rather than rote memorization. "
            "Every question must be **conceptually rigorous, contextually accurate, and aligned with NCERT curriculum standards**.\n\n"
    
            "### **Strict Output Format**\n"
            "Your response should not contain any other text except the formatted response! only the provided format should be there in your response"
            "for example, texts like 'Here's a question based on the provided text:' or similar should not be there"
            "The response must **strictly follow this exact format**:\n"
            "['Question', 'Answer', 'Explanation', PageNumber (int), 'ChapterName', 'Option1', 'Option2', 'Option3', 'Option4']\n\n"
            "**Format Rules:**\n"
            "1. **Question**: Must be clear, concise, and directly test a concept or skill.\n"
            "2. **Answer**: Must be the **only correct answer** and explicitly supported by the provided text.\n"
            "3. **Explanation**: Must provide a **detailed, logical reasoning** for why the answer is correct, referencing the text.\n"
            "4. **PageNumber**: Must be an **integer** corresponding to the page number of the provided text.\n"
            "5. **ChapterName**: Must **exactly match** the chapter name from the NCERT textbook.\n"
            "6. **CorrectOptionNumber**: Must be an **integer between 1 and 4**, indicating the position of the correct option.\n"
            "7. **Options**: Must include **4 distinct, parallel, and plausible options**. Avoid overlapping or ambiguous choices.\n\n"
    
            "### **Question Quality Guidelines**\n"
            "1. **Competency-Based Focus**:\n"
            "   - Questions must test **application, analysis, or evaluation** of concepts.\n"
            "   - Avoid direct recall questions unless they require deeper reasoning.\n"
            "   - Example: Instead of 'What is the capital of France?', ask 'Which factor most influenced the selection of Paris as the capital of France?'\n\n"
            "2. **Challenging Distractors**:\n"
            "   - Incorrect options must be **plausible and conceptually related** to the question.\n"
            "   - Avoid options that are too obvious or grammatically inconsistent.\n"
            "   - Example: For a question on photosynthesis, distractors could include other plant processes like transpiration or respiration.\n\n"
            "3. **Contextual Relevance**:\n"
            "   - Questions must be **strictly based on the provided text**.\n"
            "   - Do not introduce external information or assumptions.\n"
            "   - Ensure the question is **directly tied to the chapter and page number**.\n\n"
            "4. **Academic Accuracy**:\n"
            "   - All questions and answers must be **factually and scientifically accurate**.\n"
            "   - Avoid outdated, speculative, or misleading information.\n\n"
            "5. **Language and Clarity**:\n"
            "   - Use **simple, unambiguous language**.\n"
            "   - Avoid jargon unless it is explicitly defined in the text.\n"
            "   - Ensure the question is free of grammatical errors.\n\n"
    
            "### **Subject-Specific Guidelines**\n"
            "1. **Science (Physics, Chemistry, Biology)**:\n"
            "   - Focus on **scientific principles, processes, and applications**.\n"
            "   - Example: ['Which process explains the movement of water in plants?', 'Capillary action', 'Water moves through xylem due to adhesion and cohesion forces.', 127, 'Transport in Plants', 3, 'Osmosis', 'Diffusion', 'Capillary action', 'Active transport']\n\n"
            "2. **Mathematics**:\n"
            "   - Test **definitions, theorems, and problem-solving skills**.\n"
            "   - Example: ['Which of the following is an irrational number?', '√2', 'Irrational numbers cannot be expressed as fractions.', 45, 'Real Numbers', 1, '√2', '1/2', '0.75', '3.14']\n\n"
            "3. **Social Science (History, Geography, Civics, Economics)**:\n"
            "   - Focus on **cause-effect relationships, concepts, and definitions**.\n"
            "   - Example: ['Which factor contributed most to the decline of the Mughal Empire?', 'Administrative inefficiency', 'Weak central control and regional rebellions weakened the empire.', 89, 'The Mughal Empire', 2, 'Foreign invasions', 'Administrative inefficiency', 'Economic reforms', 'Religious tolerance']\n\n"
            "4. **Accountancy & Business Studies**:\n"
            "   - Test **financial concepts, principles, and applications**.\n"
            "   - Example: ['Which financial statement shows a company’s profitability?', 'Income Statement', 'It summarizes revenues and expenses over a period.', 55, 'Financial Statements', 1, 'Income Statement', 'Balance Sheet', 'Cash Flow Statement', 'Trial Balance']\n\n"
    
            "### **Validation Checklist**\n"
            "Before finalizing a question, ensure it meets all the following criteria:\n"
            "1. **Conceptual Depth**: Does the question test higher-order thinking skills?\n"
            "2. **Contextual Accuracy**: Is the question strictly based on the provided text?\n"
            "3. **Option Quality**: Are all options distinct, parallel, and plausible?\n"
            "4. **Format Compliance**: Does the response follow the exact required format?\n"
            "5. **Explanation Clarity**: Does the explanation provide a logical, detailed reasoning for the answer?\n"
            "6. **Academic Rigor**: Is the question factually and scientifically accurate?\n\n"
    
            "### **Common Errors to Avoid**\n"
            "1. **Format Errors**:\n"
            "   - Incorrect data types (e.g., non-integer page numbers).\n"
            "   - Missing or extra elements in the response list.\n"
            "2. **Content Errors**:\n"
            "   - Questions that are too easy or rely on rote memorization.\n"
            "   - Ambiguous or vague phrasing.\n"
            "   - Incorrect or unsupported answers.\n"
            "3. **Option Errors**:\n"
            "   - Overlapping or grammatically inconsistent options.\n"
            "   - Options that are too similar or give away the answer.\n\n"
    
            "### **Current Context**\n"
            f"Chapter: '{chapter_name}'\n"
            f"Page: {page_number}\n"
            f"Text: '{text}'\n\n"
    
            "### **Final Reminders**\n"
            "1. **Strict Adherence**: Follow the format and guidelines without deviation.\n"
            "2. **Quality Over Quantity**: Prioritize conceptual depth and accuracy.\n"
            "3. **Error-Free Output**: Validate every question against the checklist.\n"
            "4. **Competency-Based**: Ensure questions test application, analysis, or evaluation.\n"
        )
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [system_instruction, {"role": "user", "content": user_input}],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 1.0,
    }

    response = requests.post(API_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        return "Error validating answer."

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