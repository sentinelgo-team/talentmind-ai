"""
TalentMind AI - Industry Benchmarks Data
==========================================
Purpose: Centralized industry skill requirement benchmarks
         for various tech roles and experience levels.

This module serves as the knowledge base for skill gap
analysis. It defines what skills are required, preferred,
and bonus for each role at each experience level.

Why Separate Module?
    - Easy to update without touching agent logic
    - Single source of truth for industry requirements
    - Testable independently
    - Can be replaced with DB/API in future versions

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

from typing import Dict, List, Any


# ══════════════════════════════════════════════════════════════════
# INDUSTRY BENCHMARK DEFINITIONS
# ══════════════════════════════════════════════════════════════════

INDUSTRY_BENCHMARKS: Dict[str, Dict[str, Any]] = {

    # ── Python / Backend Developer ────────────────────────────────
    "python_developer": {
        "display_name": "Python Developer",
        "fresher": {
            "must_have": [
                "python", "sql", "git", "html", "css",
                "basic algorithms", "data structures",
            ],
            "good_to_have": [
                "django", "flask", "postgresql", "rest api",
                "linux", "docker basics",
            ],
            "bonus": ["fastapi", "redis", "aws basics", "pytest"],
        },
        "junior": {
            "must_have": [
                "python", "django", "flask", "sql", "git",
                "rest api", "postgresql", "linux",
            ],
            "good_to_have": [
                "docker", "fastapi", "redis", "celery",
                "unit testing", "aws", "ci/cd",
            ],
            "bonus": [
                "kubernetes", "graphql", "elasticsearch",
                "microservices",
            ],
        },
        "mid": {
            "must_have": [
                "python", "django", "fastapi", "postgresql",
                "rest api", "docker", "git", "testing",
                "sql", "redis",
            ],
            "good_to_have": [
                "kubernetes", "aws", "celery", "elasticsearch",
                "microservices", "ci/cd", "system design",
            ],
            "bonus": [
                "terraform", "kafka", "grpc",
                "performance optimization",
            ],
        },
        "senior": {
            "must_have": [
                "python", "system design", "microservices",
                "docker", "kubernetes", "aws", "postgresql",
                "rest api", "ci/cd", "performance optimization",
            ],
            "good_to_have": [
                "terraform", "kafka", "grpc", "elasticsearch",
                "mentoring", "architecture patterns",
            ],
            "bonus": [
                "ml integration", "data engineering",
                "security best practices",
            ],
        },
    },

    # ── Machine Learning Engineer ─────────────────────────────────
    "ml_engineer": {
        "display_name": "ML Engineer",
        "fresher": {
            "must_have": [
                "python", "numpy", "pandas", "scikit-learn",
                "statistics", "linear algebra", "git",
            ],
            "good_to_have": [
                "tensorflow", "pytorch", "matplotlib",
                "jupyter", "sql", "machine learning basics",
            ],
            "bonus": [
                "deep learning", "nlp basics", "kaggle",
                "feature engineering",
            ],
        },
        "junior": {
            "must_have": [
                "python", "tensorflow", "pytorch", "scikit-learn",
                "pandas", "numpy", "sql", "statistics",
                "feature engineering",
            ],
            "good_to_have": [
                "mlflow", "docker", "aws sagemaker",
                "deep learning", "nlp", "model deployment",
            ],
            "bonus": [
                "kubeflow", "spark", "airflow",
                "computer vision",
            ],
        },
        "mid": {
            "must_have": [
                "python", "tensorflow", "pytorch", "mlops",
                "model deployment", "feature engineering",
                "docker", "aws", "sql", "statistics",
            ],
            "good_to_have": [
                "kubeflow", "spark", "airflow", "langchain",
                "llm", "kubernetes", "kafka",
            ],
            "bonus": [
                "custom model architectures", "rl",
                "generative ai", "research papers",
            ],
        },
        "senior": {
            "must_have": [
                "python", "mlops", "system design",
                "model optimization", "distributed training",
                "aws", "kubernetes", "architecture",
                "team leadership",
            ],
            "good_to_have": [
                "llm fine-tuning", "rag", "langchain",
                "research background", "publications",
            ],
            "bonus": [
                "custom hardware optimization",
                "novel architectures", "patents",
            ],
        },
    },

    # ── Full Stack Developer ──────────────────────────────────────
    "full_stack_developer": {
        "display_name": "Full Stack Developer",
        "fresher": {
            "must_have": [
                "html", "css", "javascript", "python",
                "sql", "git", "rest api basics",
            ],
            "good_to_have": [
                "react", "node.js", "flask", "postgresql",
                "responsive design",
            ],
            "bonus": [
                "typescript", "docker basics",
                "aws basics", "testing",
            ],
        },
        "mid": {
            "must_have": [
                "react", "node.js", "python", "javascript",
                "typescript", "postgresql", "rest api",
                "docker", "git", "css",
            ],
            "good_to_have": [
                "aws", "redis", "graphql", "ci/cd",
                "testing", "microservices",
            ],
            "bonus": [
                "kubernetes", "next.js", "websockets",
                "performance optimization",
            ],
        },
        "senior": {
            "must_have": [
                "react", "node.js", "python", "system design",
                "microservices", "docker", "kubernetes",
                "aws", "postgresql", "ci/cd",
            ],
            "good_to_have": [
                "terraform", "kafka", "graphql",
                "security", "mentoring",
            ],
            "bonus": [
                "architecture design", "team leadership",
                "performance engineering",
            ],
        },
    },

    # ── Data Scientist ────────────────────────────────────────────
    "data_scientist": {
        "display_name": "Data Scientist",
        "fresher": {
            "must_have": [
                "python", "statistics", "sql", "pandas",
                "numpy", "matplotlib", "machine learning basics",
            ],
            "good_to_have": [
                "scikit-learn", "tableau", "r",
                "jupyter", "excel",
            ],
            "bonus": [
                "deep learning", "nlp", "spark",
                "power bi",
            ],
        },
        "mid": {
            "must_have": [
                "python", "statistics", "machine learning",
                "sql", "pandas", "scikit-learn",
                "data visualization", "feature engineering",
            ],
            "good_to_have": [
                "tensorflow", "spark", "airflow",
                "tableau", "power bi", "aws",
            ],
            "bonus": [
                "deep learning", "nlp", "causal inference",
                "ab testing",
            ],
        },
        "senior": {
            "must_have": [
                "python", "advanced statistics", "machine learning",
                "sql", "spark", "aws", "experiment design",
                "stakeholder communication",
            ],
            "good_to_have": [
                "causal inference", "bayesian methods",
                "deep learning", "leadership",
            ],
            "bonus": [
                "research publications", "novel methods",
                "cross-functional leadership",
            ],
        },
    },

    # ── DevOps Engineer ───────────────────────────────────────────
    "devops_engineer": {
        "display_name": "DevOps Engineer",
        "fresher": {
            "must_have": [
                "linux", "git", "bash", "docker basics",
                "networking basics", "ci/cd basics",
            ],
            "good_to_have": [
                "aws", "jenkins", "ansible", "python",
                "monitoring basics",
            ],
            "bonus": [
                "kubernetes", "terraform",
                "prometheus", "grafana",
            ],
        },
        "mid": {
            "must_have": [
                "docker", "kubernetes", "aws", "terraform",
                "ci/cd", "linux", "bash", "git",
                "monitoring", "ansible",
            ],
            "good_to_have": [
                "prometheus", "grafana", "elk",
                "vault", "python", "helm",
            ],
            "bonus": [
                "service mesh", "chaos engineering",
                "devsecops",
            ],
        },
        "senior": {
            "must_have": [
                "kubernetes", "aws", "terraform", "ci/cd",
                "security", "system design", "sre practices",
                "incident management", "architecture",
            ],
            "good_to_have": [
                "multi-cloud", "devsecops", "chaos engineering",
                "platform engineering",
            ],
            "bonus": [
                "custom tooling", "open source contributions",
                "team leadership",
            ],
        },
    },

    # ── AI Engineer ───────────────────────────────────────────────
    "ai_engineer": {
        "display_name": "AI Engineer",
        "fresher": {
            "must_have": [
                "python", "machine learning basics", "sql",
                "git", "statistics", "pandas", "numpy",
            ],
            "good_to_have": [
                "langchain", "openai api", "prompt engineering",
                "tensorflow", "pytorch",
            ],
            "bonus": [
                "rag", "vector databases", "llm fine-tuning",
                "langgraph",
            ],
        },
        "mid": {
            "must_have": [
                "python", "langchain", "llm", "prompt engineering",
                "rag", "vector databases", "rest api",
                "docker", "aws",
            ],
            "good_to_have": [
                "langgraph", "fine-tuning", "faiss",
                "pinecone", "mlops", "fastapi",
            ],
            "bonus": [
                "multi-agent systems", "custom llm training",
                "model optimization",
            ],
        },
        "senior": {
            "must_have": [
                "python", "llm architecture", "mlops",
                "system design", "langchain", "langgraph",
                "multi-agent systems", "aws", "kubernetes",
            ],
            "good_to_have": [
                "llm fine-tuning", "custom model training",
                "research background", "team leadership",
            ],
            "bonus": [
                "novel agent architectures", "publications",
                "open source",
            ],
        },
    },
}


# ══════════════════════════════════════════════════════════════════
# LEARNING RESOURCES DATABASE
# ══════════════════════════════════════════════════════════════════

LEARNING_RESOURCES: Dict[str, Dict[str, str]] = {
    "python": {
        "beginner": "https://docs.python.org/3/tutorial/",
        "intermediate": "https://realpython.com",
        "platform": "Coursera / Udemy",
        "duration": "4-8 weeks",
    },
    "django": {
        "beginner": "https://docs.djangoproject.com",
        "platform": "Django Official Docs / Udemy",
        "duration": "3-6 weeks",
    },
    "fastapi": {
        "beginner": "https://fastapi.tiangolo.com",
        "platform": "FastAPI Official Docs",
        "duration": "2-4 weeks",
    },
    "docker": {
        "beginner": "https://docs.docker.com/get-started/",
        "platform": "Docker Official / Udemy",
        "duration": "2-3 weeks",
    },
    "kubernetes": {
        "beginner": "https://kubernetes.io/docs/tutorials/",
        "platform": "KodeKloud / Linux Foundation",
        "duration": "4-8 weeks",
    },
    "aws": {
        "beginner": "https://aws.amazon.com/training/",
        "platform": "AWS Training / A Cloud Guru",
        "duration": "6-12 weeks",
        "certification": "AWS Certified Developer Associate",
    },
    "tensorflow": {
        "beginner": "https://www.tensorflow.org/tutorials",
        "platform": "TensorFlow Official / Coursera",
        "duration": "4-8 weeks",
    },
    "pytorch": {
        "beginner": "https://pytorch.org/tutorials/",
        "platform": "PyTorch Official / Fast.ai",
        "duration": "4-8 weeks",
    },
    "langchain": {
        "beginner": "https://docs.langchain.com",
        "platform": "LangChain Docs / DeepLearning.AI",
        "duration": "2-4 weeks",
    },
    "react": {
        "beginner": "https://react.dev/learn",
        "platform": "React Official / Scrimba",
        "duration": "4-8 weeks",
    },
    "postgresql": {
        "beginner": "https://www.postgresql.org/docs/",
        "platform": "PostgreSQL Official / Udemy",
        "duration": "3-5 weeks",
    },
    "machine learning": {
        "beginner": "https://www.coursera.org/learn/machine-learning",
        "platform": "Coursera (Andrew Ng) / Fast.ai",
        "duration": "8-12 weeks",
        "certification": "Google ML Professional Certificate",
    },
    "system design": {
        "beginner": "https://github.com/donnemartin/system-design-primer",
        "platform": "Grokking System Design / Educative",
        "duration": "4-8 weeks",
    },
}


def get_benchmark(
    role: str,
    experience_level: str,
) -> Dict[str, List[str]]:
    """
    Get skill benchmark for a specific role and level.

    Args:
        role: Job role key (e.g., 'python_developer')
        experience_level: Level (fresher/junior/mid/senior)

    Returns:
        dict with must_have, good_to_have, bonus lists
    """
    # Normalize inputs
    role_key = role.lower().replace(" ", "_").replace("-", "_")
    level = experience_level.lower()

    # Try direct match first
    if role_key in INDUSTRY_BENCHMARKS:
        benchmark = INDUSTRY_BENCHMARKS[role_key]
        if level in benchmark:
            return benchmark[level]
        # Default to mid if level not found
        return benchmark.get("mid", {})

    # Fuzzy match for common role variations
    role_mapping = {
        "python": "python_developer",
        "backend": "python_developer",
        "backend_development": "python_developer",
        "ml": "ml_engineer",
        "machine_learning": "ml_engineer",
        "data_science": "data_scientist",
        "full_stack": "full_stack_developer",
        "fullstack": "full_stack_developer",
        "devops": "devops_engineer",
        "devops_cloud": "devops_engineer",
        "ai": "ai_engineer",
        "artificial_intelligence": "ai_engineer",
    }

    mapped_role = role_mapping.get(role_key)
    if mapped_role and mapped_role in INDUSTRY_BENCHMARKS:
        benchmark = INDUSTRY_BENCHMARKS[mapped_role]
        return benchmark.get(level, benchmark.get("mid", {}))

    # Role not found — return None so caller can use AI generation
    return None


def get_learning_resource(skill: str) -> Dict[str, str]:
    """
    Get learning resource for a specific skill.

    Args:
        skill: Skill name

    Returns:
        dict with resource information
    """
    skill_lower = skill.lower()
    return LEARNING_RESOURCES.get(
        skill_lower,
        {
            "platform": "Coursera / Udemy / YouTube",
            "duration": "2-6 weeks",
            "beginner": f"Search '{skill} tutorial' on Google",
        },
    )


def get_all_roles() -> List[str]:
    """Return list of all supported role names."""
    return [
        data["display_name"]
        for data in INDUSTRY_BENCHMARKS.values()
    ]