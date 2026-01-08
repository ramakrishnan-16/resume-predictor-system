=================================
Resume ATS Score Predictor System
=================================

Developed by : Ramakrishnan J
Year         : 2025
Technologies : Python, Django REST Framework, Machine Learning (Rule-based NLP),
               React (Next.js), Bootstrap
Project Type : Resume Analysis & ATS Optimization System

---------------------------------------------------------
ABOUT THE PROJECT
---------------------------------------------------------

The Resume ATS Score Predictor System analyzes resumes and predicts
their compatibility with Applicant Tracking Systems (ATS).
It evaluates resume structure, formatting, content quality, and
basic language accuracy to generate an ATS score along with
actionable improvement suggestions.

This system is designed to work across all industries and resume types,
helping job seekers improve their chances of passing automated
resume screening systems used by recruiters.

---------------------------------------------------------
CORE HIGHLIGHTS
---------------------------------------------------------

* ATS score prediction on a scale of 0–100
* Industry-independent resume evaluation
* PDF and DOCX resume support
* Intelligent resume structure validation
* Detection of missing key resume sections
* Formatting and readability analysis
* Spelling and bullet-point usage checks
* Clear verdict classification based on ATS score
* Modern, responsive web interface
* REST API-based backend architecture

---------------------------------------------------------
ATS SCORE INTERPRETATION
---------------------------------------------------------

0 – 39   : Very poor – auto-rejected  
40 – 59  : Below average – low chance  
60 – 69  : Average – may pass ATS  
70 – 79  : Good – shortlisted  
80 – 89  : Very strong – high priority  
90 – 100 : Excellent – near-perfect match  

---------------------------------------------------------
HOW THE SYSTEM WORKS
---------------------------------------------------------

* User uploads a resume (PDF or DOCX) via the web interface
* Resume text is extracted using PDFPlumber and python-docx
* Resume validity is checked using structural and keyword analysis
* ATS checks evaluate:
  - Contact information
  - Required sections (Education, Skills, Projects, Experience)
  - Resume length and formatting
  - Bullet point usage
  - Spelling accuracy
* Each issue applies a weighted score penalty
* Final ATS score and verdict are generated
* Improvement suggestions are returned dynamically via API
* Frontend displays score, verdict, issues, and suggestions

---------------------------------------------------------
TECHNOLOGIES USED
---------------------------------------------------------

Backend:
* Python
* Django
* Django REST Framework
* Regular Expressions (NLP-based rule engine)

Frontend:
* Next.js (React)
* Bootstrap
* Axios

Libraries:
* pdfplumber
* python-docx
* pyspellchecker

---------------------------------------------------------
REQUIRED LIBRARIES
---------------------------------------------------------

pip install django djangorestframework
pip install pdfplumber python-docx pyspellchecker
pip install numpy pandas


---------------------------------------------------------
TO RUN THE PROJECT
---------------------------------------------------------

Backend:
python manage.py runserver


Frontend:
npm install
npm run dev

---------------------------------------------------------
FUTURE ENHANCEMENTS
---------------------------------------------------------

* Skill relevance scoring using job descriptions
* AI-based resume rewriting suggestions
* Multi-language resume support
* Resume keyword density analysis
* Downloadable ATS improvement report

---------------------------------------------------------
NOTES
---------------------------------------------------------

* This system follows ATS-friendly evaluation logic
* Scores are heuristic-based and simulate real ATS behavior
* Excellent resumes may still receive minor suggestions for optimization
* Resume content accuracy depends on extracted text quality
* Designed for educational, research, and portfolio purposes
* Not affiliated with any commercial ATS provider