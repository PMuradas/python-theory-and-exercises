import contextlib
import copy
import io
import json
import os
import random
import sys

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import scoring  # noqa: E402

with open(os.path.join(HERE, "questions.json"), encoding="utf-8") as f:
    BANK = json.load(f)
for i, q in enumerate(BANK["questions"], 1):
    q["number"] = i


def run(code):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exec(code, {})
    return buffer.getvalue()


def solved_namespace(tiers=("basic", "intermediate", "advanced"), pro=True):
    ns = {}
    for q in BANK["questions"]:
        if q["tier"] not in tiers:
            continue
        if q["type"] in ("mcq", "output"):
            ns[scoring.answer_name(q)] = q["answer"]
        else:
            exec(q["solution"], ns)
    if pro:
        for p in BANK["pro"]:
            exec(p["solution"], ns)
    return ns


# ------------------------------------------------------------------ the bank itself
def test_structure():
    counts = {t: sum(q["tier"] == t for q in BANK["questions"]) for t in scoring.TIERS}
    assert counts == {"basic": 12, "intermediate": 10, "advanced": 8}
    for tier, units in BANK["tier_units"].items():
        assert sum(q["weight"] for q in BANK["questions"] if q["tier"] == tier) == units
    assert sum(BANK["tier_units"].values()) == 1000
    assert len({q["id"] for q in BANK["questions"]}) == 30
    assert all(q["topic"] in BANK["topics"] for q in BANK["questions"])


@pytest.mark.parametrize("q", [q for q in BANK["questions"] if q["type"] == "output"], ids=lambda q: q["id"])
def test_output_answers_are_what_the_code_prints(q):
    assert scoring.clean_text(run(q["code"])) == scoring.clean_text(q["answer"])


@pytest.mark.parametrize("q", [q for q in BANK["questions"] if q["type"] == "mcq"], ids=lambda q: q["id"])
def test_mcq_answers_are_valid(q):
    assert q["answer"] in q["options"] and len(q["options"]) == 4


@pytest.mark.parametrize("q", [q for q in BANK["questions"] if q["type"] == "code"] + BANK["pro"], ids=lambda q: q["id"])
def test_reference_solutions_pass_every_case(q):
    ns = {}
    exec(q["solution"], ns)
    assert all(scoring.run_case(ns, c) for c in q["cases"])


@pytest.mark.parametrize("q", [q for q in BANK["questions"] if q["type"] == "code"] + BANK["pro"], ids=lambda q: q["id"])
def test_starter_code_scores_nothing(q):
    if "starter" not in q:
        return
    ns = {}
    exec(q["starter"], ns)
    assert not any(scoring.run_case(ns, c) for c in q["cases"])


# ------------------------------------------------------------------ scoring rules
def test_perfect_score_unlocks_pro():
    ns = solved_namespace()
    result = scoring.grade(ns, BANK)
    assert result["score"] == 100 and result["level"] == "Perfect score"
    pro = scoring.grade_pro(ns, BANK, result)
    assert pro["unlocked"] and pro["pro"]


def test_perfect_score_without_pro_solutions_is_not_pro():
    ns = solved_namespace(pro=False)
    result = scoring.grade(ns, BANK)
    pro = scoring.grade_pro(ns, BANK, result)
    assert result["score"] == 100 and pro["unlocked"] and not pro["pro"]


def test_pro_is_locked_below_100():
    ns = solved_namespace()
    ns["answer_01"] = "b"  # one wrong multiple choice
    result = scoring.grade(ns, BANK)
    pro = scoring.grade_pro(ns, BANK, result)
    assert result["score"] < 100 and not pro["unlocked"] and not pro["pro"]


def test_blank_test_scores_zero():
    result = scoring.grade({}, BANK)
    assert result["score"] == 0 and result["level"] == "Basic"


def test_only_basic_perfect_is_33():
    result = scoring.grade(solved_namespace(tiers=("basic",), pro=False), BANK)
    assert result["score"] == 33 and result["level"] == "Basic"


def test_basic_and_intermediate_perfect_is_66():
    result = scoring.grade(solved_namespace(tiers=("basic", "intermediate"), pro=False), BANK)
    assert result["score"] == 66 and result["level"] == "Intermediate"


def test_advanced_needs_more_than_two_perfect_tiers():
    ns = solved_namespace(tiers=("basic", "intermediate"), pro=False)
    for q in BANK["questions"]:
        if q["tier"] == "advanced" and q["type"] == "mcq":
            ns[scoring.answer_name(q)] = q["answer"]
    result = scoring.grade(ns, BANK)
    assert result["score"] == 72 and result["level"] == "Advanced"


def test_level_boundaries():
    assert [scoring.level_for(s) for s in (0, 33, 34, 66, 67, 99, 100)] == [
        "Basic", "Basic", "Intermediate", "Intermediate", "Advanced", "Advanced", "Perfect score"]


def test_wrong_multiple_choice_costs_a_third_and_tiers_never_go_negative():
    ns = {}
    for q in BANK["questions"]:
        if q["type"] == "mcq":
            ns[scoring.answer_name(q)] = next(k for k in q["options"] if k != q["answer"])
    result = scoring.grade(ns, BANK)
    assert result["score"] == 0
    one_wrong = solved_namespace(tiers=("basic",), pro=False)
    one_wrong["answer_01"] = "b"          # b01 is worth 22 units, wrong costs 22/3
    result = scoring.grade(one_wrong, BANK)
    assert abs(result["points"] - (33 - 2.2 - 2.2 / 3)) < 1e-9


def test_blank_multiple_choice_costs_nothing():
    ns = solved_namespace(tiers=("basic",), pro=False)
    ns["answer_01"] = "?"
    assert abs(scoring.grade(ns, BANK)["points"] - (33 - 2.2)) < 1e-9


def test_almost_perfect_is_never_rounded_up_to_100():
    ns = solved_namespace()
    ns["max_of_three"] = lambda a, b, c: 0 if (a, b, c) == (1, 2, 3) else max(a, b, c)   # fails exactly one of five cases
    result = scoring.grade(ns, BANK)
    assert result["points"] < 100 and result["score"] == 99 and result["level"] == "Advanced"


def test_code_questions_give_partial_credit():
    ns = solved_namespace(tiers=("basic",), pro=False)
    ns["max_of_three"] = lambda a, b, c: a   # right only when a is the largest
    result = scoring.grade(ns, BANK)
    assert 0 < 33 - result["points"] < 4


def test_random_guessing_scores_very_little():
    rng = random.Random(7)
    scores = []
    for _ in range(2000):
        ns = {}
        for q in BANK["questions"]:
            if q["type"] == "mcq":
                ns[scoring.answer_name(q)] = rng.choice("abcd")
        scores.append(scoring.grade(ns, BANK)["score"])
    assert sum(scores) / len(scores) < 5
    assert max(scores) < 34 + 20


def test_runaway_code_is_stopped():
    ns = {}
    exec("def f():\n    while True:\n        pass", ns)
    assert scoring.run_case(ns, {"call": "f()", "expected": 1}) is False


def test_bank_round_trip():
    assert scoring.decode_bank(scoring.encode_bank({"a": [1, 2]})) == {"a": [1, 2]}
