import re
from typing import Dict, List


SECTION_ALIASES = {
    "summary": ["summary", "professional summary", "profile", "about", "objective"],
    "experience": ["experience", "work experience", "employment", "professional experience", "internship", "internships"],
    "education": ["education", "academic background", "academics"],
    "skills": ["skills", "technical skills", "core skills", "key skills", "competencies"],
    "projects": ["projects", "project experience", "selected projects"],
    "certifications": ["certifications", "certificate", "licenses", "licenses & certifications"],
}


def extract_basic_info(text: str) -> Dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    first_line = lines[0] if lines else "Unknown"

    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}", text)
    linkedin_match = re.search(r"(https?://)?(www\.)?linkedin\.com/[^\s]+", text, re.IGNORECASE)
    github_match = re.search(r"(https?://)?(www\.)?github\.com/[^\s]+", text, re.IGNORECASE)

    return {
        "name_guess": first_line,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "linkedin": linkedin_match.group(0) if linkedin_match else "",
        "github": github_match.group(0) if github_match else "",
    }


def normalize_section_name(name: str) -> str:
    name = name.lower().strip().replace(":", "")
    for canonical, aliases in SECTION_ALIASES.items():
        if name == canonical or name in aliases:
            return canonical
    return name


def split_into_sections(text: str) -> Dict[str, str]:
    lines = [line.rstrip() for line in text.splitlines()]
    sections: Dict[str, List[str]] = {}
    current_section = "other"
    sections[current_section] = []

    section_words = set()
    for aliases in SECTION_ALIASES.values():
        section_words.update(aliases)

    section_pattern = re.compile(r"^[A-Za-z][A-Za-z\s/&,-]{1,40}:?$")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        candidate = line.lower().replace(":", "").strip()

        if section_pattern.match(line) and candidate in section_words:
            current_section = normalize_section_name(candidate)
            sections.setdefault(current_section, [])
        else:
            sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
        if "\n".join(content).strip()
    }


def extract_bullets(section_text: str) -> List[str]:
    bullets = []
    for line in section_text.splitlines():
        clean = line.strip().lstrip("-•*").strip()
        if clean:
            bullets.append(clean)
    return bullets


def build_resume_profile(text: str) -> Dict:
    basic_info = extract_basic_info(text)
    sections = split_into_sections(text)

    profile = {
        "basic_info": basic_info,
        "sections": sections,
        "skills": extract_bullets(sections.get("skills", "")),
        "experience": extract_bullets(sections.get("experience", "")),
        "education": extract_bullets(sections.get("education", "")),
        "projects": extract_bullets(sections.get("projects", "")),
        "certifications": extract_bullets(sections.get("certifications", "")),
    }

    return profile