import re
from typing import Dict, List, Optional, Tuple


SENSITIVE_TERMS = {
    "female", "male", "gender", "race", "ethnicity", "religion", "religious",
    "age", "old", "young", "disability", "disabled", "pregnant", "married",
    "single", "sexual orientation", "lgbt", "nationality", "caste",
}

YEARS_RE = re.compile(r"(\d+(?:\.\d+)?)\+?\s*years?", re.IGNORECASE)
YEAR_RE = re.compile(r"(19\d{2}|20\d{2})")
CERT_KEYWORDS = {"certification", "certifications", "certificate", "certificates", "certified"}
PROJECT_KEYWORDS = {"project", "projects"}
EXPERIENCE_KEYWORDS = {"year", "years", "experience", "experienced", "worked", "background"}
GRADUATION_KEYWORDS = {"graduated", "graduation", "graduated in", "completed in", "passout", "passed out"}


def is_sensitive_question(query: str) -> bool:
    q = query.lower()
    return any(term in q for term in SENSITIVE_TERMS)


def format_years(years: Optional[float]) -> str:
    if years is None:
        return "Unknown"
    if abs(years - round(years)) < 0.05:
        return f"{int(round(years))}"
    return f"{years:.1f}"


def estimate_years_experience(raw_text: str) -> Optional[float]:
    if not raw_text:
        return None

    matches = [float(m.group(1)) for m in YEARS_RE.finditer(raw_text)]
    return max(matches) if matches else None


def count_items(value) -> int:
    if isinstance(value, list):
        return len(value)
    return 0


def extract_graduation_years(education_items: List[str]) -> List[int]:
    years: List[int] = []
    for item in education_items or []:
        for match in YEAR_RE.findall(item):
            years.append(int(match))
    return sorted(set(years))


def detect_intent(query: str) -> str:
    q = query.lower()

    if is_sensitive_question(q):
        return "refuse"

    if any(k in q for k in GRADUATION_KEYWORDS):
        return "graduation_year"

    if any(k in q for k in CERT_KEYWORDS):
        return "certifications"

    if any(k in q for k in PROJECT_KEYWORDS):
        return "projects"

    if any(k in q for k in EXPERIENCE_KEYWORDS):
        return "experience_years"

    return "retrieval"


def answer_structured_question(query: str, resume_profiles: List[Dict]) -> Optional[Dict]:
    if not resume_profiles:
        return None

    intent = detect_intent(query)

    if intent == "refuse":
        return {
            "type": "refuse",
            "answer": "I cannot infer sensitive attributes like gender from resumes.",
        }

    if intent == "experience_years":
        rows = []
        for item in resume_profiles:
            profile = item.get("profile", {})
            basic = profile.get("basic_info", {})
            name = basic.get("name_guess") or item.get("filename", "Unknown")
            years = estimate_years_experience(item.get("raw_text", ""))

            rows.append(
                {
                    "name": name,
                    "filename": item.get("filename", "Unknown"),
                    "years": years if years is not None else 0.0,
                }
            )

        rows = sorted(rows, key=lambda x: x["years"], reverse=True)
        top_years = rows[0]["years"]
        leaders = [r for r in rows if abs(r["years"] - top_years) < 0.01]
        details = [f"{r['name']}: {format_years(r['years'])} years" for r in rows]

        if len(leaders) == 1:
            top = leaders[0]
            answer = f"{top['name']} appears to have the most experience at about {format_years(top['years'])} years."
        else:
            names = ", ".join(r["name"] for r in leaders)
            answer = f"{names} are tied at about {format_years(top_years)} years of experience."

        return {"type": "structured", "answer": answer, "details": details}

    if intent == "certifications":
        rows = []
        for item in resume_profiles:
            profile = item.get("profile", {})
            basic = profile.get("basic_info", {})
            name = basic.get("name_guess") or item.get("filename", "Unknown")
            cert_count = count_items(profile.get("certifications", []))

            rows.append(
                {
                    "name": name,
                    "filename": item.get("filename", "Unknown"),
                    "count": cert_count,
                }
            )

        rows = sorted(rows, key=lambda x: x["count"], reverse=True)
        top_count = rows[0]["count"]
        leaders = [r for r in rows if r["count"] == top_count]
        details = [f"{r['name']}: {r['count']} certification(s)" for r in rows]

        if top_count == 0:
            answer = "I could not find any certifications listed in the uploaded resumes."
        elif len(leaders) == 1:
            answer = f"{leaders[0]['name']} has the most certifications with {top_count}."
        else:
            names = ", ".join(r["name"] for r in leaders)
            answer = f"{names} are tied for the most certifications with {top_count} each."

        return {"type": "structured", "answer": answer, "details": details}

    if intent == "projects":
        rows = []
        for item in resume_profiles:
            profile = item.get("profile", {})
            basic = profile.get("basic_info", {})
            name = basic.get("name_guess") or item.get("filename", "Unknown")
            project_count = count_items(profile.get("projects", []))

            rows.append(
                {
                    "name": name,
                    "filename": item.get("filename", "Unknown"),
                    "count": project_count,
                }
            )

        rows = sorted(rows, key=lambda x: x["count"], reverse=True)
        top_count = rows[0]["count"]
        leaders = [r for r in rows if r["count"] == top_count]
        details = [f"{r['name']}: {r['count']} project(s)" for r in rows]

        if top_count == 0:
            answer = "I could not find any projects listed in the uploaded resumes."
        elif len(leaders) == 1:
            answer = f"{leaders[0]['name']} has the most projects with {top_count}."
        else:
            names = ", ".join(r["name"] for r in leaders)
            answer = f"{names} are tied for the most projects with {top_count} each."

        return {"type": "structured", "answer": answer, "details": details}

    if intent == "graduation_year":
        target_year_match = YEAR_RE.search(query)
        if not target_year_match:
            return None

        target_year = int(target_year_match.group(1))
        rows = []

        for item in resume_profiles:
            profile = item.get("profile", {})
            basic = profile.get("basic_info", {})
            name = basic.get("name_guess") or item.get("filename", "Unknown")
            education_items = profile.get("education", [])
            graduation_years = extract_graduation_years(education_items)

            rows.append(
                {
                    "name": name,
                    "filename": item.get("filename", "Unknown"),
                    "years": graduation_years,
                }
            )

        matches = [r for r in rows if target_year in r["years"]]
        details = [
            f"{r['name']}: {', '.join(str(y) for y in r['years']) if r['years'] else 'No year found'}"
            for r in rows
        ]

        if not matches:
            answer = f"I could not find any candidates who clearly graduated in {target_year}."
        elif len(matches) == 1:
            answer = f"{matches[0]['name']} appears to have graduated in {target_year}."
        else:
            names = ", ".join(r["name"] for r in matches)
            answer = f"{names} appear to have graduated in {target_year}."

        return {"type": "structured", "answer": answer, "details": details}

    return None
