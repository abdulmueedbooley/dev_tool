from datetime import datetime, timezone

def months_ago(months_old):
    if months_old == None:
        return None
    released = datetime.fromisoformat(months_old.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    month_amount = (now - released).days // 30
    return month_amount

def calculate_score(months_old, vul_count):
    AGE_PEN = [(24, 60), (12, 30), (6, 10)]

    unknown_age_pen = 30
    points_per_vul = 15
    score = 100

    if months_old == None:
        score -= unknown_age_pen

    for month_limit, penalty in AGE_PEN:
        if months_old > month_limit:
            score -= penalty
            break

    score -= points_per_vul  * vul_count

    return max(0, min(100, score))



GRADE_BANDS = [
    (90,"A"),
    (75,"B"),
    (50,"C"),
    (30,"D")
]

def score_grade(score):
    for min, grade in GRADE_BANDS:
        if score >= min:
            return grade
    return "F"

RISK_TABLE = {
    "PERMISSIVE": {"internal": "Low", "saas": "Low",    "shipped": "Low"},
    "GPL":        {"internal": "Low", "saas": "Medium", "shipped": "High"},
    "AGPL":       {"internal": "Low", "saas": "High",   "shipped": "High"},
    "UNKNOWN":    {"internal": "Medium", "saas": "Medium", "shipped": "Medium"},
}

def license_family(license_text):
    text = license_text.upper()
    if "AGPL" in text:
        return "AGPL"
    if "GPL" in text:
        return "GPL"
    if any(word in text for word in ("MIT", "BSD", "APACHE")):
        return "PERMISSIVE"
    return "UNKNOWN"

def license_risk(license_text, project_type):
    family = license_family(license_text)
    return RISK_TABLE[family][project_type]

def reasoning(months_old, vul_count, risk):
    parts= []

    if months_old == None:
        parts.append("Release date UNKNOWN")
    if months_old > 24:
        parts.append(f"Last release in {months_old}")
    if months_old > 12:
        parts.append(f"Last release in {months_old}")
    else:
        parts.append("Recently updated")

    if vul_count > 0:
        parts.append(f"{vul_count} vulnerabilities")
    if risk == "High":
        parts.append("license is risky for this project type")

    return ','.join(parts) + '.'

def score_package(information, project_type, vul=0):
    months_old  = months_ago(information["last_release"])
    score = calculate_score(months_old,vul)
    risk = license_risk(information["license"], project_type)

    return {
        "name" : information["name"],
        "score" : score,
        "grade" : score_grade(score),
        "license_risk" : risk,
        "reason" : reasoning(months_old, vul, risk)
    }