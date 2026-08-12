from evaluation_data import TEST_CASES
from resume_parser import parse_resume


def evaluate_skills(predicted, expected):
    predicted = {x.lower() for x in predicted}
    expected = {x.lower() for x in expected}
    tp = len(predicted & expected)
    fp = len(predicted - expected)
    fn = len(expected - predicted)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


for case in TEST_CASES:
    predicted = parse_resume(case["text"])
    expected = case["expected"]

    print(f"\n--- {case['name']} ---")
    print("Name:", predicted["name"])
    print("Email:", predicted["email"])
    print("Skills:", predicted["skills"])

    p, r, f1 = evaluate_skills(predicted["skills"], expected["skills"])
    print(f"Skills precision: {p:.2f}")
    print(f"Skills recall:    {r:.2f}")
    print(f"Skills F1:        {f1:.2f}")
