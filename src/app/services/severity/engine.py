def calculate_severity_score(finding: dict) -> int:
    score = 0
    impact = finding.get("potential_impact", "").lower()
    if any(word in impact for word in ["critical", "system compromise", "data loss"]):
        score += 4
    elif any(word in impact for word in ["high", "security breach", "service outage"]):
        score += 3
    elif any(word in impact for word in ["medium", "degradation", "failure"]):
        score += 2
    else:
        score += 1
    frequency = finding.get("count", 1)
    if frequency >= 100:
        score += 3
    elif frequency >= 20:
        score += 2
    elif frequency >= 5:
        score += 1
    category = finding.get("category", "").lower()
    if category == "security":
        score += 3
    return score


def severity_level(score: int) -> str:
    if score >= 8:
        return "CRITICAL"
    elif score >= 6:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    return "LOW"


def assign_severity(findings: list[dict]) -> list[dict]:
    updated_findings = []
    for finding in findings:
        score = calculate_severity_score(finding)
        level = severity_level(score)
        updated_finding = {**finding, "severity_score": score, "severity": level}
        updated_findings.append(updated_finding)
    return updated_findings
