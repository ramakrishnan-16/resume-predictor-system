import re
import docx
import pdfplumber
from spellchecker import SpellChecker
from datetime import datetime

spell = SpellChecker()

def extract_text(file):
    if not file.name.lower().endswith((".pdf", ".docx")):
        raise ValueError("Only PDF or DOCX files are supported")

    text = ""

    if file.name.lower().endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    else:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text.lower().strip()

def is_probable_resume(text):
    core_sections = [
        "education", "experience", "skills",
        "projects", "certifications", "summary",
        "profile", "internship", "freelance"
    ]

    found = sum(1 for s in core_sections if s in text)
    word_count = len(text.split())

    if word_count < 180:
        return False, "File content too short to be a resume"

    if found < 2:
        return False, "Uploaded file does not match resume structure"

    return True, None

def extract_experience_block(text):
    patterns = [
        r"(work experience|experience|employment)(.*?)(education|skills|projects|certifications|$)",
        r"(freelance|freelancer|self-employed)(.*?)(education|skills|projects|certifications|$)",
        r"(internship|intern)(.*?)(education|skills|projects|certifications|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(0)

    return ""

def estimate_experience_years(text):
    """
    ATS-safe logic:
    - Supports years + months
    - Counts internship partially
    - Detects freelancing
    - Never fabricates experience
    """

    current_year = datetime.now().year
    exp_text = extract_experience_block(text)

    if not exp_text:
        return 0

    total_months = 0

    explicit_years = re.findall(r"(\d+(?:\.\d+)?)\s+years?", exp_text)
    for y in explicit_years:
        total_months += int(float(y) * 12)

    year_month = re.findall(r"(\d+)\s+years?\s+(\d+)\s+months?", exp_text)
    for y, m in year_month:
        total_months += int(y) * 12 + int(m)

    months_only = re.findall(r"(\d+)\s+months?", exp_text)
    for m in months_only:
        total_months += int(m)

    ranges = re.findall(
        r"(19\d{2}|20\d{2})\s*(?:-|to)\s*(present|current|19\d{2}|20\d{2})",
        exp_text
    )

    for start, end in ranges:
        start_year = int(start)
        end_year = current_year if end in ["present", "current"] else int(end)
        if end_year > start_year:
            total_months += (end_year - start_year) * 12

    if "intern" in exp_text:
        total_months = int(total_months * 0.75)

    if any(k in exp_text for k in ["freelance", "freelancer", "self-employed"]):
        total_months = int(total_months * 1.0)

    return round(total_months / 12, 1)

def check_contact(text):
    issues, suggestions, penalty = [], [], 0

    if not re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text):
        issues.append("Email not found")
        suggestions.append("Add a professional email address")
        penalty -= 15

    if not re.search(r"\+?\d[\d\s\-]{8,}", text):
        issues.append("Phone number not found")
        suggestions.append("Add a valid phone number")
        penalty -= 15

    return issues, suggestions, penalty

def check_sections(text):
    issues, suggestions, penalty = [], [], 0

    required = {
        "education": 10,
        "skills": 10,
        "experience": 10,
        "projects": 5
    }

    for sec, p in required.items():
        if sec not in text:
            issues.append(f"Missing section: {sec.title()}")
            suggestions.append(f"Add a {sec.title()} section")
            penalty -= p

    return issues, suggestions, penalty

def check_length(text):
    issues, suggestions, penalty = [], [], 0
    wc = len(text.split())

    if wc < 300:
        issues.append("Resume too short")
        suggestions.append("Add more details and achievements")
        penalty -= 10

    if wc > 1200:
        issues.append("Resume too long")
        suggestions.append("Reduce content to improve ATS parsing")
        penalty -= 10

    return issues, suggestions, penalty

def check_bullets(text):
    bullets = text.count("-") + text.count("•") + text.count("*")
    if bullets < 5:
        return (
            ["Low use of bullet points"],
            ["Use bullet points to improve ATS readability"],
            -5
        )
    return [], [], 0

def check_spelling(text):
    issues, suggestions, penalty = [], [], 0
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text)
    misspelled = spell.unknown(words)

    if misspelled:
        issues.append("Spelling mistakes detected")
        suggestions.append("Proofread resume for spelling errors")
        penalty -= min(len(misspelled), 10)

    return issues, suggestions, penalty

def ats_score_meaning(score):
    if score <= 39:
        return "Very poor – auto-rejected"
    if score <= 59:
        return "Below average – low chance"
    if score <= 69:
        return "Average – may pass ATS"
    if score <= 79:
        return "Good – shortlisted"
    if score <= 89:
        return "Very strong – high priority"
    return "Excellent – near-perfect match"

def analyze_resume(file):
    text = extract_text(file)

    valid, reason = is_probable_resume(text)
    if not valid:
        return {
            "is_resume": False,
            "message": reason
        }

    score = 100
    raw_issues, raw_suggestions = [], []

    checks = [
        check_contact(text),
        check_sections(text),
        check_length(text),
        check_bullets(text),
        check_spelling(text)
    ]

    for issues, suggestions, penalty in checks:
        raw_issues.extend(issues)
        raw_suggestions.extend(suggestions)
        score += penalty

    experience_years = estimate_experience_years(text)

    if experience_years < 5:
        resume_length_advice = "Recommended resume length: 1 page"
    else:
        resume_length_advice = "Resume length acceptable for experienced professionals"

    score = max(0, min(100, score))
    verdict = ats_score_meaning(score)

    issues, suggestions = [], []

    if score < 70:
        issues = raw_issues
        suggestions = raw_suggestions
    elif score < 85:
        suggestions = raw_suggestions[:4]
    elif score < 95:
        suggestions = [
            "Minor improvements possible, but resume is ATS-friendly"
        ]
    else:
        suggestions = [
            "Resume is well-optimized and ATS compliant"
        ]

    return {
        "is_resume": True,
        "ats_score": score,
        "verdict": verdict,
        "experience_years": experience_years,
        "resume_length_advice": resume_length_advice,
        "issues": list(set(issues)),
        "suggestions": list(set(suggestions))
    }