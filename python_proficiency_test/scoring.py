"""Scoring for the Python by Practice level test.

How the score works
-------------------
* The test is worth 100 points, split by tier: Basic 33, Intermediate 33, Advanced 34.
  Internally points are counted in tenths ("units"), so the tiers are worth 330 / 330 / 340 units.
* Multiple choice: right = full points, blank or "?" = 0, wrong = minus one third of the points.
  (With 4 options, a pure guess is worth 0 on average.)
* Typed output: all or nothing.
* Code questions: partial credit, proportional to the test cases that pass.
* Each tier is floored at 0, so a bad tier can never take points away from another one.
* The final score is rounded to the nearest whole number, but it can only be 100 when
  every single point was earned: a score below 100 points is never rounded up to 100.
* Levels: 0-33 Basic, 34-66 Intermediate, 67-99 Advanced, 100 unlocks the Pro challenge.
"""

import base64
import html
import json
import re
import signal
import zlib
from contextlib import contextmanager
from fractions import Fraction

TIERS = ["basic", "intermediate", "advanced"]
TIER_LABELS = {"basic": "Basic", "intermediate": "Intermediate", "advanced": "Advanced"}
LEVEL_LIMITS = [(33, "Basic"), (66, "Intermediate"), (99, "Advanced")]
MCQ_PENALTY = Fraction(1, 3)
WEAK_RATIO = Fraction(6, 10)
CASE_TIME_LIMIT = 2  # seconds per test case


# ----------------------------------------------------------------------------- helpers
def encode_bank(bank):
    return base64.b64encode(zlib.compress(json.dumps(bank).encode("utf-8"))).decode("ascii")


def decode_bank(text):
    return json.loads(zlib.decompress(base64.b64decode(text)).decode("utf-8"))


@contextmanager
def time_limit(seconds):
    """Stop runaway code (e.g. an infinite loop) when the platform supports it."""
    def on_timeout(signum, frame):
        raise TimeoutError("time limit exceeded")

    try:
        old = signal.signal(signal.SIGALRM, on_timeout)
    except (AttributeError, ValueError):   # no SIGALRM (Windows) or not the main thread
        yield
        return
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def clean_text(value):
    return "\n".join(line.rstrip() for line in str(value).strip().splitlines())


def run_case(namespace, case):
    """Run one test case against the learner's code. Returns True if it passes."""
    scope = dict(namespace)
    try:
        with time_limit(CASE_TIME_LIMIT):
            if case.get("setup"):
                exec(case["setup"], scope)
            value = eval(case["call"], scope)
    except Exception as error:
        names = [cls.__name__ for cls in type(error).__mro__]
        return "raises" in case and case["raises"] in names
    if "raises" in case:
        return False
    return value == case["expected"]


def level_for(score):
    for limit, name in LEVEL_LIMITS:
        if score <= limit:
            return name
    return "Perfect score"


def answer_name(question):
    return f"answer_{question['number']:02d}"


# ----------------------------------------------------------------------------- one question
def grade_question(question, namespace):
    """Return (points earned as a Fraction of units, status)."""
    weight = Fraction(question["weight"])
    kind = question["type"]

    if kind == "mcq":
        given = str(namespace.get(answer_name(question), "")).strip().lower()
        if given not in question["options"]:      # blank, "?" or anything invalid
            return Fraction(0), "blank"
        if given == question["answer"]:
            return weight, "correct"
        return -weight * MCQ_PENALTY, "wrong"

    if kind == "output":
        given = clean_text(namespace.get(answer_name(question), ""))
        if given == "":
            return Fraction(0), "blank"
        if given == clean_text(question["answer"]):
            return weight, "correct"
        return Fraction(0), "wrong"

    passed = sum(run_case(namespace, case) for case in question["cases"])
    if passed == len(question["cases"]):
        return weight, "correct"
    if passed == 0:
        return Fraction(0), "wrong"
    return weight * Fraction(passed, len(question["cases"])), "partial"


# ----------------------------------------------------------------------------- the whole test
def grade(namespace, bank):
    tiers = {t: {"earned": Fraction(0), "max": Fraction(bank["tier_units"][t])} for t in TIERS}
    topics = {}
    review = []

    for q in bank["questions"]:
        earned, status = grade_question(q, namespace)
        tiers[q["tier"]]["earned"] += earned
        topic = topics.setdefault(q["topic"], {"earned": Fraction(0), "max": Fraction(0), "tier": q["tier"]})
        topic["earned"] += earned
        topic["max"] += q["weight"]
        if status != "correct":
            review.append({"number": q["number"], "tier": q["tier"], "topic": q["topic"], "status": status,
                           "explanation": q["explanation"]})

    for t in tiers.values():
        t["earned"] = max(Fraction(0), t["earned"])
    for t in topics.values():
        t["earned"] = max(Fraction(0), t["earned"])

    units = sum(t["earned"] for t in tiers.values())
    total_units = sum(t["max"] for t in tiers.values())
    if units >= total_units:
        score = 100
    else:
        score = min(99, int(units / 10 + Fraction(1, 2)))     # round half up, never up to 100
    level = level_for(score)

    # topics worth reviewing: weak topics up to one tier above the placed level
    level_index = 2 if score >= 67 else (1 if score >= 34 else 0)
    relevant = TIERS[: min(level_index + 2, 3)]
    weak = [(TIERS.index(d["tier"]), d["earned"] / d["max"], name) for name, d in topics.items()
            if d["tier"] in relevant and d["earned"] / d["max"] < WEAK_RATIO]
    weak.sort()
    weak_topics = [name for _, _, name in weak]
    start = next((bank["topics"][t]["lesson"] for t in weak_topics if bank["topics"][t]["lesson"]), None)

    points = float(units) / 10
    notes = []
    for boundary, below, above in [(33.5, "Basic", "Intermediate"), (66.5, "Intermediate", "Advanced")]:
        if abs(points - boundary) <= 3:
            notes.append(f"You are close to the border between {below} and {above}.")
    if 97 <= score < 100:
        notes.append("You are very close to a perfect score, which unlocks the Pro challenge.")
    if tiers["basic"]["earned"] < tiers["basic"]["max"] / 2 and score >= 67:
        notes.append("Your results are uneven: you did well on harder questions but missed several basics. Review the basics.")

    return {"score": score, "points": points, "level": level, "tiers": tiers, "topics": topics,
            "weak_topics": weak_topics, "start_lesson": start, "review": review, "notes": notes}


def grade_pro(namespace, bank, result):
    details = []
    for challenge in bank["pro"]:
        passed = sum(run_case(namespace, case) for case in challenge["cases"])
        details.append({"id": challenge["id"], "title": challenge["title"], "passed": passed, "total": len(challenge["cases"])})
    unlocked = result["score"] == 100
    return {"unlocked": unlocked, "details": details,
            "pro": unlocked and all(d["passed"] == d["total"] for d in details)}


# ----------------------------------------------------------------------------- display
def _md(text):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


def _bar(percent, color):
    return (f"<div style='background:rgba(128,128,128,.25);border-radius:6px;height:12px;width:100%'>"
            f"<div style='background:{color};height:12px;border-radius:6px;width:{percent:.0f}%'></div></div>")


def render(result, bank):
    colors = {"Basic": "#2A9D8F", "Intermediate": "#E9A23B", "Advanced": "#E63946", "Perfect score": "#7B2CBF"}
    level = result["level"]
    color = colors[level]
    box = "font-family:sans-serif;max-width:760px;padding:16px 20px;border:1px solid rgba(128,128,128,.4);border-radius:10px"
    parts = [f"<div style='{box}'>",
             f"<div style='font-size:14px;opacity:.7'>Your result</div>",
             f"<div style='font-size:44px;font-weight:700;color:{color}'>{result['score']}<span style='font-size:20px;opacity:.6'> / 100</span></div>",
             f"<div style='font-size:22px;font-weight:600'>{html.escape(level)}</div>"]
    if level == "Perfect score":
        parts.append("<div style='margin-top:6px'>Perfect score! The <b>Pro challenge</b> is unlocked: solve the last two problems of the notebook and run the final cell.</div>")

    parts.append("<h4 style='margin:18px 0 6px'>By tier</h4>")
    for tier in TIERS:
        t = result["tiers"][tier]
        percent = float(t["earned"] / t["max"] * 100)
        parts.append(f"<div style='margin:6px 0'>{TIER_LABELS[tier]}: {float(t['earned']) / 10:.1f} / {float(t['max']) / 10:.0f} points{_bar(percent, color)}</div>")

    for note in result["notes"]:
        parts.append(f"<div style='margin-top:10px'><b>Note:</b> {html.escape(note)}</div>")

    parts.append("<h4 style='margin:18px 0 6px'>Where to go next</h4>")
    if result["weak_topics"]:
        items = []
        for name in result["weak_topics"][:5]:
            info = bank["topics"][name]
            lesson = f"lesson <code>{info['lesson']}</code>" if info["lesson"] else "<i>lesson coming in a later level</i>"
            items.append(f"<li>{html.escape(info['label'])} ({lesson})</li>")
        hidden = len(result["weak_topics"]) - 5
        if hidden > 0:
            items.append(f"<li><i>...and {hidden} more topic(s), see the review below</i></li>")
        parts.append("<ul style='margin:0'>" + "".join(items) + "</ul>")
        if result["start_lesson"]:
            parts.append(f"<div style='margin-top:8px'>Suggested starting point: <b>{result['start_lesson']}</b> in <code>level-1-basics/</code>.</div>")
    else:
        parts.append("<div>No weak topics. Nice work!</div>")

    if result["review"]:
        parts.append("<h4 style='margin:18px 0 6px'>Review the questions you missed</h4>")
        for item in result["review"]:
            label = {"wrong": "wrong", "blank": "not answered", "partial": "partly right"}[item["status"]]
            parts.append(f"<details style='margin:4px 0'><summary>Question {item['number']} ({label}), {html.escape(bank['topics'][item['topic']]['label'])}</summary>"
                         f"<div style='padding:6px 0 6px 16px'>{_md(item['explanation'])}</div></details>")
    parts.append("</div>")
    return "".join(parts)


def render_pro(pro):
    box = "font-family:sans-serif;max-width:760px;padding:16px 20px;border:1px solid rgba(128,128,128,.4);border-radius:10px"
    rows = "".join(f"<li>{html.escape(d['title'])}: {d['passed']} / {d['total']} test cases</li>" for d in pro["details"])
    if not pro["unlocked"]:
        head = "<b>The Pro challenge is locked.</b> Get a perfect 100 on the main test first."
    elif pro["pro"]:
        head = "<span style='font-size:30px;font-weight:700;color:#7B2CBF'>PRO</span><br>Both challenges solved on top of a perfect score. Yoooo!"
    else:
        head = "<b>Almost there.</b> You have a perfect score; now make every test case of both challenges pass to earn <b>Pro</b>."
    return f"<div style='{box}'>{head}<ul>{rows}</ul></div>"
