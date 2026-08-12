TEST_CASES = [
    {
        "name": "standard_resume",
        "text": '''
John Smith
john@example.com
+1 555 123 4567
Python Developer
Skills
Python
SQL
TensorFlow
OpenCV
Education
BSc Computer Science
Experience
Software Developer
''',
        "expected": {
            "name": "John Smith",
            "email": "john@example.com",
            "skills": ["Python", "SQL", "TensorFlow", "OpenCV"],
        },
    },
    {
        "name": "different_section_names",
        "text": '''
JANE DOE
Contact Information
jane.doe@example.com
+44 20 1234 5678
Data Scientist
Technical Expertise
Python, Pandas, NumPy
Scikit-learn
Machine Learning
Academic Background
MSc Data Science
Professional Experience
Data Analyst
''',
        "expected": {
            "name": "JANE DOE",
            "email": "jane.doe@example.com",
            "skills": ["Python", "Pandas", "NumPy", "Scikit-learn"],
        },
    },
]
