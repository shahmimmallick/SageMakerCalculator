"""
Pytest unit tests for the SageMaker inference script (src/inference.py).

This file tests the model_fn, input_fn, predict_fn, and output_fn
to ensure they behave as expected for local development and debugging.
"""

import json
import math
import sys
from pathlib import Path
import pytest

# --- Path setup to find the 'src' directory ---
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

try:
    # Import from your actual inference script
    from inference import input_fn, predict_fn, output_fn, model_fn
    from calculator_model import MathCalculator
except ImportError:
    raise ImportError(
        "Could not import from 'inference.py' or 'calculator_model.py'. "
        "Please ensure these files exist in the 'src' directory."
    )


@pytest.fixture(scope="module")
def model():
    """Pytest fixture to load the model once for all tests in this module."""
    return model_fn(model_dir=None)


def test_model_fn():
    """Tests that model_fn correctly returns a MathCalculator instance."""
    calculator = model_fn(model_dir=None)
    assert calculator is not None
    assert isinstance(calculator, MathCalculator)


# --- Tests for input_fn ---

def test_input_fn_success():
    """Tests input_fn with valid JSON."""
    request_body = '{"operation": "add", "a": 10, "b": 5}'
    expected_data = {"operation": "add", "a": 10, "b": 5}
    assert input_fn(request_body, 'application/json') == expected_data

def test_input_fn_invalid_content_type():
    """Tests input_fn with an unsupported content type."""
    with pytest.raises(ValueError, match="Unsupported content type"):
        input_fn("some data", "text/plain")

def test_input_fn_invalid_json():
    """Tests input_fn with malformed JSON."""
    with pytest.raises(ValueError, match="Invalid JSON format"):
        input_fn('{"a":1,', 'application/json')


# --- Tests for predict_fn ---

@pytest.mark.parametrize("payload, expected_output", [
    ({'operation': 'add', 'a': 10, 'b': 5}, {'operation': 'add', 'input_a': 10, 'input_b': 5, 'result': 15.0, 'status': 'success'}),
    ({'operation': 'sqrt', 'a': 16}, {'operation': 'sqrt', 'input_a': 16, 'input_b': None, 'result': 4.0, 'status': 'success'}),
    ({'operation': 'sin', 'a': 30}, {'operation': 'sin', 'input_a': 30, 'input_b': None, 'result': pytest.approx(0.5), 'status': 'success'}),
])
def test_predict_fn_valid_operations(model, payload, expected_output):
    """Tests predict_fn with various valid operations."""
    prediction = predict_fn(payload, model)
    assert prediction == expected_output

@pytest.mark.parametrize("payload, error_message_part", [
    ({'operation': 'divide', 'a': 20, 'b': 0}, "Division by zero"),
    ({'operation': 'invent', 'a': 10}, "Unsupported operation: invent"),
    ({'a': 10, 'b': 5}, "Missing required parameter: 'operation'"),
    ({'operation': 'add', 'b': 5}, "Missing required parameter: 'a'"),
    ({'operation': 'sqrt', 'a': -4}, "Square root of negative number"),
])
def test_predict_fn_error_cases(model, payload, error_message_part):
    """Tests predict_fn returns a JSON error for various failure modes."""
    prediction = predict_fn(payload, model)
    assert prediction['status'] == 'error'
    assert error_message_part in prediction['error']


# --- Tests for output_fn ---

def test_output_fn_success():
    """Tests output_fn with a valid prediction."""
    prediction = {'status': 'success', 'result': 42}
    accept = 'application/json'
    expected_body = json.dumps(prediction)

    # output_fn should return a tuple (body, content_type)
    body, returned_accept = output_fn(prediction, accept)

    assert returned_accept == accept
    assert body == expected_body

def test_output_fn_invalid_accept_type():
    """Tests output_fn with an unsupported accept type."""
    with pytest.raises(ValueError, match="Unsupported accept type"):
        output_fn({'result': 42}, "text/plain")