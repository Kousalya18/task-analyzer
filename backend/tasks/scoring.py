from datetime import date
from dateutil.parser import parse as parse_date


# -----------------------------
# Helper Functions
# -----------------------------

def parse_due(d):
    """Convert string to date object safely."""
    if not d:
        return None
    try:
        return parse_date(d).date()
    except:
        return None


def urgency_score(due):
    """Higher score means more urgent."""
    today = date.today()

    if not due:
        return 0.1   # no due date = low urgency

    days_left = (due - today).days

    if days_left < 0:
        # Past due → extra urgency
        return 1 + min(1, abs(days_left) / 7)  

    # If due in future → normalize
    return max(0, 1 - (days_left / 30))


def effort_score(hours):
    """Lower hours = higher score (quick win)."""
    try:
        h = float(hours)
        return 1 / (1 + h)
    except:
        return 1 / (1 + 4)   # default for missing/invalid


def importance_score(imp):
    """Normalize importance (1-10) to 0–1."""
    try:
        val = float(imp)
        return max(0, min(1, val / 10))
    except:
        return 0.5


# -----------------------------
# Circular Dependency Detection
# -----------------------------

def detect_cycles(tasks):
    graph = {t["id"]: t.get("dependencies", []) for t in tasks}
    visited = {}
    cycle_nodes = set()

    def dfs(node, stack):
        if node in visited:
            return

        visited[node] = True
        stack.add(node)

        for nei in graph.get(node, []):
            if nei in stack:
                cycle_nodes.update(stack)
            else:
                dfs(nei, stack)

        stack.remove(node)

    for node in graph:
        dfs(node, set())

    return cycle_nodes



# -----------------------------
# Main Scoring Function
# -----------------------------

def score_tasks(tasks, mode="smart"):
    """
    Input: list of tasks (dicts)
    Output: same list with scores + reasons, sorted
    """

    # MODE WEIGHTS
    MODES = {
        "smart":    {"u":1.2, "i":1.4, "e":1.0, "d":1.0},
        "fastest":  {"u":0.6, "i":0.8, "e":2.0, "d":0.6},
        "impact":   {"u":0.8, "i":2.5, "e":0.3, "d":0.4},
        "deadline": {"u":2.5, "i":0.8, "e":0.3, "d":0.4},
    }

    weights = MODES.get(mode, MODES["smart"])

    # Parse due dates
    for t in tasks:
        t["due_parsed"] = parse_due(t.get("due_date"))

    # Count how many tasks depend on each task
    dep_count = {t["id"]: 0 for t in tasks}
    for t in tasks:
        for d in t.get("dependencies", []):
            if d in dep_count:
                dep_count[d] += 1

    # Detect cycles
    cycles = detect_cycles(tasks)

    scored = []

    for t in tasks:
        U = urgency_score(t["due_parsed"])
        I = importance_score(t.get("importance", 5))
        E = effort_score(t.get("estimated_hours", 4))
        D = dep_count[t["id"]] / (max(dep_count.values()) or 1)

        # Weighted score
        raw = (U * weights["u"]) + (I * weights["i"]) + (E * weights["e"]) + (D * weights["d"])
        max_possible = (2 * weights["u"]) + weights["i"] + weights["e"] + weights["d"]

        score = (raw / max_possible) * 100

        # Explanation / reasons
        reasons = []
        if t["id"] in cycles:
            reasons.append("Circular dependency detected")
        if t["due_parsed"] and t["due_parsed"] < date.today():
            reasons.append("Past due")
        if t.get("importance", 0) >= 8:
            reasons.append("High importance")
        if t.get("estimated_hours", 10) <= 2:
            reasons.append("Quick win (low effort)")
        if dep_count[t["id"]] > 0:
            reasons.append(f"Blocks {dep_count[t['id']]} other task(s)")

        scored.append({
            **t,
            "score": round(score, 2),
            "reasons": reasons
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored
