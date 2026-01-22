import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

# Detect if running inside Gradescope
if Path("/autograder").exists() and os.name != "nt":
    AG_ROOT = Path("/autograder")
else:
    # Local testing fallback
    AG_ROOT = Path.cwd()

SUBMISSION_DIR = AG_ROOT / "submission"
RESULTS_PATH = AG_ROOT / "results" / "results.json"
SCHEMA_PATH = AG_ROOT / "grading_schema.xml"



def find_submission_json() -> Path:
    """
    Locate submission_<unit>.json.
    Supports:
      - a zip containing submission_*.json
      - a raw submission_*.json file
    """
    # Look for a zip file
    zips = list(SUBMISSION_DIR.glob("*.zip"))
    if zips:
        zip_path = zips[0]
        with zipfile.ZipFile(zip_path, "r") as zf:
            candidates = [
                name for name in zf.namelist()
                if re.match(r"submission_.*\.json$", os.path.basename(name))
            ]
            if not candidates:
                raise FileNotFoundError("No submission_*.json found inside zip.")
            target = candidates[0]
            zf.extract(target, SUBMISSION_DIR)
            return SUBMISSION_DIR / target

    # Otherwise look directly
    json_files = list(SUBMISSION_DIR.glob("submission_*.json"))
    if not json_files:
        raise FileNotFoundError("No submission_*.json found in submission directory.")
    return json_files[0]


def load_grading_schema(schema_path: Path):
    """
    Parse grading_schema.xml into a list of question dicts:
    [
      {
        "id": "1",
        "qtag": "Sequential updates",
        "grade": True/False,
        "parts": [
          {"label": "all", "points": 10},
          ...
        ]
      },
      ...
    ]
    """
    tree = ET.parse(schema_path)
    root = tree.getroot()

    questions = []
    for q in root.findall("question"):
        q_id = q.get("id")

        qtag_el = q.find("qtag")
        grade_el = q.find("grade")
        parts_el = q.find("parts")

        qtag = qtag_el.text.strip() if qtag_el is not None and qtag_el.text else ""
        grade_flag = (
            grade_el.text.strip().lower() == "true"
            if grade_el is not None and grade_el.text
            else False
        )

        parts = []
        if parts_el is not None:
            for p in parts_el.findall("part"):
                label_el = p.find("part_label")
                points_el = p.find("points")
                if label_el is None or points_el is None:
                    continue
                label = label_el.text.strip()
                try:
                    points = float(points_el.text.strip())
                except Exception:
                    points = 0.0
                parts.append({"label": label, "points": points})

        questions.append(
            {
                "id": q_id,
                "qtag": qtag,
                "grade": grade_flag,
                "parts": parts,
            }
        )

    return questions


def compute_scores(schema_questions, submission_json):
    """
    Compute total score and per-question breakdown.
    JSON structure:
      {
        "<qtag>": {
          "parts": {
            "<label>": { "grade_status": "pass"/"fail", ... }
          },
          ...
        }
      }
    """
    if not isinstance(submission_json, dict) or not submission_json:
        raise ValueError("Submission JSON is empty or malformed.")

    # Set the unit data
    unit_data = submission_json


    total_score = 0.0
    max_score = 0.0
    tests = []
    overall_feedback = []

    for q in schema_questions:
        if not q["grade"]:
            continue  # skip ungraded questions

        qtag = q["qtag"]
        parts = q["parts"]

        q_max = sum(p["points"] for p in parts)
        max_score += q_max

        q_score = 0.0
        q_feedback = []

        q_json = unit_data.get(qtag)

        if q_json is None:
            tests.append({
                "name": qtag,
                "score": 0,
                "max_score": q_max,
                "output": "No submission for this question."
            })
            continue

        q_parts_json = q_json.get("parts", {})

        for p in parts:
            label = p["label"]
            points = p["points"]
            p_json = q_parts_json.get(label)

            if p_json is None:
                p_score = 0.0
                p_output = f"Missing part '{label}'."
            else:
                status = (p_json.get("grade_status") or "").strip().lower()
                feedback = p_json.get("feedback") or ""
                explanation = p_json.get("explanation") or ""

                if status == "pass":
                    p_score = points
                    p_output = "Pass."
                else:
                    p_score = 0.0
                    p_output = "Fail."

                if feedback:
                    q_feedback.append(f"[{label}] Feedback: {feedback}")
                if explanation:
                    q_feedback.append(f"[{label}] Explanation: {explanation}")

            q_score += p_score

        total_score += q_score

        tests.append({
            "name": qtag,
            "score": q_score,
            "max_score": q_max,
            "output": "\n".join(q_feedback) if q_feedback else ""
        })

        if q_feedback:
            overall_feedback.append(f"Question: {qtag}\n" + "\n".join(q_feedback))

    return {
        "score": total_score,
        "max_score": max_score,
        "tests": tests,
        "output": "\n\n".join(overall_feedback) if overall_feedback else ""
    }


def write_results(results):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "score": results["score"],
        "output": results["output"],
        "tests": results["tests"],
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(payload, f, indent=2)


def main():
    try:
        submission_json_path = find_submission_json()
        with open(submission_json_path, "r") as f:
            submission_json = json.load(f)

        schema_questions = load_grading_schema(SCHEMA_PATH)
        results = compute_scores(schema_questions, submission_json)
        write_results(results)

    except Exception as e:
        RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RESULTS_PATH, "w") as f:
            json.dump(
                {
                    "score": 0,
                    "output": f"Autograder error: {e}",
                    "tests": [],
                },
                f,
                indent=2,
            )


if __name__ == "__main__":
    main()