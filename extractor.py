import re
import PyPDF2
import json

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to parse the text and extract questions, options, and answers
def parse_questions(text):
    questions = []
    lines = text.split("\n")
    
    current_question = None
    current_options = []
    correct_answer = None

    for line in lines:
        line = line.strip()
        
        # Identify a question line, assuming questions start with a number
        question_match = re.match(r'^\d+\.\s+(.*)', line)
        if question_match:
            # Save the current question if exists
            if current_question:
                questions.append({
                    "question": current_question,
                    "options": current_options,
                    "correct_answer": correct_answer
                })

            # Reset for the next question
            current_question = question_match.group(1)
            current_options = []
            correct_answer = None
            continue

        # Identify options (A, B, C, D format)
        option_match = re.match(r'^[A-D]\.\s+(.*)', line)
        if option_match:
            current_options.append(option_match.group(1))
            continue

        # Identify the correct answer (e.g., "Correct Answer: A")
        answer_match = re.match(r'^Correct Answer:\s+([A-D])', line)
        if answer_match:
            correct_answer = answer_match.group(1)
            continue

    # Add the last question
    if current_question:
        questions.append({
            "question": current_question,
            "options": current_options,
            "correct_answer": correct_answer
        })
    
    return questions

# Function to save questions to JSON format (this can later be used for DB upload)
def save_to_json(questions, output_file='questions.json'):
    with open(output_file, 'w') as f:
        json.dump(questions, f, indent=4)

# Main execution
if __name__ == "__main__":
    pdf_path = 'path_to_your_pdf_file.pdf'
    
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Parse the questions, options, and answers
    questions = parse_questions(extracted_text)
    
    # Save the parsed questions to a JSON file (can be used to upload to DB)
    save_to_json(questions)

    print("Questions extracted and saved to JSON file.")
