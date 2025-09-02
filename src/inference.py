"""
SageMaker Inference Handler for Math Calculator Model

This module provides the inference interface for the MathCalculator model
when deployed on Amazon SageMaker. It implements the required SageMaker
inference functions: model_fn, input_fn, predict_fn, and output_fn.

Expected Input Format:
{
    "operation": "add",  # Required: operation name
    "a": 10,            # Required: first operand
    "b": 5              # Optional: second operand (for binary operations)
}

Output Format:
{
    "operation": "add",
    "input_a": 10,
    "input_b": 5,
    "result": 15,
    "status": "success"
}

Error Format:
{
    "error": "Error message",
    "status": "error"
}
"""

import json
import os
from calculator_model import MathCalculator

def model_fn(model_dir):
    """
    Load the model for inference.
    
    This function is called once when the SageMaker endpoint starts up.
    It should return the model object that will be used for predictions.
    
    Args:
        model_dir (str): Path to the directory containing model artifacts
        
    Returns:
        MathCalculator: Initialized calculator model instance
    """
    return MathCalculator()

def input_fn(request_body, content_type='application/json'):
    """
    Parse and validate input data for inference.
    
    Args:
        request_body (str): Raw request body from the client
        content_type (str): Content type of the request
        
    Returns:
        dict: Parsed input data
        
    Raises:
        ValueError: If content type is not supported
    """
    if content_type == 'application/json':
        try:
            return json.loads(request_body)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
    
    raise ValueError(f"Unsupported content type: {content_type}. "
                    "Only 'application/json' is supported.")

def predict_fn(input_data, model):
    """
    Run inference on the input data.
    
    Args:
        input_data (dict): Parsed input data from input_fn
        model (MathCalculator): Model instance from model_fn
        
    Returns:
        dict: Prediction result with operation details and result
        
    Expected input_data format:
        {
            "operation": "add",  # Required
            "a": 10,            # Required
            "b": 5              # Optional for unary operations
        }
    """
    try:
        # Validate required parameters
        operation = input_data.get('operation')
        a = input_data.get('a')
        b = input_data.get('b')
        
        if operation is None:
            raise ValueError("Missing required parameter: 'operation'")
        if a is None:
            raise ValueError("Missing required parameter: 'a'")
        
        # Perform calculation
        result = model.calculate(operation, a, b)
        
        # Return structured response
        return {
            'operation': operation,
            'input_a': a,
            'input_b': b,
            'result': float(result),  # Ensure result is JSON serializable
            'status': 'success'
        }
    
    except Exception as e:
        # Return error response
        return {
            'error': str(e),
            'status': 'error'
        }

def output_fn(prediction, accept='application/json'):
    """
    Format the prediction output.
    
    Args:
        prediction (dict): Prediction result from predict_fn
        accept (str): Requested response content type
        
    Returns:
        tuple: (formatted_output, content_type)
        
    Raises:
        ValueError: If accept type is not supported
    """
    if accept == 'application/json':
        return json.dumps(prediction), accept
    
    raise ValueError(f"Unsupported accept type: {accept}. "
                    "Only 'application/json' is supported.")