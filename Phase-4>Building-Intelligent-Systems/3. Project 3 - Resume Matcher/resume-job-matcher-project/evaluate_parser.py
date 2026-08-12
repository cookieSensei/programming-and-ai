from evaluation_data import TEST_CASES
from job_matcher import (
    KNOWN_SKILLS,
    extract_required_skills,
    match_exact_skills,
)


def main():
    print("Resume ↔ Job Matcher evaluation cases")
    print("=" * 50)

    for case in TEST_CASES:
        required, preferred = extract_required_skills(
            case["job"],
            KNOWN_SKILLS,
        )

        print(f"\n--- {case['name']} ---")
        print("Required:", required)
        print("Preferred:", preferred)
        print("Expected category:", case["expected_category"])

        # This file deliberately evaluates extraction separately from
        # embedding thresholds so students can inspect each failure source.
        resume_skills = set()
        exact = match_exact_skills(resume_skills, required + preferred)
        print("Exact matches:", sorted(exact["matched"]))
        print("Missing:", sorted(exact["missing"]))


if __name__ == "__main__":
    main()
