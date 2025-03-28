<div align="center">
  <img src="https://i.ibb.co/tMKrCgxy/acencert.png" alt="AceNCERT Logo"><br>
</div>

-----------------

# AceNCERT: AI-Powered NCERT Question Generator & Validator

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-red)
![Vercel](https://img.shields.io/badge/hosted%20on-Vercel-black)
![Together-AI](https://img.shields.io/badge/Together%20AI-0f6fff)

## What is it?

AceNCERT is an AI-powered tool designed to generate and validate questions from NCERT textbooks for **Classes 9 to 12**. It utilizes **Flask** for the backend, **Together API** for AI-driven question generation and answer validation, and a clean **HTML, CSS, and JavaScript** frontend.

With **AceNCERT**, you can:
- Get text from **random pages** of NCERT books for a selected class and subject.
- Generate different types of questions (**MCQs, one-word answers, and True/False**) using AI.
- Validate the correctness of answers using AI.

## How It Works

1. **NCERT PDFs Processing**: 
   - Official **NCERT PDFs** for **Classes 9-12** were downloaded and preprocessed using Python.
   - Converted into structured **JSON format** for fast retrieval.

2. **Random Page Selection**:
   - Users select a **Class** and **Subject**.
   - A random page from the selected subject's book is retrieved.

3. **AI Question Generation & Validation**:
   - Together API generates **customized questions** from the extracted text.
   - AI also validates answers, ensuring correctness.

## Where to Access It?

AceNCERT is hosted on Vercel and available online:

🔗 **[Live Demo](https://ace-ncert.vercel.app/)**

## Installation and Setup

### 1. Clone the repository:
```bash
 git clone https://github.com/gautamxgambhir/AceNCERT.git
```

### 2. Install dependencies:
```bash
cd AceNCERT
pip install -r requirements.txt
```

### 3. Run the Flask server:
```bash
python app.py
```

### 4. Deploy on Vercel:
- Install Vercel CLI if not already installed:
```bash
npm install -g vercel
```
- Deploy using:
```bash
vercel
```

## Usage

Once deployed or running locally, users can:

- **Select Class & Subject** to fetch a random page from NCERT books.
- **Generate AI-powered questions** based on the page content.
- **Validate answers** using AI to check correctness.

## Dependencies

- [**Flask**](https://flask.palletsprojects.com/en/3.0.x/) - Backend framework for handling requests.
- [**Together API**](https://www.together.ai/) - AI-powered question generation and validation.
- [**PyMuPDF**](https://pymupdf.readthedocs.io/en/latest/) - Processing NCERT PDFs and extracting text.
- [**HTML, CSS, JavaScript**] - Frontend for user interaction.
- [**Vercel**](https://vercel.com/) - Hosting platform.

## Contributing

Contributions are welcome! To contribute:
- Fork the repo.
- Create a new branch (`git checkout -b feature-branch`).
- Commit changes (`git commit -m "Added new feature"`).
- Push to the branch (`git push origin feature-branch`).
- Open a pull request.

## License

This project is licensed under the **MIT License**.

## Contact

- **GitHub**: [@gautamxgambhir](https://github.com/gautamxgambhir)
- **Email**: ggambhir1919@gmail.com
- **Instagram**: [gautamxgambhir](https://www.instagram.com/gautamxgambhir)
- **Twitter**: [gautamxgambhir](https://www.twitter.com/gautamxgambhir)
