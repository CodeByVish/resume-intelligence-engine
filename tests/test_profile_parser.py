from src.parsing.profile_parser import build_resume_profile


def test_build_resume_profile_basic():
    sample = """
John Q. Public
john.public@example.com

Skills
- Python
- NLP

Experience
- Worked on NLP pipelines
"""

    profile = build_resume_profile(sample)
    assert isinstance(profile, dict)
    assert profile["basic_info"]["name_guess"].lower().startswith("john")
    assert "python" in [s.lower() for s in profile.get("skills", [])]
