"""
Resume Parser
Extracts structured information (email, phone, skills, education) from
plain-text resume content using regex patterns and spaCy for name detection.
"""

import re
import spacy

nlp = spacy.load("en_core_web_sm")

# A small list of skills to search for. In a real-world tool this would be
# a much larger, industry-specific list (or loaded from a file).
KNOWN_SKILLS = [
    "python", "java", "c++", "c", "javascript", "sql", "html", "css",
    "react", "node.js", "flask", "django", "git", "docker", "aws",
    "machine learning", "data analysis", "excel", "project management",
]


def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None


def extract_phone(text):
    # Matches optional country code, then digit groups separated by spaces/dots/dashes,
    # allowing for formats like "+91 98765 43210" or "123-456-7890"
    match = re.search(r"(\+\d{1,3}[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}[-.\s]?\d{0,5}", text)
    return match.group().strip() if match else None


def extract_skills(text):
    """Uses word-boundary matching so short skills like 'c' or 'r' don't
    falsely match inside unrelated words (e.g. 'c' inside 'Science')."""
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found


def extract_name(text):
    """Uses spaCy's named entity recognition to guess the candidate's name.
    Assumes the name appears near the top of the resume, which is typical."""
    doc = nlp(text[:200])  # only check the first chunk, where names usually appear
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_education(text):
    """Looks for common degree keywords and returns the surrounding line."""
    degree_keywords = ["bachelor", "master", "b.tech", "m.tech", "bsc", "msc", "phd", "b.e", "m.e"]
    lines = text.split("\n")
    found_lines = []
    for line in lines:
        if any(keyword in line.lower() for keyword in degree_keywords):
            found_lines.append(line.strip())
    return found_lines


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
    }


def main():
    print("Paste resume text below. When finished, type END on its own line:\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    resume_text = "\n".join(lines)
    result = parse_resume(resume_text)

    print("\n--- Extracted Information ---")
    print(f"Name: {result['name'] or 'Not found'}")
    print(f"Email: {result['email'] or 'Not found'}")
    print(f"Phone: {result['phone'] or 'Not found'}")
    print(f"Skills found: {', '.join(result['skills']) if result['skills'] else 'None found'}")
    print("Education lines found:")
    if result["education"]:
        for line in result["education"]:
            print(f"  - {line}")
    else:
        print("  None found")


if __name__ == "__main__":
    main()