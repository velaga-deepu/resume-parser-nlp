# Resume Parser (NLP)

Extracts structured information — name, email, phone, skills, and education — from plain-text resume content, using a mix of NLP and pattern matching.

## Problem
Wanted hands-on experience with the kind of text-extraction tooling real hiring platforms use behind the scenes to process resumes automatically.

## Features
- Detects candidate name using spaCy's named entity recognition
- Extracts email and phone number using regex pattern matching
- Matches against a known skills list using whole-word matching (avoids false positives)
- Finds education lines by scanning for common degree keywords

## Tech Stack
Python, spaCy (NLP), regex

## How to Run
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python resume_parser.py
```
Paste resume text when prompted, then type `END` on its own line.

## Bugs Found and Fixed
- Initial skill matching used plain substring search, which incorrectly matched "c" inside unrelated words like "Science." Fixed by switching to word-boundary regex matching.
- Initial phone regex failed on space-separated formats like "+91 98765 43210." Fixed by adjusting the pattern to handle variable-length space-separated digit groups.

## Future Improvements
- Support parsing directly from PDF/DOCX files instead of pasted text
- Expand the skills list to be loaded from an external file
- Improve education extraction to also capture graduation year separately

## What I learned
That real-world text extraction often breaks on edge cases that look fine at first glance (like short skill names or varied phone formats), and how word-boundary matching and testing against realistic sample data catches these before they become bigger problems.
