from job_matcher import (
    KNOWN_SKILLS,
    calculate_skill_score,
    exact_skill_match,
    extract_job_skills,
)
from resume_analysis import analyze_resume
from resume_parser import parse_resume
from similarity import calculate_tfidf_similarity


CASES = [
    {
        "name": "strong_match",
        "resume": """
        Jane Doe
        jane@example.com

        Skills
        Python
        SQL
        Machine Learning
        OpenCV
        TensorFlow

        Experience
        Built computer vision applications using Python and OpenCV.
        Developed predictive models using TensorFlow.

        Projects
        Resume intelligence platform
        """,
        "job": """
        Machine Learning Engineer

        Required:
        Python
        SQL
        Machine Learning
        Computer Vision

        Preferred:
        PyTorch
        Docker
        """,
    },
    {
        "name": "weak_match",
        "resume": """
        John Smith
        john@example.com

        Skills
        JavaScript
        TypeScript
        Next.js

        Experience
        Built ecommerce web applications.
        """,
        "job": """
        Machine Learning Engineer

        Required:
        Python
        SQL
        Machine Learning
        Computer Vision
        """,
    },
]


def main():
    for case in CASES:
        resume = parse_resume(case["resume"])
        job_skills = extract_job_skills(
            case["job"],
            KNOWN_SKILLS,
        )
        exact = exact_skill_match(
            resume["skills"],
            job_skills,
        )

        skill_score = calculate_skill_score(
            exact,
            job_skills,
        )

        tfidf = calculate_tfidf_similarity(
            case["resume"],
            case["job"],
        )

        analysis = analyze_resume(resume)

        print("\n" + "=" * 60)
        print(case["name"])
        print("=" * 60)
        print("Skills:", resume["skills"])
        print("Job skills:", job_skills)
        print("Matched:", exact["matched"])
        print("Missing:", exact["missing"])
        print(f"Skill score: {skill_score:.2f}")
        print(f"TF-IDF similarity: {tfidf:.2f}")
        print("Resume statistics:", analysis)


if __name__ == "__main__":
    main()
