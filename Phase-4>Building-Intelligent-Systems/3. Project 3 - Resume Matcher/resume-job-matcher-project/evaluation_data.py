TEST_CASES = [
    {
        "name": "strong_match",
        "job": """
        Machine Learning Engineer

        Required Qualifications:
        Python
        Machine Learning
        SQL
        Computer Vision

        Preferred:
        AWS
        Docker
        Kubernetes
        """,
        "resume": """
        John Smith

        Python developer and machine learning engineer.

        Skills:
        Python
        SQL
        Machine Learning
        OpenCV
        TensorFlow
        Docker

        Experience:
        Built image classification systems using convolutional neural networks.
        Developed predictive models and data pipelines.
        """,
        "expected_category": "Strong Match",
    },
    {
        "name": "weak_match",
        "job": """
        Machine Learning Engineer

        Required Qualifications:
        Python
        Machine Learning
        SQL
        Computer Vision

        Preferred:
        AWS
        Docker
        """,
        "resume": """
        Jane Smith

        Software developer.

        Skills:
        Java
        JavaScript
        HTML
        CSS

        Experience:
        Built web applications and ecommerce websites.
        """,
        "expected_category": "Weak Match",
    },
]
