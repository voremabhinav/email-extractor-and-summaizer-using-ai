import spacy
from spacy.matcher import Matcher

# Load spaCy's English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_requirements(text: str) -> dict:
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Patterns to detect requirements based on modal verbs (must, shall, should, need to)
    pattern_req = [
        {"POS": "NOUN", "OP": "*"},
        {"LOWER": {"IN": ["must", "shall", "should", "needs", "need"]}},
        {"LOWER": "to", "OP": "?"},
        {"POS": "VERB"},
        {"POS": "NOUN", "OP": "+"}
    ]
    matcher.add("REQUIREMENT_PATTERN", [pattern_req])

    matches = matcher(doc)
    extracted_items = []

    for match_id, start, end in matches:
        span = doc[start:end]
        extracted_items.append(span.text)

    # Classify dependencies/tech stack keywords
    tech_keywords = [token.text for token in doc if token.pos_ == "PROPN"]

    return {
        "extracted_requirements": list(set(extracted_items)),
        "technologies_mentioned": list(set(tech_keywords))
    }

# Example Usage
raw_project_text = """
The system must support secure user authentication using OAuth 2.0.
Users shall be able to export financial reports in PDF format.
The application needs to store all data securely inside PostgreSQL.
The dashboard should load within 2 seconds under heavy traffic.
"""

results = extract_requirements(raw_project_text)

print("--- Extracted Requirements ---")
for req in results["extracted_requirements"]:
    print(f"- {req}")

print("\n--- Identified Technologies/Entities ---")
print(", ".join(results["technologies_mentioned"]))