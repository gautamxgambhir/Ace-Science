import json
import os
import random
# from PyPDF2 import PdfReader

# def process_pdf(pdf_path, chapter_name):
#     """
#     Extract text from a PDF file and associate it with page numbers using PyPDF2.
#     """
#     reader = PdfReader(pdf_path)
#     chapter_data = {"chapter": chapter_name, "pages": []}
    
#     for page_num, page in enumerate(reader.pages, start=1):
#         text = page.extract_text()
#         if text.strip():  # Avoid blank pages
#             chapter_data["pages"].append({"page": page_num, "text": text.strip()})
    
#     return chapter_data

# def save_chapters_to_json(pdf_paths, output_file=f"{str(input("name : "))}.json"):
#     """
#     Process multiple PDFs and save the extracted data as a JSON file.
#     """
#     all_chapters = []
#     for chapter_name, pdf_path in pdf_paths.items():
#         if os.path.exists(pdf_path):
#             print(f"Processing {chapter_name}...")
#             chapter_data = process_pdf(pdf_path, chapter_name)
#             all_chapters.append(chapter_data)
#         else:
#             print(f"File not found: {pdf_path}")
    
#     with open(output_file, "w", encoding="utf-8") as file:
#         json.dump(all_chapters, file, ensure_ascii=False, indent=4)
#     print(f"Chapters saved to {output_file}")

# pdf_files = {
#     "Chapter 1: Integrals": "lemh201.pdf",
#     "Chapter 2: Application of Integrals": "lemh202.pdf",
#     "Chapter 3: Differential Equations": "lemh203.pdf",
#     "Chapter 4: Vector Algebra": "lemh204.pdf",
#     "Chapter 5: Three-Dimensional Geometry": "lemh205.pdf",
#     "Chapter 6: Linear Programming": "lemh206.pdf",
#     "Chapter 7: Probability": "lemh207.pdf"
# }

# save_chapters_to_json(pdf_files)

def select_random_page(chapter_name="all", data_file="chemistry10.json"):
    if data_file == "all9.json":
        random_data_file = random.choice(["chemistry9.json", "physics9.json", "biology9.json", "history9.json", "geography9.json", "political_science9.json", "economics.json"])
        with open(f"subjects/{random_data_file}", "r", encoding="utf-8") as file:
            chapters_data = json.load(file)
        if chapter_name != "all":
            chapter = next((ch for ch in chapters_data if ch["chapter"] == chapter_name), None)
        else:
            chapter = random.choice(chapters_data)
        page = random.choice(chapter["pages"])
        data_list = [chapter["chapter"], page["page"], page["text"]]
        return data_list
    elif data_file == "all10.json":
        random_data_file = random.choice(["chemistry10.json", "physics10.json", "biology10.json", "history10.json", "geography10.json", "political_science10.json", "economics10.json"])
        with open(f"subjects/{random_data_file}", "r", encoding="utf-8") as file:
            chapters_data = json.load(file)
        if chapter_name != "all":
            chapter = next((ch for ch in chapters_data if ch["chapter"] == chapter_name), None)
        else:
            chapter = random.choice(chapters_data)
        page = random.choice(chapter["pages"])
        data_list = [chapter["chapter"], page["page"], page["text"]]
        return data_list
    else:
        with open(f"subjects/{data_file}", "r", encoding="utf-8") as file:
            chapters_data = json.load(file)
        if chapter_name != "all":
            chapter = next((ch for ch in chapters_data if ch["chapter"] == chapter_name), None)
        else:
            chapter = random.choice(chapters_data)
        page = random.choice(chapter["pages"])
        data_list = [chapter["chapter"], page["page"], page["text"]]
        return data_list