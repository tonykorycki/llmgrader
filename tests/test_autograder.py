import json
import pytest
from pathlib import Path
from llmgrader.gradescope.autograde import load_grading_schema, compute_scores


# Path to fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_compute_scores_all_pass():
    """Test that all passing submissions get full score."""
    # Load grading schema
    schema_path = FIXTURES_DIR / "grade_schema.xml"
    schema_questions = load_grading_schema(schema_path)
    
    # Load submission JSON
    submission_path = FIXTURES_DIR / "submission_full.json"
    with open(submission_path, "r") as f:
        submission_json = json.load(f)
    
    # Compute scores
    results = compute_scores(schema_questions, submission_json)
    
    # Assert total score
    assert results["score"] == 20.0, f"Expected total score 20, got {results['score']}"
    assert results["max_score"] == 20.0, f"Expected max score 20, got {results['max_score']}"
    
    # Assert per-question scores
    tests = results["tests"]
    assert len(tests) == 2, f"Expected 2 tests, got {len(tests)}"
    
    # Find Q1 and Q2 results
    q1_result = next((t for t in tests if t["name"] == "Q1"), None)
    q2_result = next((t for t in tests if t["name"] == "Q2"), None)
    
    assert q1_result is not None, "Q1 result not found"
    assert q2_result is not None, "Q2 result not found"
    
    # Check Q1 score (10 points)
    assert q1_result["score"] == 10.0, f"Expected Q1 score 10, got {q1_result['score']}"
    assert q1_result["max_score"] == 10.0, f"Expected Q1 max score 10, got {q1_result['max_score']}"
    
    # Check Q2 score (10 points)
    assert q2_result["score"] == 10.0, f"Expected Q2 score 10, got {q2_result['score']}"
    assert q2_result["max_score"] == 10.0, f"Expected Q2 max score 10, got {q2_result['max_score']}"


def test_missing_question():
    """Test that missing questions receive 0 points."""
    # Load grading schema
    schema_path = FIXTURES_DIR / "grade_schema.xml"
    schema_questions = load_grading_schema(schema_path)
    
    # Load submission JSON (only Q1, Q2 missing)
    submission_path = FIXTURES_DIR / "submission_missing_question.json"
    with open(submission_path, "r") as f:
        submission_json = json.load(f)
    
    # Compute scores
    results = compute_scores(schema_questions, submission_json)
    
    # Assert total score (Q1 present = 10, Q2 missing = 0)
    assert results["score"] == 10.0, f"Expected total score 10, got {results['score']}"
    assert results["max_score"] == 20.0, f"Expected max score 20, got {results['max_score']}"
    
    # Assert per-question scores
    tests = results["tests"]
    assert len(tests) == 2, f"Expected 2 tests, got {len(tests)}"
    
    # Find Q1 and Q2 results
    q1_result = next((t for t in tests if t["name"] == "Q1"), None)
    q2_result = next((t for t in tests if t["name"] == "Q2"), None)
    
    assert q1_result is not None, "Q1 result not found"
    assert q2_result is not None, "Q2 result not found"
    
    # Check Q1 score (10 points - present and passing)
    assert q1_result["score"] == 10.0, f"Expected Q1 score 10, got {q1_result['score']}"
    assert q1_result["max_score"] == 10.0, f"Expected Q1 max score 10, got {q1_result['max_score']}"
    
    # Check Q2 score (0 points - missing)
    assert q2_result["score"] == 0.0, f"Expected Q2 score 0, got {q2_result['score']}"
    assert q2_result["max_score"] == 10.0, f"Expected Q2 max score 10, got {q2_result['max_score']}"


def test_missing_part():
    """Test that missing parts within a question receive 0 points."""
    # Load grading schema
    schema_path = FIXTURES_DIR / "grade_schema.xml"
    schema_questions = load_grading_schema(schema_path)
    
    # Load submission JSON (Q2 with only p1, p2 missing)
    submission_path = FIXTURES_DIR / "submission_missing_part.json"
    with open(submission_path, "r") as f:
        submission_json = json.load(f)
    
    # Compute scores
    results = compute_scores(schema_questions, submission_json)
    
    # Assert total score (Q2.p1 pass = 5, Q2.p2 missing = 0)
    assert results["score"] == 5.0, f"Expected total score 5, got {results['score']}"
    assert results["max_score"] == 20.0, f"Expected max score 20, got {results['max_score']}"
    
    # Assert per-question scores
    tests = results["tests"]
    
    # Find Q2 result
    q2_result = next((t for t in tests if t["name"] == "Q2"), None)
    
    assert q2_result is not None, "Q2 result not found"
    
    # Check Q2 score (5 points - only p1 passes, p2 missing)
    assert q2_result["score"] == 5.0, f"Expected Q2 score 5, got {q2_result['score']}"
    assert q2_result["max_score"] == 10.0, f"Expected Q2 max score 10, got {q2_result['max_score']}"


def test_fail_cases():
    """Test that failing submissions receive 0 points."""
    # Load grading schema
    schema_path = FIXTURES_DIR / "grade_schema.xml"
    schema_questions = load_grading_schema(schema_path)
    
    # Load submission JSON (Q1 fails, Q2.p1 passes, Q2.p2 fails)
    submission_path = FIXTURES_DIR / "submission_fail.json"
    with open(submission_path, "r") as f:
        submission_json = json.load(f)
    
    # Compute scores
    results = compute_scores(schema_questions, submission_json)
    
    # Assert total score (Q1 fail = 0, Q2.p1 pass = 5, Q2.p2 fail = 0)
    assert results["score"] == 5.0, f"Expected total score 5, got {results['score']}"
    assert results["max_score"] == 20.0, f"Expected max score 20, got {results['max_score']}"
    
    # Assert per-question scores
    tests = results["tests"]
    assert len(tests) == 2, f"Expected 2 tests, got {len(tests)}"
    
    # Find Q1 and Q2 results
    q1_result = next((t for t in tests if t["name"] == "Q1"), None)
    q2_result = next((t for t in tests if t["name"] == "Q2"), None)
    
    assert q1_result is not None, "Q1 result not found"
    assert q2_result is not None, "Q2 result not found"
    
    # Check Q1 score (0 points - fails)
    assert q1_result["score"] == 0.0, f"Expected Q1 score 0, got {q1_result['score']}"
    assert q1_result["max_score"] == 10.0, f"Expected Q1 max score 10, got {q1_result['max_score']}"
    
    # Check Q2 score (5 points - p1 passes, p2 fails)
    assert q2_result["score"] == 5.0, f"Expected Q2 score 5, got {q2_result['score']}"
    assert q2_result["max_score"] == 10.0, f"Expected Q2 max score 10, got {q2_result['max_score']}"
