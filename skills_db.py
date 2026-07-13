"""
Predefined skills database used for matching resumes against job descriptions.
Organized by category purely for readability/maintenance -- matching itself
is done against the flattened master list.
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
        "sql", "bash", "shell scripting", "dart", "objective-c"
    ],
    "Web Development": [
        "html", "css", "react", "reactjs", "angular", "vue", "vuejs", "node.js",
        "nodejs", "express.js", "django", "flask", "fastapi", "spring boot",
        "asp.net", "next.js", "graphql", "rest api", "restful api", "webpack",
        "tailwind css", "bootstrap", "jquery", "redux"
    ],
    "Data Science & ML": [
        "machine learning", "deep learning", "natural language processing", "nlp",
        "computer vision", "data analysis", "data visualization", "statistics",
        "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "opencv", "spacy", "nltk", "matplotlib", "seaborn", "plotly",
        "power bi", "tableau", "hugging face", "transformers", "llm",
        "generative ai", "predictive modeling", "feature engineering",
        "a/b testing", "time series analysis", "xgboost", "reinforcement learning"
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
        "cassandra", "dynamodb", "elasticsearch", "firebase", "mariadb",
        "microsoft sql server", "nosql"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud platform", "docker", "kubernetes",
        "jenkins", "ci/cd", "terraform", "ansible", "linux", "git", "github",
        "gitlab", "bitbucket", "cloudformation", "microservices", "serverless",
        "devops", "prometheus", "grafana", "nginx", "load balancing"
    ],
    "Tools & Platforms": [
        "jira", "confluence", "slack", "figma", "postman", "vs code",
        "visual studio", "excel", "spss", "sas", "airflow", "spark",
        "apache spark", "hadoop", "kafka", "streamlit", "gradio", "docker compose"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "project management",
        "collaboration", "adaptability", "creativity", "presentation skills",
        "stakeholder management", "agile", "scrum", "analytical skills",
        "attention to detail", "decision making", "mentoring"
    ],
    "Mobile Development": [
        "android", "ios", "react native", "flutter", "xamarin", "swift ui"
    ],
}

# Flattened lookup list used by the PhraseMatcher
MASTER_SKILLS_LIST = sorted({skill for group in SKILLS_DB.values() for skill in group})
